import crypto_utils as utils

# Initial and permutation, represented as a matrix
# Initial: post_perm[i] = msg[if_perm[i]]
# Final: post_perm[if_perm[i]] = pre_perm[i]
if_perm = [57, 49, 41, 33, 25, 17, 9,  1,
           59, 51, 43, 35, 27, 19, 11, 3,
           61, 53, 45, 37, 29, 21, 13, 5,
           63, 55, 47, 39, 31, 23, 15, 7,
           56, 48, 40, 32, 24, 16, 8,  0,
           58, 50, 42, 34, 26, 18, 10, 2,
           60, 52, 44, 36, 28, 20, 12, 4,
           62, 54, 46, 38, 30, 22, 14, 6]

expansion = [31, 0,  1,  2,  3,  4,
             3,  4,  5,  6,  7,  8,
             7,  8,  9,  10, 11, 12,
             11, 12, 13, 14, 15, 16,
             15, 16, 17, 18, 19, 20,
             19, 20, 21, 22, 23, 24,
             23, 24, 25, 26, 27, 28,
             27, 28, 29, 30, 31, 0]

sbox = [[14, 4,  13, 1, 2,  15, 11, 8,  3,  10, 6,  12, 5,  9,  0, 7],
        [0,  15, 7,  4, 14, 2,  13, 1,  10, 6,  12, 11, 9,  5,  3, 8],
        [4,  1,  14, 8, 13, 6,  2,  11, 15, 12, 9,  7,  3,  10, 5, 0],
        [15, 12, 8,  2, 4,  9,  1,  7,  5,  11, 3,  14, 10, 0,  6, 13]]

mangler_perm = [15, 6,  19, 20,
                28, 11, 27, 16,
                0,  14, 22, 25,
                4,  17, 30, 9,
                1,  7,  23, 13,
                31, 26, 2,  8,
                18, 12, 29, 5,
                21, 10, 3,  24]

class Encryption(object):
    def __init__(self):
        pass

    # RSA Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def rsa(self, message, key={}):
        e = key['e']
        p = key['p']
        q = key['q']
        n = p * q
        msg = message.encode('hex')
        return math.pow(msg, e, n)

    # DES Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def des(self, message, key={}):
        return ""

    # One Time Pad Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def one_time_pad(self, message, key={}):
        return ""

    # El Gamal Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    # encode string: int(string.encode('hex'),16)
    # decode int: str(hex(integer)[2:]).decode('hex')
    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        beta = key['beta']
        msg = message.encode('hex')
        msg = int(msg, 16)
        if msg > p:
            raise Exception("WeakKeyError: message is larger than prime (p) potential loss of data")

        k = random.randint(3,p)
        r = pow(alpha, k, p)
        t = pow(beta, k, p)*msg % p
        hex_r = hex(int(r))[2:]
        hex_t = hex(int(t))[2:]

        return (hex_r, hex_t)