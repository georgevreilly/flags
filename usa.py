#!/usr/bin/env python3

from PIL import Image, ImageDraw

import math
import os

def draw_star(width=500, multiplier=2):
    width *= multiplier
    height = width
    CX = CY = int(width / 2)
    star_radius = CX * 0.95

    def pt(x, y):
        return (round(CX + star_radius * x), round(CY - star_radius * y))

    im = Image.new("RGB", (width, height), "#F5E1D2")
    draw = ImageDraw.Draw(im)

    start_angle = 90
    outer_radius = 1.0
    inner_radius = outer_radius * math.sin(math.radians(18)) / math.sin(math.radians(54))
    prev = pt(0, 1)
    colors = ["red", "green", "blue", "black", "yellowgreen", "cyan", "magenta",
              "orange", "gray", "maroon", "indigo", "teal",]

    for i in range(1, 11):
        radius = inner_radius if i & 1 else outer_radius
        angle = (36 * i + start_angle) % 360
        rad = math.radians(angle)
        x, y = (radius * math.cos(rad), radius * math.sin(rad))
        sx, sy = pt(x, y)
        print(f"i={i:2}, a={angle:3}, r={radius:.3f}, x={x:6.3f}, y={y:6.3f}, sx={sx:3}, sy={sy:3}, c={colors[i]}")
        if prev:
            draw.line([*prev, sx, sy], fill=colors[i])
        prev = (sx, sy)

    # Quarters
    hx = inner_radius / math.tan(math.radians(36))
    draw.line([*pt(-hx, 0), *pt(hx, 0)], fill="crimson")
    draw.line([*pt(0, -inner_radius), *pt(0, outer_radius)], fill="chartreuse")

    im = im.resize((width // multiplier, height // multiplier), Image.ANTIALIAS)
    im.save("stars.png")    


draw_star()

