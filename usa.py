#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Tuple

from PIL import Image, ImageDraw  # type: ignore

import math
import os

def star_outer_radius(diameter: float = 1.0) -> float:
    return (diameter / 2)


def star_inner_radius(diameter: float = 1.0) -> float:
    return star_outer_radius(diameter) * math.sin(math.radians(18)) / math.sin(math.radians(54))


def star_polygon(diameter: float = 1.0, cx: float = 0.0, cy: float = 0.0) -> List[Tuple[float, float]]:
    start_angle = 90
    outer_radius = star_outer_radius(diameter)
    inner_radius = star_inner_radius(diameter)
    points = []

    for i in range(10):
        radius = inner_radius if i & 1 else outer_radius
        angle = (36 * i + start_angle) % 360
        rad = math.radians(angle)
        x, y = (cx + radius * math.cos(rad), cy + radius * math.sin(rad))
        points.append((x, y))

    return points


def draw_star(
        diameter: float = 1.0,
        cx: float = 0.0,
        cy: float = 0.0,
        fill_polygon: bool = True,
        image_width: int = 500,
        multiplier: int = 2,
        line_width: int = 0,
        quarters: bool = True,
        filename: str = "stars.png",
        background_color: str = "#F5E1D2",
    ):
    image_width *= multiplier
    image_height = image_width
    CX = CY = int(image_width / 2)
    star_radius = 2.0 * CX * 0.95

    def pt(x, y):
        assert -0.5 <= x - cx <= +0.5
        assert -0.5 <= y - cy <= +0.5
        px = round(CX + star_radius * x)
        py = round(CY - star_radius * y) # subtract because image origin is at top-left
        return (px, py)

    im = Image.new("RGB", (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(im)

    colors = ["Red", "Green", "Blue", "Black", "YellowGreen", "Cyan", "Magenta",
              "Orange", "Gray", "Maroon", "Indigo", "Teal",]

    outer_radius = star_outer_radius(diameter)
    inner_radius = star_inner_radius(diameter)
    points = star_polygon(diameter, cx, cy)

    if fill_polygon:
        polygon = [pt(x, y) for x,y in points]
        draw.polygon(polygon, outline="Red", fill="White")
        print(polygon)
    else:
        for i, (x, y) in enumerate(points):
            sx, sy = pt(x, y)
            p = i - 1 if i > 0 else len(points) - 1
            px, py = pt(*points[p])
            print(f"i={i:2}, x={x:6.3f}, y={y:6.3f}, sx={sx:3}, sy={sy:3}, c={colors[i]}")
            draw.line([px, py, sx, sy], width=line_width, fill=colors[i])

    if quarters:
        # hx = where the y=0 line intercepts the right side of the star
        hx = inner_radius / math.tan(math.radians(36))
        draw.line([*pt(-hx, 0), *pt(hx, 0)], width=line_width, fill="CornflowerBlue")
        draw.line([*pt(0, -inner_radius), *pt(0, outer_radius)], width=line_width, fill="SeaGreen")

    # Scale down to smooth image
    if multiplier > 1:
        im = im.resize((image_width // multiplier, image_height // multiplier), Image.ANTIALIAS)

    if filename:
        im.save(filename)    


if __name__ == "__main__":
    draw_star(fill_polygon=True, line_width=3)
