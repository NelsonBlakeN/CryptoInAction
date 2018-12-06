import crypto_utils as cutils
import random

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
        msg = int(msg, 16)

        if msg > n:
            raise Exception("WeakKeyError: message is larger than n potential loss of data")

        msg = pow(msg, e, n)
        msg = hex(int(msg))[2:]
        if msg[-1] == "L":
            msg = msg[:-1]
        return msg

    # DES Encryption
    # message: the string message to encrypt
    # key: the key used to encrypt (could be multiple values)
    def des(self, message, key={}):
        # Translate message
        binary_msg = bin(int(message.encode('hex'), 16))[2:]
        while len(binary_msg) % 8 != 0:
            binary_msg = "0" + binary_msg

        # Obtain key
        key = key['k']

        # Initial permutation
        post_iperm = ""
        for i in range(len(binary_msg)):
            post_iperm += binary_msg[if_perm[i]]

        left_block = post_iperm[:32]
        right_block = post_iperm[32:]

        post_mangler = utils.mangler(right_block, key)

        print "Post mangler:", post_mangler

        # XOR: Mangler out and left block
        post_final_xor = utils.xor(left_block, post_mangler)

        final_left_block = right_block
        final_right_block = post_final_xor

        # Final permutation
        pre_fperm = final_left_block + final_right_block
        post_fperm = [0] * len(pre_fperm)
        for i in range(len(pre_fperm)):
            post_fperm[if_perm[i]] = pre_fperm[i]

        return ''.join(post_fperm)

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
        if hex_r[-1] == "L":
            hex_r = hex_r[:-1]
        if hex_t[-1] == "L":
            hex_t = hex_t[:-1]

        return (hex_r, hex_t)