# for each point in space the closest point of a circle in the xy plane is (x, y) * R / √(x^2 + y^2)
# surface of a torus is fixed distance r from that point
# the simplified expresion turns out to be (√(x^2 + y^2) - R)^2 + z^2 = r^2

# vector algebra

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
vone = (1, 1, 1)

# torus raycast

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
        point = add(point, multiply(direction, 0.05))
        for i in range(30):
            sd, d = self.sd(point)
            cos = dotp(direction, normalise(d))
            if cos < 0 and sd > 2 * self.R:
                return None
            point = add(point, multiply(direction, sd))
        return point

# image ray tracing

resh = 80
resv = resh * 3 // 4
torus = Torus(1, 0.4)
light = normalise((1, 1, -1))
angles = (0, 0, 0)
rotation = (11, 17, -3)
pos = (-3.5, 0, 0)

def gen_image():
    global angles
    arr = [[None] * resv for i in range(resh)]
    for py in range(resh):
        for pz in range(resv):
            y, z = (py / resh * 2 - 1, (resv - pz * 2) / resh)
            intersection = torus.cast(rotate(pos, angles), rotate((1, y, z), angles))
            color = multiply(vone, 0.125)
            if intersection != None:
                l = -dotp(rotate(light, angles), torus.n(intersection))
                if torus.cast(intersection, rotate(sub(vzero, light), angles)) != None: l = 0
                color = multiply((1, 1, 1), max(l, 0.4))
            arr[py][pz] = color
    angles = add(angles, rotation)
    return arr

# image sequence draw and save

from PIL import Image

def draw_squence(n):
    for i in range(n):
        img = Image.new(mode="RGBA", size=(resh, resv))
        arr = gen_image()
        for x in range(len(arr)):
            for y in range(len(arr[x])):
                img.putpixel((x, y), vint(multiply(arr[x][y], 255)))
        # img.show()
        img.save(f"frames/frame{i}.png","PNG")

# console draw

from random import random
import time
import os
clear = lambda: os.system('clear')

def draw_console():
    arr = gen_image()
    out = ""
    for y in range(len(arr[0]) // 3):
        for x in range(len(arr) // 2):
            values = []
            for ax in range(2):
                for ay in range(3):
                    values.append(arr[x * 2 + ax][y * 3 + ay][0])
            var = 0
            pow = 1
            for i in range(len(values)):
                value = values[i]
                if value != 0 and ((x * 2 + y * 3 + i) % int(1 / value)) == 0:
                    var += pow
                pow <<= 1
            out += chr(0x2800 + var)
        out += "\n"
    print(out)

# main

while(True):
    # clear()
    draw_console()
    time.sleep(0.01)

# try with resh = 300
# draw_squence(24)