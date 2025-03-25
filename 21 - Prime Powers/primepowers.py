primes = [2]
last_checked = 2

def check_next():
    global last_checked
    last_checked += 1
    for p in primes:
        if last_checked % p == 0: return
    primes.append(last_checked)

def get_prime_powers(n):
    while n > last_checked: check_next()
    powers = []
    for p in primes:
        power = 0
        while n % p == 0:
            n //= p
            power += 1
        powers.append(power)
        if n == 1: break
    return powers

def mult_prime_powers(prime_powers):
    n = 1
    for i in range(len(prime_powers)):
        n *= primes[i] ** prime_powers[i]
    return n

# to use:
# from primepowers import get_prime_powers, primes