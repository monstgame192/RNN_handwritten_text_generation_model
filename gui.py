import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage  # To handle the image
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


def update_preview():
    try:
        # Get user inputs
        max_line_length = int(max_line_length_entry.get())
        lines_per_page = int(lines_per_page_entry.get())
        line_height = int(line_height_entry.get())
        total_lines_per_page = int(total_lines_entry.get())
        view_height = int(view_height_entry.get())
        view_width = float(view_width_entry.get())
        margin_left = int(margin_left_entry.get())
        margin_top = int(margin_top_entry.get())

        # Check if the total lines per page is not less than the lines per page
        if total_lines_per_page < lines_per_page:
            messagebox.showwarning("Input Error", "Total Lines Per Page must not be lesser than Lines Per Page.")
            return

        # Update the bottom half of the right side with current values
        height_value.set(line_height)
        width_value.set(view_width)
        margin_left_value.set(margin_left)
        margin_top_value.set(margin_top)
        total_lines_value.set(total_lines_per_page)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_generate():
    try:
        # Get user inputs
        input_text = text_box.get("1.0", tk.END).strip()
        output_dir = os.path.join(os.path.dirname(__file__), 'img')
        os.makedirs(output_dir, exist_ok=True)

        # Parameters
        max_line_length = int(max_line_length_entry.get())
        lines_per_page = int(lines_per_page_entry.get())
        handwriting_consistency = float(handwriting_consistency_entry.get())
        styles = int(styles_combobox.get())
        pen_thickness = float(pen_thickness_entry.get())
        line_height = int(line_height_entry.get())
        total_lines_per_page = int(total_lines_entry.get())
        view_height = int(view_height_entry.get())
        view_width = float(view_width_entry.get())
        margin_left = int(margin_left_entry.get())
        margin_top = int(margin_top_entry.get())

        if total_lines_per_page < lines_per_page:
            messagebox.showwarning("Input Error", "Total Lines Per Page must not be lesser than Lines Per Page.")
            return

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
        process_text(input_text, output_dir, alphabet, max_line_length, lines_per_page, handwriting_consistency, styles, pen_thickness, page)
        messagebox.showinfo("Success", "Handwriting SVG files generated successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create the main window
root = tk.Tk()
root.title("Handwriting SVG Generator")
root.resizable(False, False)

# Load image for banner
banner_image = PhotoImage(file="assets/banner.png")  # Adjust the path to your image

# Frame for text input (right half)
input_frame = tk.Frame(root, width=500, height=600)
input_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Text input box
tk.Label(input_frame, text="Input Text:").pack(padx=10, pady=5, anchor="w")
text_box = tk.Text(input_frame, wrap="word", width=40, height=20)
text_box.pack(padx=10, pady=5, fill="both", expand=True)

# Frame for parameter inputs (left half)
param_frame = tk.Frame(root, width=500, height=600)
param_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Add the banner image at the top of the parameter frame
banner_label = tk.Label(param_frame, image=banner_image)
banner_label.grid(row=0, column=0, columnspan=2, pady=5)

# Parameter input fields
fields = [
    ("Line Length (characters)", "60"), ("Lines Per Page", "24"), ("Handwriting Consistency", "0.95"), ("Styles", "1"),
    ("Pen Thickness", "1"), ("Line Height", "32"), ("Total Lines Per Page", "24"),
    ("View Height", "896"), ("View Width", "633.472"), ("Margin Left", "-64"), ("Margin Top", "-96")
]
entries = {}

for i, (label, default) in enumerate(fields):
    tk.Label(param_frame, text=f"{label}:").grid(row=i+2, column=0, padx=10, pady=5, sticky="e")
    entry = ttk.Entry(param_frame)
    entry.insert(0, default)
    entry.grid(row=i+2, column=1, padx=10, pady=5, sticky="ew")  # Added sticky="ew" for stretch
    entries[label] = entry

# Map entries to variables
max_line_length_entry = entries["Line Length (characters)"]
lines_per_page_entry = entries["Lines Per Page"]
handwriting_consistency_entry = entries["Handwriting Consistency"]
pen_thickness_entry = entries["Pen Thickness"]
line_height_entry = entries["Line Height"]
total_lines_entry = entries["Total Lines Per Page"]
view_height_entry = entries["View Height"]
view_width_entry = entries["View Width"]
margin_left_entry = entries["Margin Left"]
margin_top_entry = entries["Margin Top"]

# Styles dropdown (combobox)
tk.Label(param_frame, text="Styles:").grid(row=len(fields)+2, column=0, padx=10, pady=5, sticky="e")
styles_combobox = ttk.Combobox(param_frame, values=[str(i) for i in range(1, 8)], state="readonly")
styles_combobox.set("1")  # Default value
styles_combobox.grid(row=len(fields)+2, column=1, padx=10, pady=5, sticky="ew")

# Display values on right side (bottom section)
value_frame = tk.Frame(input_frame)
value_frame.pack(padx=10, pady=5, fill="both", expand=True)

# Labels and values for height, width, margins, and total lines
height_value = tk.StringVar(value="32")
width_value = tk.StringVar(value="633.472")
margin_left_value = tk.StringVar(value="-64")
margin_top_value = tk.StringVar(value="-96")
total_lines_value = tk.StringVar(value="24")

tk.Label(value_frame, text="Height:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(value_frame, textvariable=height_value).grid(row=0, column=1, padx=5, pady=5)

tk.Label(value_frame, text="Width:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(value_frame, textvariable=width_value).grid(row=1, column=1, padx=5, pady=5)

tk.Label(value_frame, text="Margin Left:").grid(row=2, column=0, padx=5, pady=5)
tk.Label(value_frame, textvariable=margin_left_value).grid(row=2, column=1, padx=5, pady=5)

tk.Label(value_frame, text="Margin Top:").grid(row=3, column=0, padx=5, pady=5)
tk.Label(value_frame, textvariable=margin_top_value).grid(row=3, column=1, padx=5, pady=5)

tk.Label(value_frame, text="Total Lines Per Page:").grid(row=4, column=0, padx=5, pady=5)
tk.Label(value_frame, textvariable=total_lines_value).grid(row=4, column=1, padx=5, pady=5)

# Buttons for preview and generate
button_frame = tk.Frame(param_frame)
button_frame.grid(row=len(fields)+3, column=0, columnspan=2, pady=10)

# Add Preview and Generate buttons
preview_button = ttk.Button(button_frame, text="Preview", command=update_preview)
preview_button.grid(row=0, column=0, padx=10)

generate_button = ttk.Button(button_frame, text="Generate", command=on_generate)
generate_button.grid(row=0, column=1, padx=10)

# Run the GUI
root.mainloop()
