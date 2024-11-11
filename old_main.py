from handwriting_synthesis import Hand

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
