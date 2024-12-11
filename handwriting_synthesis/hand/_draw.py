import numpy as np
import svgwrite
import cairosvg

from handwriting_synthesis import drawing

def _draw(strokes, lines, filename, stroke_colors=None, stroke_widths=None, page = None):
    stroke_colors = stroke_colors or ['black'] * len(lines)
    stroke_widths = stroke_widths or [2] * len(lines)

    line_height, total_lines_per_page, view_height, view_width, margin_left, margin_top, page_color, margin_color, line_color = page or [32, 24, 896, 632, -64, -96, "fff", "f00", "888"]


    # Initialize the SVG drawing
    dwg = svgwrite.Drawing(filename=filename)
    dwg.viewbox(width=view_width, height=view_height)
    dwg.add(dwg.rect(insert=(0, 0), size=(view_width, view_height), fill=page_color))


    # Draw fixed number of ruled lines
    for i in range(total_lines_per_page):
        y_position = line_height * (i + 1) - margin_top # Adjust as needed to align with text
        dwg.add(dwg.line(start=(0, y_position), end=(view_width, y_position), stroke=line_color, stroke_width=1))

    dwg.add(dwg.line(start=(-margin_left + line_height/2, 0), end=(-margin_left + line_height/2, view_height), stroke=margin_color, stroke_width=1))
    dwg.add(dwg.line(start=(-margin_left + line_height/2 - 5, 0), end=(-margin_left + line_height/2 - 5, view_height), stroke=margin_color, stroke_width=1))

    dwg.add(dwg.line(start=(0, -margin_top), end=(view_width, -margin_top), stroke=margin_color, stroke_width=1))
    dwg.add(dwg.line(start=(0, -margin_top - 5), end=(view_width, -margin_top - 5), stroke=margin_color, stroke_width=1))


    initial_coord = np.array([margin_left, margin_top - line_height/2])


    for i, (offsets, line, color, width) in enumerate(zip(strokes, lines, stroke_colors, stroke_widths)):
        # Stop drawing text if lines exceed the fixed page limit
        if i >= total_lines_per_page:
            break

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
