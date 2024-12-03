import os
from handwriting_synthesis import Hand

def process_text(input_file, output_dir, alphabet, max_line_length, lines_per_page, biases, styles, stroke_widths, page):
    """
    Processes text from an input file, sanitizes, wraps, paginates it,
    and generates handwriting SVG files.

    Parameters:
        input_file (str): Path to the input text file.
        output_dir (str): Directory to save the generated SVG files.
        alphabet (list): Allowed characters for sanitization.
        max_line_length (int): Maximum length of each line.
        lines_per_page (int): Number of lines per page.
        biases (list): Bias values for handwriting style.
        styles (list): Style values for handwriting.
        stroke_widths (list): Stroke width values for handwriting.
    """
    # Read lines from the input file
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if line.strip()]

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


def main():
    # Initialize parameters
    input_file = 'input.txt'              # Input text file
    output_dir = 'img'                    # Directory for output SVG files
    alphabet = [
        '\x00', ' ', '!', '"', '#', "'", '(', ')', ',', '-', '.',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
        '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
        'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
        'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
        'y', 'z'
    ]

    max_line_length = 60                 # Maximum characters per line
    lines_per_page = 24                  # Lines per page
    biases = 0.95                        # Handwriting bias
    styles = 1                           # Handwriting style
    stroke_widths = 1                    # Stroke width for handwriting

    # Page parameters to be stored in page array
    line_height = 32
    total_lines_per_page = 24
    view_height = 896
    view_width = view_height * 0.707 # Ratio for a4 paper
    margin_left = -64
    margin_top = -96

    page = [line_height, total_lines_per_page, view_height, view_width, margin_left, margin_top]


    # Call the process_text function
    try:
        process_text(input_file, output_dir, alphabet, max_line_length, lines_per_page, biases, styles, stroke_widths, page)
    except FileNotFoundError as e:
        print(e)
        exit(1)


if __name__ == '__main__':
    main()
