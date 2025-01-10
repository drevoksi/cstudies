from PIL import Image

def get_img(arr):
    w = len(arr)
    h = len(arr[0])
    img = Image.new(mode="RGB", size=(w, h))
    for x in range(w):
        for y in range(h):
            c = arr[x][y]
            col = int(255 * c)
            img.putpixel((x, y), (col, col, col))
    return img

import math

# (a + bi) * (c + di) = (ac - bd) + i(ad + bc)
def mult(a, b, c, d):
    return (a * c - b * d, a * d + b * c)

def sq(a, b):
    return (a * a - b * b, a * b * 2)

def mandelbrot(a, b, n):
    c = 0
    d = 0
    for i in range(n):
        # c, d = sq(c, d) + (a, b)
        # don't forget to update the two values simultaneously - don't use the new value of c in d
        c, d = (c * c - d * d + a, c * d * 2 + b)
        if c * c + d * d > 4:
            return i / n
    return 0

def mandelbrot_set(centre, size, resolution, n):
    c, d = centre
    k, l = size
    w, h = resolution
    arr = [[0] * h for x in range(w)]
    for x in range(w):
        for y in range(h):
            a = (x / w - 0.5) * k + c
            b = (y / h - 0.5) * l + d
            arr[x][y] = mandelbrot(a, b, n)
    return arr

centre = (-0.667, 0)
size = (2.5, 2.5)
resolution = (400, 400)
n = 80
arr = mandelbrot_set(centre, size, resolution, n)
img = get_img(arr)
img.show()