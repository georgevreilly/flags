#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Tuple

import svgwrite as sw

import math
import os
import sys

SCRIPT_DIR = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
print(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from flags.usa import star_polygon, star_inner_radius, star_outer_radius


COLORS = ["Red", "Green", "Blue", "Black", "YellowGreen", "Cyan", "Magenta",
          "Orange", "Gray", "Maroon", "Indigo", "Teal",]

def diagram(
        image_width: int = 500,
        multiplier: int = 2,
        line_width: int = 0,
        filename: str = "star.svg",
    ):
    image_width *= multiplier
    image_height = image_width
    CX = CY = int(image_width / 2)
    outer_radius = CX * 0.95
    inner_radius = star_inner_radius(outer_radius * 2)
    ratio = inner_radius / outer_radius

    def pt(x, y, r=outer_radius, cx=0.0, cy=0.0):
        assert -0.5 <= x - cx <= +0.5, str(x)
        assert -0.5 <= y - cy <= +0.5, str(y)
        px = round(CX + r * x)
        py = round(CY - r * y) # subtract because image origin is at top-left
        return (px, py)

    dwg = sw.Drawing(filename=filename, size=(image_width, image_height), debug=True)

    star = star_polygon()
    scaled_star = [pt(x, y) for x, y in star_polygon()]
    dwg.add(dwg.polygon(scaled_star).fill("none").stroke("red", width=2))

    outer_pentagon = scaled_star[0::2]
    inner_pentagon = scaled_star[1::2]
    dwg.add(dwg.polygon(inner_pentagon).fill("none").stroke("blue").dasharray([3, 3]))
    dwg.add(dwg.polygon(outer_pentagon).fill("none").stroke("gray").dasharray([3, 3]))

    dwg.add(dwg.circle(center=(CX, CY), r=outer_radius/2).fill("none").stroke("green").dasharray([2, 3]))
    dwg.add(dwg.circle(center=(CX, CY), r=inner_radius/2).fill("none").stroke("purple").dasharray([2, 3]))

    # hx = where the y=0 line intercepts the right side of the star
    hx = (ratio / math.tan(math.radians(36))) * outer_radius / 2
    x1, x2 = -hx + CX, hx + CX
    y1, y2 = CY + inner_radius / 2, CY - outer_radius / 2
    dwg.add(dwg.line((x1, CY), (x2, CY)).stroke("cornflowerblue", width=2).dasharray([4, 4]))
    dwg.add(dwg.line((CX, y1), (CX, y2)).stroke("aqua", width=2).dasharray([4, 4]))

    dwg.add(dwg.text("a", pt(*star[0], 1.05 * outer_radius), text_anchor="middle"))
    dwg.add(dwg.text("b", pt(*star[-1], 0.75 * outer_radius)))
    dwg.add(dwg.text("c", pt(*star[-2], 1.05 * outer_radius)))

    dwg.save(pretty=True)


if __name__ == "__main__":
    diagram()
