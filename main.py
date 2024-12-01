from handwriting_synthesis import Hand
import os

def read_lines_from_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines if line.strip()]


alphabet = [
    '\x00', ' ', '!', '"', '#', "'", '(', ')', ',', '-', '.',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';',
    '?', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
    'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z'
]


def sanitize_input(text, allowed_chars):
    sanitized_text = ''.join(char if char in allowed_chars else ' ' for char in text)
    return sanitized_text




def wrap_lines(lines, max_length=60):
    wrapped_lines = []
    for line in lines:
        words = line.split()
        current_line = ""
        
        for word in words:
            # Check if adding the next word would exceed the max_length
            if len(current_line) + len(word) + 1 > max_length:
                wrapped_lines.append(current_line.strip())
                current_line = word
            else:
                current_line += " " + word
        
        # Append the last line
        if current_line:
            wrapped_lines.append(current_line.strip())
    
    return wrapped_lines

def paginate_lines(wrapped_lines, lines_per_page=24):
    # Split wrapped lines into pages with fixed lines per page
    return [wrapped_lines[i:i + lines_per_page] for i in range(0, len(wrapped_lines), lines_per_page)]

if __name__ == '__main__':
    input_file = 'input.txt'  # Replace with your text file name

    # Read lines from the text file
    try:
        lines = read_lines_from_file(input_file)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Sanitize each line
    sanitized_lines = [sanitize_input(line, alphabet) for line in lines]

    # Wrap sanitized lines to ensure no line exceeds 40 characters
    wrapped_lines = wrap_lines(sanitized_lines, max_length=60)

    # Paginate wrapped lines into pages of 24 lines each
    lines_per_page = 24
    pages = paginate_lines(wrapped_lines, lines_per_page=lines_per_page)

    hand = Hand()

    for page_num, page_lines in enumerate(pages):
        # Set biases and styles for the current page
        biases = [0.95 for _ in page_lines]
        styles = [1 for _ in page_lines]
        stroke_widths = [1 for _ in page_lines]

        # Generate the handwriting SVG for each page
        filename = f'img/result_page_{page_num + 1}.svg'
        hand.write(
            filename=filename,
            lines=page_lines,
            biases=biases,
            styles=styles,
            stroke_widths=stroke_widths,
        )
