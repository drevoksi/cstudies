# Linear Feedback Shift Register function with the period of 2^127 - 1 (as state of 0 is excluded)
def LSFR():
    i = (1 << 127) | 1
    while(True):
        yield i & 1
        b = (i ^ (i >> 1) ^ (i >> 2) ^ (i >> 7)) & 1
        i = (i >> 1) | (b << 127)