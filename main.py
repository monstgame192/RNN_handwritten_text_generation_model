from handwriting_synthesis import Hand

def wrap_lines(lines, max_length=50):
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


# Original text lines
lines = [
    "This is the first paragraph, and it contains several long sentences, which should be split into multiple lines, because it exceeds fifty characters, and we want to see how the wrapping happens in practice.",
    "The second paragraph is just as long, with a lot of words that go beyond the fifty character limit. Here we will check if the wrapping works correctly, making sure no line exceeds the specified maximum length.",
    "Finally, this is the third paragraph. It has long text as well, and will be wrapped accordingly, so we can check if everything works as expected, wrapping lines at appropriate points, without cutting off any words in the middle."
]



# Wrap lines to ensure no line exceeds 50 characters
wrapped_lines = wrap_lines(lines, max_length=50)

if __name__ == '__main__':
    hand = Hand()

    # Set biases and styles
    biases = [.75 for _ in wrapped_lines]
    styles = [7 for _ in wrapped_lines]

    # Generate the handwriting SVG
    hand.write(
        filename='img/result.svg',
        lines=wrapped_lines,
        biases=biases,
        styles=styles,
    )