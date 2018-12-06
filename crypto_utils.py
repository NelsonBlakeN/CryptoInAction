import random, math, time

expansion = [31, 0,  1,  2,  3,  4,
             3,  4,  5,  6,  7,  8,
             7,  8,  9,  10, 11, 12,
             11, 12, 13, 14, 15, 16,
             15, 16, 17, 18, 19, 20,
             19, 20, 21, 22, 23, 24,
             23, 24, 25, 26, 27, 28,
             27, 28, 29, 30, 31, 0]

sbox = [
    [[14, 4,  13, 1, 2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0, 7],
     [0,  15, 7,  4, 14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3, 8],
     [4,  1,  14, 8, 13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5, 0],
     [15, 12, 8,  2, 4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6, 13]],

    [[15, 1,  8,  14, 6,  11, 3,  4,  9,  7, 2,  13, 12, 0, 5,  10],
     [3,  13, 4,  7,  15, 2,  8,  14, 12, 0, 1,  10, 6,  9, 11, 5],
     [0,  14, 7,  11, 10, 4,  13, 1,  5,  8, 12, 6,  9,  3, 2,  15],
     [13, 8,  10, 1,  3,  15, 4,  2,  11, 6, 7,  12, 0,  5, 14, 9]],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]
]

mangler_perm = [15, 6,  19, 20,
                28, 11, 27, 16,
                0,  14, 22, 25,
                4,  17, 30, 9,
                1,  7,  23, 13,
                31, 26, 2,  8,
                18, 12, 29, 5,
                21, 10, 3,  24]

# euclidean method of finding gcd(a,b)
# may need replacing for large numbers
def egcd(a, b):
    x0 = xn = y1 = 1
    y0 = yn = x1 = f = 0
    rem = a % b
    while rem > 0:
        f = a // b
        xn = x0 - f*x1
        yn = y0 - f*y1

        x0 = x1
        y0 = y1
        x1 = xn
        y1 = yn
        a = b
        b = rem
        rem = a % b

    return b, xn, yn

def modinv(a, n):
    g, x, _ = egcd(a, n)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % n

def dlog(x, order, base=10, limit=None):
    '''discrete log for modulus logarithms base^y = x mod order'''
    ''' bad approach O(k) where base^y = x + k*order
    y = math.log(x,base)
    i = 1
    if int(y) == 0:
        y = math.log(x + i*order, base)
        i += 1

    while y % int(y) != 0:
        y = math.log(x + i*order, base)
        #print(y, i)
        #time.sleep(1)
        if y > order - 1:
            raise Exception("Discrete Log error: discrete log of {} base {} does not exist with respect to {}".format(x,base,order))
        i += 1
        if i > 1000:
            return int(math.log(x + (10**10)*order, base)+1)

    return int(y)'''
    base_inv = modinv(base, order)
    N = int(math.ceil(order**0.5)) if limit is None else int(math.ceil(limit**0.5))

    j_list = []
    k_list = []
    i = 0
    match = set([])
    while i <= N:
        j_list.append(pow(base, i, order))
        k_list.append(pow(x*pow(base_inv, N*i, order), 1, order))
        '''if len(match) != 0:
            break'''
        i += 1

    #print(j_list)
    #print(k_list)
    match = set(j_list).intersection(k_list)

    if len(match) == 0:
        raise Exception("Discrete Log error: discrete log of {} base {} does not exist with respect to {}".format(x,base,order))

    match = list(match)[0]
    j = j_list.index(match)
    k = k_list.index(match)

    return j + N*k

def rem(a, x, b, y):
    '''Chinese Remainder function returns c given:
        n = a mod x &
        n = b mod y
        then n = c mod x*y
    '''
    diff = 0
    left = x
    right = y
    if a < b:
        diff = b - a
    elif a > b:
        diff = a - b
        left = y
        right = x

    solution = pow(modinv(left, right)*diff, 1, right)

    if a > b:
        return b + y*solution
    else:
        return a + x*solution


# Find primitive root
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

    # 3. BEST APPROACH: O(f + p1) where f is the number of prime factors and p1 is the second largest prime factor of base-1
    factors = prime_factors(base-1)
    #print(factors)
    for factor in factors:
        if pow(r, (base-1)/ factor, base) != 1:
            continue
        else:
            #print("Bad Factor:",factor)
            return False

    return True

def isPrime(n, certainty=4):
    '''n is the integer in question, certainty is a parameter to repeat the Miller-Rabin test (recommended 4 repetitions for 96.1% avoidance of strong psuedoprimes)'''
    if n <= 1:
        raise Exception("isPrime error: n must be positive and not 1")

    k = 0
    m = (n-1)/(2**k)
    while m % 2 == 0:
        k += 1
        m = (n-1)/(2**k)

    if k == 0:
        #g, _, _ = egcd(2, n)
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
            if last != 1 and isPrime(last):
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

def xor(block, key):
    if len(block) != len(key):
        raise Exception("Sizes don't match.")

    result = ""
    for i in range(len(block)):
        result += str(int(block[i]) ^ int(key[i]))

    return result

# Mangler function in DES
def mangler(right_block, key):
    ## Expansion
    expanded_block = ""
    for i in range(len(expansion)):
        expanded_block += right_block[expansion[i]]

    ## XOR
    post_xor_block = xor(expanded_block, key)

    ## S-box
    post_sbox = ""
    for b in range(0, len(post_xor_block), 6):
        address = post_xor_block[b:b+6]
        column = int(address[1:5], 2)
        row = int(address[0] + address[5], 2)
        sub = sbox[b / 6][row][column]
        bit_sub = bin(sub)[2:]
        while len(bit_sub) < 4:
            bit_sub = "0" + bit_sub
        post_sbox += bit_sub

    ## Permutation
    mangler_post_perm = ""
    for i in range(len(post_sbox)):
        mangler_post_perm += post_sbox[mangler_perm[i]]

    return mangler_post_perm