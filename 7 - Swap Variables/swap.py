# this is a very simple but incredible trick my friend taught me
a = 1378
b = 415

a ^= b
b ^= a
a ^= b

print(a, b) # prints '415 1378'

# two variables can be swapped without declaration of a third variable
# it may not be more efficient, but it certainly is very impressive

# another swap of integers in a similar manner uses addition and subtraction:
#   x = x + y
#   y = x - y   (y is still y, so (x + y) - y = x)
#   x = x - y   (because y = x, it's (x + y) - x = y)

# xor version works in a similar way; though it is commutative (x ^ y = y ^ x)
# the property it takes advantage of is that a ^ b ^ b = a
#   x = x ^ y
#   y = y ^ x   ((x ^ y) ^ y = x)
#   x = x ^ y   ((x ^ y) ^ x = y ^ x ^ x = y)