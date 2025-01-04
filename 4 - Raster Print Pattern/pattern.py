# all media printed on paper is transferred onto it with tiny raster colour dots of different sizes
# this code attempts to replicate that pattern 

import math
floor = math.floor
ceil = math.ceil
sqrt = math.sqrt
from random import random

def sheet(w, h):
    return [[1] * h for i in range(w)]

sub = ((-0.25, -0.25), (0.25, -0.25), (-0.25, 0.25), (0.25, 0.25))
def draw_circle(tone, cx, cy, rsq):
    w = len(tone)
    h = len(tone[0])
    r = sqrt(rsq)
    for x in range(max(floor(cx - r), 0), min(ceil(cx + r + 1), w)):
        for y in range(max(floor(cy - r), 0), min(ceil(cy + r + 1), h)):
            m = 0
            for p in sub:
                dx = cx - x - p[0]
                dy = cy - y - p[1]
                dsq = dx * dx + dy * dy
                if dsq <= rsq: m += 1
            tone[x][y] -= m / len(sub)

def get_tone_pattern(tone, res):
    tw = len(tone)
    th = len(tone[0])
    w = res * tw
    h = res * th
    pattern = sheet(w, h)
    for tx in range(tw):
        for ty in range(th):
            cx = tx * res + res / 2
            cy = ty * res + res / 2
            t = tone[tx][ty]
            draw_circle(pattern, cx, cy, t * res * res / 2)
    return pattern
    
def get_img(tone_r, tone_g, tone_b):
    w = len(tone_r)
    h = len(tone_r[0])
    img = Image.new(mode="RGB", size=(w, h))
    for x in range(w):
        for y in range(h):
            img.putpixel((x, y), tuple(int(min(max(tone[x][y], 0), 1) * 255) for tone in (tone_r, tone_g, tone_b)))
    return img

tone = [[random() for y in range(100)] for x in range(100)]
tone_p = get_tone_pattern(tone, 10)
get_img(tone_p, tone_p, tone_p).show()