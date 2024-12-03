import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from handwriting_synthesis import Hand


def process_text(input_text, output_dir, alphabet, max_line_length, lines_per_page, biases, styles, stroke_widths, page):
    """
    Processes text input, sanitizes, wraps, paginates it,
    and generates handwriting SVG files.
    """
    # Split input text into lines
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]

    # Sanitize lines
    sanitized_lines = [''.join(char if char in alphabet else ' ' for char in line) for line in lines]

    # Wrap lines
    wrapped_lines = []
    for line in sanitized_lines:
        words = line.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > max_line_length:
                wrapped_lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
        if current_line:
            wrapped_lines.append(current_line.strip())

    # Paginate lines
    pages = [wrapped_lines[i:i + lines_per_page] for i in range(0, len(wrapped_lines), lines_per_page)]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate handwriting SVG files
    hand = Hand()
    for page_num, page_lines in enumerate(pages):
        filename = os.path.join(output_dir, f'result_page_{page_num + 1}.svg')
        hand.write(
            filename=filename,
            lines=page_lines,
            biases=[biases] * len(page_lines),
            styles=[styles] * len(page_lines),
            stroke_widths=[stroke_widths] * len(page_lines),
            page=page
        )
        print(f"Page {page_num + 1} written to {filename}")


def on_generate():
    try:
        # Get user inputs
        input_text = text_box.get("1.0", tk.END).strip()
        output_dir = os.path.join(os.path.dirname(__file__), 'img')
        os.makedirs(output_dir, exist_ok=True)

        # Parameters
        max_line_length = int(max_line_length_entry.get())
        lines_per_page = int(lines_per_page_entry.get())
        biases = float(biases_entry.get())
        styles = int(styles_entry.get())
        stroke_widths = float(stroke_widths_entry.get())
        line_height = int(line_height_entry.get())
        total_lines_per_page = int(total_lines_entry.get())
        view_height = int(view_height_entry.get())
        view_width = float(view_width_entry.get())
        margin_left = int(margin_left_entry.get())
        margin_top = int(margin_top_entry.get())

        # Page layout
        page = [line_height, total_lines_per_page, view_height, view_width, margin_left, margin_top]

        # Alphabet
        alphabet = [
            '\x00', ' ', '!', '"', '#', "'", '(', ')', ',', '-', '.',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
            '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
            'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y',
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
            'y', 'z'
        ]

        # Process text
        process_text(input_text, output_dir, alphabet, max_line_length, lines_per_page, biases, styles, stroke_widths, page)
        messagebox.showinfo("Success", "Handwriting SVG files generated successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
root = tk.Tk()
root.title("Handwriting SVG Generator")

# Text input box
tk.Label(root, text="Input Text:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
text_box = tk.Text(root, width=60, height=10)
text_box.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

# Parameter input fields
fields = [
    ("Max Line Length", "60"), ("Lines Per Page", "24"), ("Biases", "0.95"), ("Styles", "1"),
    ("Stroke Widths", "1"), ("Line Height", "32"), ("Total Lines Per Page", "24"),
    ("View Height", "896"), ("View Width", "633.472"), ("Margin Left", "-64"), ("Margin Top", "-96")
]
entries = {}

for i, (label, default) in enumerate(fields):
    tk.Label(root, text=f"{label}:").grid(row=2 + i, column=0, padx=10, pady=5, sticky="e")
    entry = ttk.Entry(root)
    entry.insert(0, default)
    entry.grid(row=2 + i, column=1, padx=10, pady=5)
    entries[label] = entry

# Map entries to variables
max_line_length_entry = entries["Max Line Length"]
lines_per_page_entry = entries["Lines Per Page"]
biases_entry = entries["Biases"]
styles_entry = entries["Styles"]
stroke_widths_entry = entries["Stroke Widths"]
line_height_entry = entries["Line Height"]
total_lines_entry = entries["Total Lines Per Page"]
view_height_entry = entries["View Height"]
view_width_entry = entries["View Width"]
margin_left_entry = entries["Margin Left"]
margin_top_entry = entries["Margin Top"]

# Generate button
generate_button = ttk.Button(root, text="Generate", command=on_generate)
generate_button.grid(row=2 + len(fields), column=0, columnspan=2, pady=10)

root.mainloop()
