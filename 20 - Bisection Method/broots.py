def sign(a):
    if a > 0: return 1
    elif a < 0: return -1
    else: return 0

# this method finds a root of f at the interval [a, b] where the function changes its sign
def interval(a, b, f):
    y_a = f(a)
    y_b = f(b)
    if y_a == 0: return y_a
    if y_b == 0: return y_b
    x = (a + b) / 2
    y = f(x)
    if sign(y_a) == sign(y_b):
        print("Same sign interval")
        return None
    if y == 0 or x == a or x == b: return x             # found root or interval didn't change
    if sign(y) == sign(y_a): return interval(x, b, f)
    else:                    return interval(a, x, f)
    
import math

print(interval(3, 4, math.sin)) # gives pi