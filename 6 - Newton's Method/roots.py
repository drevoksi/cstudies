import math
from random import random

# define any continious function
def f(x):
    return x * x * x - 4 * x * x + 2 * x + 3
def g(x):
    return -x * x + 2 * x

# Euler's method with arbitrary-chosen dx
def find_root(f, x, n):
    dx = 0.0000001
    for i in range(n):
        y = f(x)
        if y == 0:
            break
        dy = f(x + dx) - y
        if dy == 0:
            x += dx
            continue
        x -= y * dx / dy
    return x

# Euler's method with dx based on the minimal precision-difference
def find_root_d(f, x0 = random(), n = 20):
    for i in range(n):
        y0 = f(x0)
        if y0 == 0:
            break
        dx = (math.nextafter(x0, float('inf')) - x0) * 10
        x1 = x0 + dx
        dy = f(x1) - y0
        if dy == 0:
            x0 += random() - 0.5
            continue
        x0 -= y0 * dx / dy
    return x0

print(find_root_d(g, 1, 20))