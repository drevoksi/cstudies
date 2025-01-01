def sqrt(n):
    l = 0
    r = max(n, 1)
    a = -1
    p = -2
    while a != p:
        p = a
        a = (l + r) / 2
        if a * a > n:
            r = a
        else: 
            l = a
    return a

print(sqrt(0.0256))

