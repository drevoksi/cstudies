# a complete binary tree data structure, where a parent is always smaller than its children
# insert and pop are both O(log(n))
class MinHeap:
    def __init__(self, size = 1):
        self.list = [None]
        self.size = 1
        while self.size < size:
            self.double()
        self.length = 0
    
    def double(self):
        self.list.extend(None for i in range(self.size))
        self.size <<= 1
    def swap(self, i_0, i_1):
        swap = self.list[i_0]
        self.list[i_0] = self.list[i_1]
        self.list[i_1] = swap
    
    def left(self, i):
        return (i << 1) + 1
    def right(self, i):
        return (i << 1) + 2
    def child(self, i):
        return (i - 1) >> 1

    # insert the element at the end of the array, and swap up the tree while it's smaller than its parent
    def insert(self, val):
        if self.size == self.length:
            self.double()
        i = self.length
        self.list[i] = val
        self.length += 1
        child = self.child(i)
        while child >= 0 and self.list[child] > val:
            self.swap(child, i)
            i = child
            child = self.child(child)
    # swap the first element with the last one and remove the last element
    # now start with the new first element: if it is bigger than the smaller parent, swap them; continue until it isn't or if there's no parents
    def pop(self):
        element = self.list[0]
        self.length -= 1
        self.swap(0, self.length)
        self.list[self.length] = None
        i = 0
        while True:
            left = self.left(i)
            right = self.right(i)
            c_el = self.list[i]
            l_el = self.list[left] if left < self.length else None
            r_el = self.list[right] if right < self.length else None
            min_el = l_el if r_el == None else r_el if l_el == None else min(l_el, r_el)
            min_i = left if l_el == min_el else right
            if min_el != None and c_el > min_el:
                self.swap(i, min_i)
                i = min_i
            else: break
        return element
    def peek(self):
        return self.list[0]

    def write(self):
        n = 0
        while self.size != 0:
            if self.size & (1 << n) != 0: break
            n += 1
        for i in range(n):
            o = (1 << (i + 1)) - 2
            print(i, self.list[self.child(o) + 1 : o + 1])

import random

min_heap = MinHeap()
for i in range(32):
    min_heap.insert(i)
while min_heap.length != 0:
    print(min_heap.pop())