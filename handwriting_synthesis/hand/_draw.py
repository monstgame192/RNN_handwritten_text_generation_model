import numpy as np
import svgwrite
import cairosvg

from handwriting_synthesis import drawing

def _draw(strokes, lines, filename, stroke_colors=None, stroke_widths=None):
    stroke_colors = stroke_colors or ['black'] * len(lines)
    stroke_widths = stroke_widths or [2] * len(lines)

    line_height = 32
    view_width = 1000
    view_height = line_height * (len(strokes) + 1)

    # Initialize the SVG drawing
    dwg = svgwrite.Drawing(filename=filename)
    dwg.viewbox(width=view_width, height=view_height)
    dwg.add(dwg.rect(insert=(0, 0), size=(view_width, view_height), fill='white'))

    # Draw ruled lines
    for i in range(len(strokes) + 1):
        y_position = line_height * (i + 1) - line_height / 2  # Adjust position to line up with text
        dwg.add(dwg.line(start=(0, y_position), end=(view_width, y_position), stroke='lightgray', stroke_width=1))

    # Starting position for text
    initial_coord = np.array([0, -(3 * line_height / 4)])
    for offsets, line, color, width in zip(strokes, lines, stroke_colors, stroke_widths):
        if not line:
            initial_coord[1] -= line_height
            continue

        # Convert offsets to coordinates and adjust them
        offsets[:, :2] *= 1
        strokes = drawing.offsets_to_coords(offsets)
        strokes = drawing.denoise(strokes)
        strokes[:, :2] = drawing.align(strokes[:, :2])
        strokes[:, 1] *= -1
        strokes[:, :2] -= strokes[:, :2].min() + initial_coord

        # Create the path for handwriting strokes
        prev_eos = 1.0
        p = "M{},{} ".format(0, 0)
        for x, y, eos in zip(*strokes.T):
            p += '{}{},{} '.format('M' if prev_eos == 1.0 else 'L', x, y)
            prev_eos = eos
        path = svgwrite.path.Path(p)
        path = path.stroke(color=color, width=width, linecap='round').fill("none")
        dwg.add(path)

        initial_coord[1] -= line_height

    # Save the SVG file and convert to PNG
    dwg.save()
    cairosvg.svg2png(url=filename, write_to=filename + '.png')
