# this is a very simple but incredible trick my friend taught me
a = 1378
b = 415

a ^= b
b ^= a
a ^= b

print(a, b) # prints '415 1378'

# two variables can be swapped without declaration of a third variable
# it may not be more efficient, but it certainly is very impressive