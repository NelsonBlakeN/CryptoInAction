
# euclidean method of finding gcd(a,b)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, n):
    g, x, y = egcd(a ,n)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % n