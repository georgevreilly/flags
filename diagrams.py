#!/usr/bin/env python3

from __future__ import annotations

import svgwrite as sw

import math
import os
import sys

SCRIPT_DIR = os.path.normpath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, SCRIPT_DIR)

from flags.usa import star_polygon, STAR_INNER_RADIUS_RATIO, walk_polygon


def svg_diagram(
        image_width: int = 500,
        filename: str = "star.svg",
    ):

    X_OFS, Y_OFS = 150, 180
    image_height = image_width
    CX, CY = X_OFS + image_width // 2, Y_OFS + image_height // 2
    outer_radius = 0.9 * image_width // 2
    inner_radius = outer_radius * STAR_INNER_RADIUS_RATIO

    def pt(x, y, r=outer_radius, cx=0.0, cy=0.0):
        assert 0.0 <= x <= 1.0, str(x)
        assert 0.0 <= y <= 1.0, str(y)
        px, py = CX + round(2 * r * (x-0.5)), CY + round(2 * r * (y-0.5))
        return (px, py)

    dwg = sw.Drawing(filename=filename, size=(image_width + X_OFS, image_height + Y_OFS), debug=True)
    dwg.add(dwg.rect((10, 10), (X_OFS-10, Y_OFS-10), fill='grey'))
    dwg.add(dwg.rect((X_OFS, Y_OFS), (image_width, image_height), fill='pink'))

    star = star_polygon()
    # star = walk_polygon()
    scaled_star = [pt(x, y) for x, y in star]
    dwg.add(dwg.polygon(scaled_star).fill("none").stroke("red", width=2))

    outer_pentagon = scaled_star[0::2]
    inner_pentagon = scaled_star[1::2]
    dwg.add(dwg.polygon(inner_pentagon).fill("none").stroke("blue").dasharray([3, 3]))
    dwg.add(dwg.polygon(outer_pentagon).fill("none").stroke("gray").dasharray([3, 3]))

    dwg.add(dwg.circle(center=(CX, CY), r=outer_radius).fill("none").stroke("green").dasharray([2, 3]))
    dwg.add(dwg.circle(center=(CX, CY), r=inner_radius).fill("none").stroke("purple").dasharray([2, 3]))

    # hx = where the y=0 line intercepts the right side of the star
    hx = (STAR_INNER_RADIUS_RATIO / math.tan(math.radians(36))) * outer_radius
    x1, x2 = -hx + CX, hx + CX
    y1, y2 = CY + inner_radius, CY - outer_radius
    dwg.add(dwg.line((x1, CY), (x2, CY)).stroke("cornflowerblue", width=2).dasharray([4, 4]))
    dwg.add(dwg.line((CX, y1), (CX, y2)).stroke("aqua", width=2).dasharray([4, 4]))

    dwg.add(dwg.text("a", pt(*star[0], 1.05 * outer_radius), text_anchor="middle"))
    dwg.add(dwg.text("b", pt(*star[-1], 0.75 * outer_radius)))
    dwg.add(dwg.text("c", pt(*star[-2], 1.05 * outer_radius)))

    dwg.save(pretty=True)


if __name__ == "__main__":
    svg_diagram()
