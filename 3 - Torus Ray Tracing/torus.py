# for each point in space the closest point of a circle in the xy plane is (x, y) * R / √(x^2 + y^2)
# surface of a torus is fixed distance r from that point
# the simplified expresion turns out to be (√(x^2 + y^2) - R)^2 + z^2 = r^2

import math

def magnitude(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
def multiply(v, a):
    return (v[0] * a, v[1] * a, v[2] * a)
def normalise(v):
    if v == vzero: return v
    return multiply(v, 1 / magnitude(v))
def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2])
def sub(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2])
def dotp(v1, v2):
    return (v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2])
def vint(v):
    return tuple(int(c) for c in v)
def rotate(v, euler_angles):
    x, y, z = (math.radians(c) for c in euler_angles)
    c = math.cos
    s = math.sin
    return (
        (c(z) * c(y)) * v[0] + (c(z) * s(y) * s(x) - s(z) * c(x)) * v[1] + (c(z) * s(y) * c(x) + s(z) * s(x)) * v[2],
        (s(z) * c(y)) * v[0] + (s(z) * s(y) * s(x) + c(z) * c(x)) * v[1] + (s(z) * s(y) * c(x) - c(z) * s(x)) * v[2],
        (-s(y)) * v[0] + (c(y) * s(x)) * v[1] + (c(y) * c(x)) * v[2]
    )
vzero = (0, 0, 0)

class Torus:
    def __init__(self, R, r):
        self.R = R
        self.r = r
    def d(self, point):
        c = multiply(normalise((point[0], point[1], 0)), self.R)
        return sub(c, point)
    def sd(self, point):
        direction = self.d(point)
        return (magnitude(direction) - self.r, direction)
    def n(self, point):
        return normalise(multiply(self.d(point), -1))
    def cast(self, point, direction):
        direction = normalise(direction)
        for i in range(20):
            sd, d = self.sd(point)
            if (dotp(d, direction) < 0 or sd < 0) and dotp(direction, sub(vzero, point)) < 0:
                return None
            if sd > 0.0001:
                point = add(point, multiply(direction, sd))
        return point

# ray trace the image

from PIL import Image

resh = 300
resv = resh * 3 // 4
torus = Torus(1, 0.4)
light = (1, 1, -1)
angles = (0, 0, 0)
pos = (-6, 0, 0)
rotation = (26, 39, -7)

for i in range(360 // 26):
    img = Image.new(mode="RGBA", size=(resh, resv))
    for py in range(resh):
        for pz in range(resv):
            y, z = (py / resh * 2 - 1, (resv - pz * 2) / resh)
            intersection = torus.cast(rotate(pos, angles), rotate((1, y, z), angles))
            color = (45, 45, 45)
            if intersection != None:
                l = -dotp(rotate(light, angles), torus.n(intersection))
                int2 = torus.cast(intersection, rotate(sub(vzero, light), angles))
                if int2 != None and magnitude(sub(intersection, int2)) > 0.1: l = -4
                color = multiply((255, 255, 255), max(l, 0.1))
                if l == -4: color = (255, 0, 0)
            img.putpixel((py, pz), vint(color))
    # img.show()
    img.save(f"frames/frame{i}.png","PNG")
    angles = add(angles, rotation)