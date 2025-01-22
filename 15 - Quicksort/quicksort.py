# recursive quicksort splits a list into two with values smaller and larger than a randomly-chosen pivot
# recursively-sorted lists are concatenated in sorting order with the pivot value in-between
def quicksort_r(l):
    if len(l) < 2: return l
    if len(l) == 2: return l if l[0] <= l[1] else [l[1], l[0]]
    pivot = l.pop() # better to take from the middle
    smaller = [x for x in l if x <= pivot] # better to distribute between lists from one loop
    larger = [x for x in l if x > pivot]   # may also use filter(lambda condition, list)
    return quicksort_r(smaller) + [pivot] + quicksort_r(larger)

from random import randrange

def shuffle(l):
    ordered = list(l)
    result = [None] * len(ordered)
    for i in range(len(result)):
        result[i] = ordered.pop(randrange(len(ordered)))
    return result

from time import time

l = shuffle(range(500))

time_s = time()
sorted_l = quicksort_r(l)
time_e = time()

print(sorted_l)
print(f"Completed in {time_e - time_s}s")