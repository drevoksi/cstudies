import math

def f(x):
    return x * x + 3 * x + 6

# normal integral, with samples every d of the interval
def integral(f, a, b, d = 0.001):
    s = 0
    x = a
    y_0 = f(x)
    while x < b:
        x += d
        y_1 = f(x)
        s += d * (y_0 + y_1) / 2
        y_0 = y_1
    return s

# sample integral, with fixed sample size for any interval
def integral_s(f, a, b, n = 10000):
    s = 0
    x = a
    x_0 = x
    y_0 = f(x)
    for i in range(n):
        x = a + (b - a) * i / n
        y_1 = f(x)
        s += (x - x_0) * (y_0 + y_1) / 2
        x_0 = x
        y_0 = y_1
    return s

print(integral(math.sin, 0, math.pi)) # int(sinx, 0, pi) = [-cosx](0, pi) = -cos(pi) - (-cos(0)) = 1 + 1 = 2
