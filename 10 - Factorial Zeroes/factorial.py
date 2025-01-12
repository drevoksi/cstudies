# ... to take it further: attempt to come up with a formula of n

# to find the number of zeroes in a large factorial, calculate the number of its factors of 10
# each such factor is product of the primes 2 and 5
# so the number of trailing zeroes is the number, or power, of the prime factor pair 2, 5 of the factorial

# factorial of n is the product of the first n natural numbers
# when multiplying numbers together, the arrays of prime factors are 'added' together
# so, to find the number of n factorial's prime factors, 
# ... it is sufficient to find the number of such prime factors in the first n natural numbers

# add the number of multiples of p's power before n
# multiples of greater powers are also divisible by prior powers
# thus, each new power only gives one new factor per its multiple
def factors_before(p, n):
    count = 0
    power = p
    while power <= n:
        count += n // power
        power *= p
    return count

n = 100

number_of_2s = factors_before(2, n)
number_of_5s = factors_before(5, n)

# there are always more smaller factors than greater factors
# for n in range(100):
#     print(pfactors_before(2, n), pfactors_before(3, n), pfactors_before(4, n), pfactors_before(5, n))

# ... so for this problem, the bottleneck of the # of pairs of prime factors is the # of factors of 5
# ... the number of trailing zeroes is, therefore, the calculated number_of_5s

print(f'Number of trailing zeroes: {number_of_5s}')

# validating is pretty easy in python as large integers are managed automatically

def factorial(n):
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product

print(factorial(n)) # 24 for 100! ✅

# and to validate:

def validate(n):
    num = factors_before(5, n)
    fstr = str(factorial(n))
    trail = 0
    while fstr[- 1 - trail] == '0':
        trail += 1
    valid = trail == num
    print('VALID' if valid else 'NOT VALID')

# for n in range(0, 150):
#     validate(n)