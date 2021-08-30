#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Tuple

from PIL import Image, ImageDraw  # type: ignore

import math
import os

STAR_INNER_RADIUS_RATIO = math.sin(math.radians(18)) / math.sin(math.radians(54))
STAR_SEGMENT_LENGTH = math.cos(math.radians(18)) - math.cos(math.radians(54))


def star_polygon() -> List[Tuple[float, float]]:
    start_angle = 90
    outer_radius = 1.0 / 2.0
    inner_radius = STAR_INNER_RADIUS_RATIO * outer_radius
    points = []
    print(f"star: outer={outer_radius:5.3f}, inner={inner_radius:5.3f}")

    for i in range(10):
        radius = inner_radius if i & 1 else outer_radius
        angle = (36 * i + start_angle) % 360
        rad = math.radians(angle)
        x, y = (radius * math.cos(rad), radius * math.sin(rad))
        sx, sy = 0.5 + x, 0.5 - y
        points.append((sx, sy))
        print(f"a={angle:3}, x={x:6.3f}, y={y:6.3f}, sx={sx:5.3f}, sy={sy:5.3f}")

    return points


def walk_polygon() -> list[tuple[float, float]]:
    outer_radius = 1.0 / 2.0
    x, y = 0, outer_radius
    angle = 270 - 18
    length = STAR_SEGMENT_LENGTH
    points = []
    print(f"walk: outer={outer_radius:5.3f}, length={length:5.3f}")

    for i in range(5):
        for adj in (-72, 144):
            sx, sy = 0.5 + x, 0.5 - y
            points.append((sx, sy))
            print(f"a={angle:3}, x={x:6.3f}, y={y:6.3f}, sx={sx:5.3f}, sy={sy:5.3f}")
            rad = math.radians(angle)
            x += length * math.cos(rad)
            y += length * math.sin(rad)
            angle = (angle + adj) % 360

    return points


def draw_star(
        diameter: float = 1.0,
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
    star_radius = image_width

    def pt(x, y):
        assert 0.0 <= x <= 1.0, str(x)
        assert 0.0 <= y <= 1.0, str(y)
        px, py = round(star_radius * x), round(star_radius * y)
        return (px, py)

    im = Image.new("RGB", (image_width, image_height), color=background_color)
    draw = ImageDraw.Draw(im)

    colors = ["Red", "Green", "Blue", "Black", "YellowGreen", "Cyan", "Magenta",
              "Orange", "Gray", "Maroon", "Indigo", "Teal",]

    outer_radius = 1.0 / 2.0
    inner_radius = STAR_INNER_RADIUS_RATIO * outer_radius
    points = star_polygon()

    if fill_polygon:
        polygon = [pt(x, y) for x,y in points]
        draw.polygon(polygon, outline="Red", fill="White")
        # print(polygon)
    else:
        px, py = pt(*points[-1])
        for i, (x, y) in enumerate(points):
            sx, sy = pt(x, y)
            # print(f"i={i:2}, x={x:6.3f}, y={y:6.3f}, sx={sx:3}, sy={sy:3}, c={colors[i]}")
            draw.line([px, py, sx, sy], width=line_width, fill=colors[i])
            px, py = sx, sy

    if quarters:
        # hx = where the y=0 line intercepts the right side of the star
        hx = inner_radius / math.tan(math.radians(36))
        cx = cy = 0.5 # center is translated to (0.5, 0.5)
        horiz = [*pt(cx - hx, cy), *pt(cx + hx, cy)]
        vert = [*pt(cx, cy + inner_radius), *pt(cx, cy - outer_radius)]
        draw.line(horiz, width=line_width, fill="CornflowerBlue")
        draw.line(vert, width=line_width, fill="SeaGreen")

    draw.ellipse((0, 0, image_width, image_height), fill=None, outline="Teal")

    # Scale down to smooth image
    if multiplier > 1:
        im = im.resize((image_width // multiplier, image_height // multiplier), Image.ANTIALIAS)

    if filename:
        im.save(filename)    


if __name__ == "__main__":
    draw_star(fill_polygon=False, line_width=3)
