from handwriting_synthesis import Hand

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


lines = [
    "In the beginning, there was only a vast expanse of darkness, an endless void filled with possibilities yet untouched.",
    "As eons passed, stars began to form, galaxies spun into existence, and the universe slowly took shape, full of wonder and mystery.",
    "The Earth emerged as a small blue planet amidst the vastness of space, a cradle for life as we know it, and a home to countless creatures.",
    "Mountains rose from the Earth's crust, rivers carved through landscapes, and the seas teamed with life, each playing a role in the delicate balance of nature.",
    "Humanity appeared, bringing with it curiosity and intelligence, striving to understand its place among the stars and uncover the secrets of existence.",
    "Civilizations flourished, built upon the wisdom of those who came before, with stories, art, and knowledge passed down through generations.",
    "Technological advancements reshaped societies, connecting distant lands and bringing about rapid changes that transformed the human experience.",
    "With each new discovery, humanity's understanding of the cosmos grew, from the motion of planets to the composition of distant stars.",
    "The pursuit of science and exploration led to great achievements, from landing on the moon to exploring the depths of the ocean.",
    "Throughout history, individuals have sought meaning and purpose, pondering the mysteries of life, death, and the universe itself.",
    "Philosophers, poets, and thinkers left behind works that continue to inspire, questioning the nature of reality and the essence of the human soul.",
    "In times of struggle, humanity showed resilience, finding strength in unity and hope, rising above challenges to build a better future.",
    "Art, music, and culture blossomed, providing a reflection of society's joys, sorrows, and aspirations, immortalized in creations that transcend time.",
]

# Wrap lines to ensure no line exceeds 40 characters
wrapped_lines = wrap_lines(lines, max_length=60)

# Paginate wrapped lines into pages of 24 lines each
lines_per_page = 24
pages = paginate_lines(wrapped_lines, lines_per_page=lines_per_page)

if __name__ == '__main__':
    hand = Hand()

    for page_num, page_lines in enumerate(pages):
        # Set biases and styles for the current page
        biases = [0.75 for _ in page_lines]
        styles = [4 for _ in page_lines]
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
