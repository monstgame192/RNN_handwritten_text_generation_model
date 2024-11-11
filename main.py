import numpy as np
from handwriting_synthesis import Hand

give_up = """Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you"""

lines = [
    "Rudraneel Dutta",
    "I'm winding down, I'm growing tired",
    "Seconds drift into the night",
    "The clock just ticks till my time expires",
]

if __name__ == '__main__':
    hand = Hand()

    lines = lines
    biases = [.75 for i in lines]
    styles = [7 for i in lines]

    hand.write(
        filename='img/result.svg',
        lines=lines,
        biases=biases,
        styles=styles,
    )
