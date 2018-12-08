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
        while len(binary_msg) < 64:
            binary_msg = "0" + binary_msg

        # Obtain key
        keys = key['k']

        # Initial permutation
        post_iperm = ""
        for i in range(len(binary_msg)):
            post_iperm += binary_msg[if_perm[i]]

        left_block = post_iperm[:32]
        right_block = post_iperm[32:]

        for key in keys:
            post_mangler = cutils.mangler(right_block, key)

            # XOR: Mangler out and left block
            post_final_xor = cutils.xor(left_block, post_mangler)

            left_block = right_block
            right_block = post_final_xor

        temp = left_block
        left_block = right_block
        right_block = temp

        # Final permutation
        pre_fperm = left_block + right_block
        post_fperm = [0] * len(pre_fperm)
        for i in range(len(pre_fperm)):
            post_fperm[if_perm[i]] = pre_fperm[i]

        return ''.join(post_fperm)

    # One Time Pad Encryption
    # message: the string message to encrypt, as binary
    # key: the key used to encrypt (could be multiple values)
    def one_time_pad(self, message, key={}):
<<<<<<< HEAD
        # Assume the message is already binary string
        # binary_msg = bin(int(message.encode('hex'), 16))[2:]
        binary_key = key['key']

        # XOR
        cipher = cutils.xor(message, binary_key)

        # Return cipher
        return cipher
=======
        # Get message as binary
        binary_msg = bin(int(message.encode('hex'), 16))[2:]

        # Generate key of same length
        binary_key = ""
        for _ in range(len(binary_msg)):
            bit = random.getrandbits(1)
            binary_key += str(bit)

        # XOR
        cipher = cutils.xor(binary_msg, binary_key)

        # Return cipher and key
        return cipher, binary_key
>>>>>>> master

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