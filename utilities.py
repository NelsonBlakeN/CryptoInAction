from crypto.decryption import Decryption
from crypto.encryption import Encryption
from crypto.signature import Signature
import crypto_utils as cutils
import random

enc = Encryption()
dec = Decryption()
sign = Signature()

# Initial key permutation
key_perms = [56, 48, 40, 32, 24, 16, 8,
            0,  57, 49, 41, 33, 25, 17,
            9,  1,  58, 50, 42, 34, 26,
            18, 10, 2,  59, 51, 43, 35,
            62, 54, 46, 38, 30, 22, 14,
            6,  61, 53, 45, 37, 29, 21,
            13, 5,  60, 52, 44, 36, 28,
            20, 12, 4,  27, 19, 11, 3]

# Permutation of the left half
left_perm = [13, 16, 10, 23, 0,  4,
             2,  27, 14, 5,  20, 9,
             22, 18, 11, 3,  25, 7,
             15, 6,  26, 19, 12, 1]

# Permutation of right half
right_perm = [40, 51, 30, 36, 46, 54,
              29, 39, 50, 44, 32, 47,
              43, 48, 38, 55, 33, 52,
              45, 41, 49, 35, 28, 31]

class Utilities(object):
    enc_algos = {
        "rsa": enc.rsa,
        "des": enc.des,
        "otp": enc.one_time_pad,
        "el_gamal": enc.el_gamal
    }
    dec_algos = {
        "rsa": dec.rsa,
        "des": dec.des,
        "otp": dec.one_time_pad,
        "el_gamal": dec.el_gamal
    }
    sign_algos = {
        "rsa": sign.rsa,
        "el_gamal": sign.el_gamal,
        "dsa": sign.dsa
    }

    HOST = '127.0.0.1'
    SERVER_PORT = 8080

    def __init__(self):
        pass

    @staticmethod
    def generate_keys(algo="el_gamal", prime_length = 31):
        if algo == "el_gamal":
            p = cutils.find_large_prime(prime_length)
            alpha = cutils.randroot(p, 2, 100)
            a = random.randint(3, p-1) # private key
            beta = pow(alpha, a, p)
            return {'p': p, 'alpha': alpha, 'beta': beta, 'a': a}

        elif algo == "rsa":
            # HMB, this is about to be some Grade A "excellent" code
            e = 3
            while True:
                p = q = cutils.find_large_prime(prime_length // 2 + 1)
                while p == q:
                    p = cutils.find_large_prime(prime_length // 2 + 1)
                phi = (p - 1) * (q - 1)
                try:
                    d = cutils.modinv(e, phi)
                except:
                    e += 1
                    continue
                return {'d': d, 'e': e, 'p': p, 'q': q}
            

        elif algo == "dsa":
            q = cutils.find_large_prime(prime_length)
            p = 2*q + 1
            while (p - 1) % q != 0 or not cutils.isPrime(p):
                #print("Testing Prime:", p)
                p = p + q
                while not cutils.isPrime(p):
                    p = p + q
            #print("Found (p, q): {},{}".format(p, q))

            g = cutils.randroot(p)
            alpha = pow(g, (p-1) / q, p)
            while pow(alpha, q, p) != 1:
                g = cutils.randroot(p, 2, q-1)
                alpha = pow(g, (p-1) / q, p)

            a = random.randint(3, q-1) # private key
            beta = pow(alpha, a, p)
            return {'p': p, 'q': q, 'alpha': alpha, 'beta': beta, 'a': a}

        elif algo == "des":
            key = "abcdefgh"    # 8 byte key
            round_keys = []

            # Convert key to binary before permutations
            # Translate message
            binary_key = bin(int(key.encode('hex'), 16))[2:]
            while len(binary_key) % 8 != 0:
                binary_key = "0" + binary_key

            perm_key = [0] * len(key_perms)
            for i in range(len(key_perms)):
                perm_key[i] = binary_key[key_perms[i]]

            c = perm_key[:28]
            d = perm_key[28:]

            for i in range(16):
                # Circular shift
                c.append(c.pop(0))
                d.append(d.pop(0))
                if i not in [0, 1, 8, 15]:
                    # Shift twice
                    c.append(c.pop(0))
                    d.append(d.pop(0))

                pre_perm_key = c + d

                ## Permutation with discard
                left_side = ""
                right_side = ""
                # Left
                for i in range(len(left_perm)):
                    left_side += pre_perm_key[left_perm[i]]
                # Right
                for i in range(len(right_perm)):
                    right_side += pre_perm_key[right_perm[i]]

                round_key = left_side + right_side

                round_keys.append(round_key)
            return {'k': round_keys}

        else:
            return {}