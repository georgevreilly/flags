#!/usr/bin/env python3

from __future__ import annotations

from typing import List, Tuple

from PIL import Image, ImageDraw  # type: ignore

import math
import os

def star_inner_radius(outer_radius: float = 0.5) -> float:
    return outer_radius * math.sin(math.radians(18)) / math.sin(math.radians(54))


def star_polygon(outer_radius: float = 0.5) -> List[Tuple[float, float]]:
    start_angle = 90
    inner_radius = star_inner_radius(outer_radius)
    points = [(0.0, outer_radius)]

    for i in range(1, 11):
        radius = inner_radius if i & 1 else outer_radius
        angle = (36 * i + start_angle) % 360
        rad = math.radians(angle)
        x, y = (radius * math.cos(rad), radius * math.sin(rad))
        points.append((x, y))

    return points


def draw_star(width=500, multiplier=2, line_width=0, separate_edges=True, quarters=True, diameter=1.0):
    width *= multiplier
    height = width
    CX = CY = int(width / 2)
    star_radius = 2.0 * CX * 0.95

    def pt(x, y):
        return (round(CX + star_radius * x), round(CY - star_radius * y))

    im = Image.new("RGB", (width, height), "#F5E1D2")
    draw = ImageDraw.Draw(im)

    colors = ["red", "green", "blue", "black", "yellowgreen", "cyan", "magenta",
              "orange", "gray", "maroon", "indigo", "teal",]

    outer_radius = diameter / 2
    inner_radius = star_inner_radius(outer_radius)

    if separate_edges:
        px = py = None
        for i, (x, y) in enumerate(star_polygon()):
            sx, sy = pt(x, y)
            print(f"i={i:2}, x={x:6.3f}, y={y:6.3f}, sx={sx:3}, sy={sy:3}, c={colors[i]}")
            if px is not None:
                draw.line([px, py, sx, sy], width=line_width, fill=colors[i])
            px, py = (sx, sy)
    else:
        polygon = [pt(x, y) for x,y in star_polygon()[1:]]
        print(polygon)
        draw.polygon(polygon, outline="black", fill="white")

    if quarters:
        hx = inner_radius / math.tan(math.radians(36))
        draw.line([*pt(-hx, 0), *pt(hx, 0)], fill="crimson")
        draw.line([*pt(0, -inner_radius), *pt(0, outer_radius)], fill="seagreen")

    im = im.resize((width // multiplier, height // multiplier), Image.ANTIALIAS)
    im.save("stars.png")    


draw_star(line_width=3, separate_edges=False)
