import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage  # To handle the image
from handwriting_synthesis import Hand
from tkinter.colorchooser import askcolor


def process_text(
    input_text,
    output_dir,
    alphabet,
    max_line_length,
    lines_per_page,
    biases,
    styles,
    stroke_colors,
    stroke_widths,
    page,
):
    """
    Processes text input, sanitizes, wraps, paginates it,
    and generates handwriting SVG files.
    """
    # Split input text into lines
    lines = [line.strip() for line in input_text.split("\n") if line.strip()]
    # convert stroke colors values from text counterpart to hexadecimal (black blue red and green only)
    stroke_colors = {"Black": "#000000", "Blue": "#0000FF", "Red": "#FF0000", "Green": "#008000"}[stroke_colors]

    # Sanitize lines
    sanitized_lines = [
        "".join(char if char in alphabet else " " for char in line) for line in lines
    ]

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
    pages = [
        wrapped_lines[i : i + lines_per_page]
        for i in range(0, len(wrapped_lines), lines_per_page)
    ]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate handwriting SVG files
    # def write(self, filename, lines, biases=None, styles=None, stroke_colors=None, stroke_widths=None, page=None):
    hand = Hand()
    for page_num, page_lines in enumerate(pages):
        filename = os.path.join(output_dir, f"result_page_{page_num + 1}.svg")
        hand.write(
            filename=filename,
            lines=page_lines,
            biases=[biases] * len(page_lines),
            styles=[styles] * len(page_lines),
            stroke_colors = [stroke_colors] * len(page_lines),
            stroke_widths=[stroke_widths] * len(page_lines),
            page=page,
        )
        print(f"Page {page_num + 1} written to {filename}")

margin_left_line = None
margin_top_line = None
page_preview = None
selected_page_color = "white"  # Default page color
selected_margin_color = "red"  # Default margin color
selected_line_color = "lightgray"  # Default line color
overflow = False

def update_preview():
    global margin_left_line, margin_top_line, page_preview  # Access the global variables
    global selected_page_color, selected_margin_color, selected_line_color  # Access the selected colors
    global overflow
    try:
        # Get user inputs
        view_height = float(view_height_entry.get())
        view_width = float(view_width_entry.get())
        margin_left = int(margin_left_entry.get())
        margin_top = int(margin_top_entry.get())
        total_lines = int(total_lines_entry.get())
        line_height_input = int(line_height_entry.get())  # Get the line height from user input

        # Clear the canvas before drawing
        canvas.delete("all")

        # Calculate the rectangle size
        if view_height > view_width:
            rect_height = canvas.winfo_height() * 0.9
            rect_width = (view_width / view_height) * rect_height
        else:
            rect_width = canvas.winfo_width() * 0.5
            rect_height = (view_height / view_width) * rect_width

        # Center the rectangle
        x_offset = (canvas.winfo_width() - rect_width) / 2
        y_offset = (canvas.winfo_height() - rect_height) / 2

        margin_left_ratio = margin_left / view_width
        margin_top_ratio = margin_top / view_height
        margin_left_x = x_offset + rect_width * margin_left_ratio
        margin_top_y = y_offset + rect_height * margin_top_ratio

        # Calculate the line height in pixels
        line_height_ratio = line_height_input / view_height
        actual_line_height = rect_height * line_height_ratio

        # Draw rectangle and margins
        page_preview = canvas.create_rectangle(
            x_offset, y_offset, 
            x_offset + rect_width, y_offset + rect_height,
            outline="black", fill=selected_page_color
        )

        # Draw lines and check for overflow
        current_y = margin_top_y + actual_line_height
        overflow = False

        for i in range(total_lines):
            if current_y + actual_line_height > y_offset + rect_height:
                overflow = True
                break
            canvas.create_line(
                x_offset, current_y,
                x_offset + rect_width, current_y,
                fill=selected_line_color, width=1, tags="horizontal_line"
            )
            current_y += actual_line_height

        margin_left_line = canvas.create_line(
            margin_left_x, y_offset, margin_left_x, y_offset + rect_height, 
            fill=selected_margin_color, width=2
        )
        margin_top_line = canvas.create_line(
            x_offset, margin_top_y, x_offset + rect_width, margin_top_y, 
            fill=selected_margin_color, width=2
        )

        # Draw the border rectangle for the page preview
        canvas.create_rectangle(
            x_offset, y_offset, 
            x_offset + rect_width, y_offset + rect_height,
            outline="black", fill=None
        )

        # Display dimensions and lines
        canvas.create_text(
            x_offset + 5, y_offset + rect_height / 2,
            text=f"{view_height} px", angle=90, anchor="n", font=("Arial", 10)
        )
        canvas.create_text(
            x_offset + rect_width / 2, y_offset + 5,
            text=f"{view_width} px", anchor="n", font=("Arial", 10)
        )
        canvas.create_text(
            x_offset + rect_width / 2, y_offset + rect_height - 5,
            text=f"{total_lines} Lines", anchor="s", font=("Arial", 10)
        )

        # Show a warning if overflow occurs
        if overflow:
            warning_text = "⚠ Too Many Lines"
            font_size = 12
            warning_x = canvas.winfo_width() / 2
            warning_y = canvas.winfo_height() / 2

            # Calculate text background dimensions
            text_id = canvas.create_text(
                warning_x, warning_y,
                text=warning_text,
                font=("Arial", font_size, "bold")
            )
            bbox = canvas.bbox(text_id)  # Get bounding box for the text
            canvas.delete(text_id)  # Remove the temporary text
            
            # Draw white background rectangle
            canvas.create_rectangle(
                bbox[0] - 5, bbox[1] - 2,  # Slight padding
                bbox[2] + 5, bbox[3] + 2,
                fill="white", outline=""
            )
            
            # Redraw the warning text
            canvas.create_text(
                warning_x, warning_y,
                text=warning_text,
                fill="red",
                font=("Arial", font_size, "bold")
            )

    except Exception as e:
        messagebox.showerror("Error", str(e))


def on_generate():
    update_preview()
    if overflow:
        messagebox.showwarning("Overflow", "Too many lines to fit in the given space.")
        return
    try:
        # Get user inputs
        input_text = text_box.get("1.0", tk.END).strip()
        output_dir = os.path.join(os.path.dirname(__file__), "img")
        os.makedirs(output_dir, exist_ok=True)

        # Parameters
        max_line_length = int(max_line_length_entry.get())
        lines_per_page = int(lines_per_page_entry.get())
        handwriting_consistency = float(handwriting_consistency_entry.get())
        styles = int(styles_combobox.get())
        ink_color = color_combobox.get()
        pen_thickness = float(pen_thickness_entry.get())
        line_height = int(line_height_entry.get())
        total_lines_per_page = int(total_lines_entry.get())
        view_height = float(view_height_entry.get())
        view_width = float(view_width_entry.get())
        margin_left = int(margin_left_entry.get()) * -1
        margin_top = int(margin_top_entry.get()) * -1

        if total_lines_per_page < lines_per_page:
            messagebox.showwarning(
                "Input Error",
                "Total Lines Per Page must not be lesser than Lines Written Per Page.",
            )
            return

        # Page layout
        page = [
            line_height,
            total_lines_per_page,
            view_height,
            view_width,
            margin_left,
            margin_top,
            selected_page_color,
            selected_margin_color,
            selected_line_color
        ]

        # Alphabet
        alphabet = [
            "\x00",
            " ",
            "!",
            '"',
            "#",
            "'",
            "(",
            ")",
            ",",
            "-",
            ".",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            ":",
            ";",
            "?",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "Y",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

        # Process text
        process_text(
            input_text,
            output_dir,
            alphabet,
            max_line_length,
            lines_per_page,
            handwriting_consistency,
            styles,
            ink_color,
            pen_thickness,
            page,
        )
        messagebox.showinfo("Success", "Handwriting SVG files generated successfully!")

    except Exception as e:
        messagebox.showerror("Error", str(e))

def choose_page_color():
    global page_preview, selected_page_color
    # Open color picker dialog to select page background color
    color = askcolor()[1]
    if color and page_preview:
        # Update the page preview rectangle with the selected color
        canvas.itemconfig(page_preview, fill=color)
        selected_page_color = color
        page_color_button.config(bg=color)
        print(f"Selected Page Color: {color}")

def choose_margin_color():
    global margin_left_line, margin_top_line, selected_margin_color
    # Open the color picker dialog and get the selected color
    color = askcolor()[1]  # The askcolor() function returns a tuple (rgb, hex), so we take the second element for the hex value.
    
    if color and margin_left_line and margin_top_line:
        # Update the margin lines with the selected color
        canvas.itemconfig(margin_left_line, fill=color)  # Update left margin line color
        canvas.itemconfig(margin_top_line, fill=color)   # Update top margin line color
        selected_margin_color = color
        margin_color_button.config(bg=color)
        print(f"Selected Margin Color: {color}")


def choose_line_color():
    global selected_line_color
    # Open the color picker dialog and get the selected color
    color = askcolor()[1]  # Get the hex value of the selected color

    if color:
        # Update the color of the lines in the preview canvas
        for item in canvas.find_withtag("horizontal_line"):
            # Check if the item is a line by looking at its type
            if canvas.type(item) == "line":
                canvas.itemconfig(item, fill=color)  # Update the color
        line_color_button.config(bg=color)  # Change the button color as a visual cue
        selected_line_color = color
        print(f"Selected Line Color: {color}")



def reset_default():
    # Default values as per your 'fields' list
    default_values = {
        "Line Length (characters)": "60",
        "Total Lines Per Page": "24",
        "Lines Written Per Page": "24",
        "Handwriting Consistency": "0.95",
        "Pen Thickness": "1",
        "Line Height": "32",
        "View Height": "896",
        "View Width": "633.472",
        "Margin Left": "64",
        "Margin Top": "96",
    }

    # Reset all entries to their default values
    for label, default in default_values.items():
        entries[label].delete(0, tk.END)
        entries[label].insert(0, default)

    # Reset the styles combobox to default value
    styles_combobox.set("1")
    # reset the page, margin and line colors
    global selected_page_color, selected_margin_color, selected_line_color
    selected_page_color = "white"
    selected_margin_color = "red"
    selected_line_color = "lightgray"
    # reset the color buttons to have no color at all
    page_color_button.config(bg="SystemButtonFace")
    margin_color_button.config(bg="SystemButtonFace")
    line_color_button.config(bg="SystemButtonFace")

    #reset color combo box
    color_combobox.set("Black")
    update_style_label()

    # Optionally, you can reset the canvas or other UI components as well
    canvas.delete("all")  # Clear the preview canvas
    update_preview()

# Update the style value label when the style selection changes

def update_style_label(event=None):
    # Get the selected style
    selected_style = styles_combobox.get()
    
    # Construct the image file path based on the selected style
    image_path = f"assets/font{selected_style}.png"
    
    try:
        # Load the image
        style_image = PhotoImage(file=image_path)
        
        # Update the image label
        style_value_label.config(image=style_image)
        style_value_label.image = style_image  # Keep a reference to the image to prevent garbage collection
    
    except Exception as e:
        # If the image doesn't exist or there is an error, show a default message
        style_value_label.config(text="Image not found")
        print(f"Error loading image: {e}")

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
    ("Line Length (characters)", "60"),
    ("Total Lines Per Page", "24"),
    ("Lines Written Per Page", "24"),
    ("Handwriting Consistency", "0.95"),
    ("Pen Thickness", "1"),
    ("Line Height", "32"),
    ("View Height", "896"),
    ("View Width", "633.472"),
    ("Margin Left", "64"),
    ("Margin Top", "96"),
]
entries = {}

for i, (label, default) in enumerate(fields):
    tk.Label(param_frame, text=f"{label}:").grid(
        row=i + 2, column=0, padx=5, pady=5, sticky="e"
    )
    entry = ttk.Entry(param_frame)
    entry.insert(0, default)
    entry.grid(
        row=i + 2, column=1, padx=5, pady=5, sticky="ew"
    )  # Added sticky="ew" for stretch
    entries[label] = entry

# Map entries to variables
max_line_length_entry = entries["Line Length (characters)"]
lines_per_page_entry = entries["Lines Written Per Page"]
handwriting_consistency_entry = entries["Handwriting Consistency"]
pen_thickness_entry = entries["Pen Thickness"]
line_height_entry = entries["Line Height"]
total_lines_entry = entries["Total Lines Per Page"]
view_height_entry = entries["View Height"]
view_width_entry = entries["View Width"]
margin_left_entry = entries["Margin Left"]
margin_top_entry = entries["Margin Top"]

# Styles dropdown (combobox)
tk.Label(param_frame, text="Writing Style:").grid(
    row=len(fields) + 3, column=0, padx=5, pady=5, sticky="e"
)
styles_combobox = ttk.Combobox(
    param_frame, values=[str(i) for i in range(1, 13)], state="readonly"
)
styles_combobox.set("1")  # Default value
styles_combobox.grid(row=len(fields) + 3, column=1, padx=5, pady=5, sticky="ew")

# Color dropdown (combobox)
tk.Label(param_frame, text="Ink Color:").grid(
    row=len(fields) + 2, column=0, padx=5, pady=5, sticky="e"
)
color_combobox = ttk.Combobox(
    param_frame, values=["Black", "Blue", "Red", "Green"], state="readonly"
)
color_combobox.set("Black")  # Default value
color_combobox.grid(row=len(fields) + 2, column=1, padx=5, pady=5, sticky="ew")








# Buttons for preview and generate
page_button_frame = tk.Frame(param_frame)
page_button_frame.grid(row=len(fields) + 4, column=0, columnspan=2, pady=5, padx=0, sticky="ew")

# Configure columns to expand equally
page_button_frame.grid_columnconfigure(0, weight=1, uniform="button")
page_button_frame.grid_columnconfigure(1, weight=1, uniform="button")
page_button_frame.grid_columnconfigure(2, weight=1, uniform="button")

page_color_button = tk.Button(page_button_frame, text="Page Color", command=choose_page_color, relief="groove")
page_color_button.grid(row=0, column=0, sticky="ew", padx=5)

margin_color_button = tk.Button(page_button_frame, text="Margin Color", command=choose_margin_color, relief="groove")
margin_color_button.grid(row=0, column=1, sticky="ew", padx=5)

line_color_button = tk.Button(page_button_frame, text="Line Color", relief="groove", command=choose_line_color)
line_color_button.grid(row=0, column=2, sticky="ew", padx=5)








# Display values on right side (bottom section)
value_frame = tk.Frame(input_frame)
value_frame.pack(padx=10, pady=5, fill="both", expand=True)

# Add Canvas to draw the white rectangle in the bottom section of input_frame
canvas = tk.Canvas(value_frame, bg="white")
canvas.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

# Buttons for preview and generate
button_frame = tk.Frame(param_frame)
button_frame.grid(row=len(fields) + 5, column=0, columnspan=2, pady=5, padx=0, sticky="ew")

# Configure columns to expand equally
button_frame.grid_columnconfigure(0, weight=1, uniform="button")
button_frame.grid_columnconfigure(1, weight=1, uniform="button")
button_frame.grid_columnconfigure(2, weight=1, uniform="button")

# Add Preview and Generate buttons
preview_button = ttk.Button(button_frame, text="Preview", command=update_preview)
preview_button.grid(row=0, column=0, sticky="ew", padx=5)

generate_button = ttk.Button(button_frame, text="Generate", command=on_generate)
generate_button.grid(row=0, column=1, sticky="ew", padx=5)

# Rest to Default button
reset_button = ttk.Button(button_frame, text="Reset Default", command=reset_default)
reset_button.grid(row=0, column=2, sticky="ew", padx=5)


# Create a frame for the style display (below the buttons in the left section)
style_frame = tk.Frame(param_frame)
style_frame.grid(row=len(fields) + 6, column=0, columnspan=2, pady=10)

# Label to show the selected style value (now will display an image)
style_value_label = tk.Label(style_frame)
style_value_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Bind the update_style_label function to the combobox event
styles_combobox.bind("<<ComboboxSelected>>", update_style_label)

# Initialize the style display with the default selected style (usually "1")
root.after(100, update_style_label)


root.after(100, update_preview)

# Run the GUI
root.mainloop()
