import random, math
# euclidean method of finding gcd(a,b)
# may need replacing for large numbers
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % n

def dlog(x, order, base=10):
    # discrete log for modulus logarithms
    # base^y = x mod ord
    y = math.log(x,base)
    i = 1
    if int(y) == 0:
        y = math.log(x + i*order, base)
        i += 1

    while y % int(y) != 0:
        y = math.log(x + i*order, base)
        if y > order - 1:
            raise Exception("Discrete log error: discrete log of {} base {} does not exist with respect to {}".format(x,base,order))
        i += 1
    
    return int(y)

def isRoot(r, base):
    # 1. Tabular method too slow O(base) when checking to base/2
    '''table = []
    last = 0
    i = 2
    while i < base / 2:
        last = pow(r, i, base)
        if last in table:
            return False
        table.append(last)
        i += 1'''

    # 2. Log method even slower O(base*log(base))
    '''k = random.randint(2, base-2)
    return pow(r, random.randint(1, base-2)*(base-1), base) == 1 and dlog(pow(r, k, base), base, r) % (base - 1) == k'''
    
    # 3. BEST APPROACH: O(f + p1) where f is the number of prime factors and p1 is the second largest prime
    factors = prime_factors(base-1)
    for factor in factors:
        if pow(r, (base-1)/ factor, base) != 1:
            continue
        else:
            #print("Bad Factor:",factor)
            return False

    return True

def isPrime(n, certainty=5):
    # n is the integer in question, certainty is a parameter to repeat the Miller-Rabin test (reccommended 4 repetitions for 96.1% avoidance of strong psuedoprimes)
    if n <= 1:
        raise Exception("isPrime error: n must be positive and not 1")

    k = 0
    m = (n-1)/(2**k)
    while m % 2 == 0:
        k += 1
        m = (n-1)/(2**k)
    
    if k == 0:
        g, _, _ = egcd(2, n)
        #print("Common factor with {}: {}".format(2, g))
        return False

    flags = [False]*certainty

    for f in range(certainty):
        a = random.randint(2, n-1)
        b = [0]*k
        b[0] = pow(a, m, n)
        if b[0] == 1 or b[0] == (n-1):
            flags[f] = True
            continue

        for i in range(1, k):
            b[i] = pow(b[i-1], 2, n)
            if b[i] == 1:
                #g, _, _ = egcd(b[i-1]-1, n)
                #print("Common factor with {}: {}".format(b[i-1], g))
                flags[f] = False
                break
            elif b[i] == n-1:
                flags[f] = True
                break
        
        if b[k-1] != 0 and b[k-1] != 1:
            if b[k-1] != n-1:
                #g, _, _ = egcd(b[k-1]-1, n)
                #print("Common factor with {}: {}".format(b[k-1], g))
                flags[f] = False
            else:
                flags[f] = True
    
    if False in flags:
        return False
    else:
        return True

def nextPrime(n):
    return find_nearby_prime(n+1)

def find_nearby_prime(n):
    p = 0
    if n % 2 == 0:
        p = n + 1
    else:
        p = n

    while p < 2*n:
        #print("Testing Prime:",p)
        if isPrime(p):
            return p
        p = p + 2
    raise ValueError("number too big")

def find_large_prime(size=31):
    if size > 512:
        raise ValueError("Size given: {} (max size supported is 512)".format(size))
    p = random.randrange(10**(size - 1), 10**size - 1, 1)
    while not isPrime(p):
        p = random.randrange(10**(size - 1), 10**size - 1, 1)
    return p

def prime_factors(n):
    if n <= 1:
        return []
    factors = []
    i = n
    last = i
    prime = 2
    while i > 1:
        i %= prime
        if i == 0:
            g, _, _ = egcd(prime, last)
            while g == prime:
                last /= prime
                g, _, _ = egcd(prime, last)
            #print("Found factor:",prime)
            factors.append(prime)
            if isPrime(last):
                factors.append(last)
                break
        i = last
        prime = nextPrime(prime)

    return factors

def randroot(base, min=2, max=11):
    r = random.randint(min, max)
    i = 0
    #print("Checking root:",r)
    while not isRoot(r, base):
        r = random.randint(min, max)
        #print("Checking root:",r)
        i += 1
        if i == 2*(max - min + 1):
            raise Exception("RootError: no root for base {} in range {}-{}".format(base, min, max))
    return r