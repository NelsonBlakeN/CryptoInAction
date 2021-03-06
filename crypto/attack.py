from __future__ import print_function
from crypto.decryption import Decryption
from crypto.encryption import Encryption
import crypto_utils as cutils
import utilities as utils
import random, math, fractions, time

# Index corresponds to digit size of corresponding binary encoded key
# des_benchmark_keys = ['', '\a', '!', 'm', '!!', 'aa', '\aaa', 'abc']#, , '\a\a\a\a', '~~~~']

class Attack(object):
    def __init__(self):
        self.enc = Encryption()
        self.dec = Decryption()
        pass

    def benchmark(self, attack, algorithm='rsa', min=3, max=15, key=""):
        if algorithm not in ['rsa', 'rsa_sig', 'el_gamal', 'dsa', 'des', 'otp']:
            print("Invalid algorithm passed")
            return None

        message = 'h'

        for key_size in range(min, max+1):
            #print('[' + algorithm + ':' + attack + ']' + " (key_size " + str(key_size) + ')', end='')
            #print(' ', end='')
            # key = des_benchmark_keys[key_size]
            keys = utils.Utilities.generate_keys(algo=algorithm, prime_length=key_size, key=key)
            ciphertext = ''
            if algorithm == 'rsa':
                ciphertext = utils.enc.rsa(message, keys)
                e = keys['e']
                n = keys['p'] * keys['q']
                #print("Starting attack")
                #print("n=",n)
                start = stop = time.time()
                output = self.rsa_dec(cipher=ciphertext, pub_key={'e': e, 'n': n}, appr=attack)
                stop = time.time()
                if output == 'h':
                    print(str(stop - start))#+ ' seconds')
                else:
                    print("wrong plaintext recovered")
            elif algorithm == 'el_gamal':
                ciphertext = utils.enc.el_gamal(message, keys)
                p = keys['p']
                alpha = keys['alpha']
                beta = keys['beta']
                #print("Starting attack")
                #print("p=",p,"a=",keys["a"])
                start = stop = time.time()
                output = self.el_gamal_dec(cipher=ciphertext, pub_key={'p': p, 'alpha': alpha, 'beta': beta}, appr=attack)
                stop = time.time()
                if output == 'h':
                    print(str(stop - start)) #+ ' seconds')
                else:
                    print("wrong plaintext recovered: {}".format(output))

            elif algorithm == 'des':
                ciphertext = utils.enc.des(message, keys)

                start = stop = time.time()
                # Run brute force...
                output = self.des_attack(cipher=[message, ciphertext])
                stop = time.time()
                if output == 'h':
                    print(str(stop - start))
                else:
                    print("Failed to recover plaintext: {}".format(output))

            elif algorithm == 'otp':
                # Because the OTP key needs to be the size of the message,
                # recalculate keys using the message
                new_msg = message * key_size    # Since the key is dependent on the message, increase the message size each time
                # Encode message
                binary_msg = bin(int(new_msg.encode('hex'), 16))[2:]

                keys = utils.Utilities.generate_keys(algo=algorithm, prime_length=key_size, key=binary_msg)

                # Encrypt
                ciphertext = utils.enc.one_time_pad(binary_msg, keys)

                start = stop = time.time()
                # Run brute force...
                print("Running attack with key {} ({})".format(keys['key'], len(str(int(keys['key'], 2)))))
                output = self.otp_attack([new_msg, ciphertext])
                stop = time.time()
                if output == new_msg:
                    print(str(stop - start))
                else:
                    print("Failed to recover plaintext: {}".format(output))

    def otp_attack(self, cipher, appr="brute"):
        # Generate random key
        known_plaintxt = cipher[0]
        known_cipher = cipher[1]
        result = ""
        k = 1
        if appr == 'brute':
            while result != known_cipher:
                # Encode message
                binary_msg = bin(int(known_plaintxt.encode('hex'), 16))[2:]
                key = bin(k)[2:]
                while len(key) < len(binary_msg):
                    key = "0" + key
                key = utils.Utilities.generate_keys(algo='otp', key=key)

                result = self.enc.one_time_pad(binary_msg, key)

        if result == "":
            raise Exception("OTP brute force failed")

        if result == known_cipher:
            return known_plaintxt
        return ''

    def des_attack(self, cipher, appr = "brute"):
        # Use generate_keys with a random key
        # Call result = self.enc.des(message, key set)
        # If result != cipher, increment key and repeat
        known_plaintxt = cipher[0]
        known_cipher = cipher[1]
        result = ""
        k = 1
        if appr == 'brute':
            while result != known_cipher:
                key = str(k)
                keys = utils.Utilities.generate_keys(algo='des', key=key)
                result = self.enc.des(known_plaintxt, keys)
                k += 1

        if result == "":
            raise Exception("DES brute force failed")

        if result == known_cipher:
            return known_plaintxt

        return ''


    def el_gamal_dec(self, cipher, pub_key={}, appr = "shanks"):
        p = pub_key['p']
        alpha = pub_key['alpha']
        beta = pub_key['beta']
        a = 0

        r = cipher[0]
        t = cipher[1]

        if appr == "brute":
            i = 3
            while i < p-1:
                if beta == pow(alpha, i, p):
                    a = i
                    break
                i += 1

            if i == p-1:
                raise Exception("El Gamal brute force attack failed")

            #print("Private key:",a)

            return self.dec.el_gamal(cipher=cipher, key={'p': p, 'beta': beta, 'alpha': alpha, 'a': a})
        elif appr == "shanks":
            alpha_inv = cutils.modinv(alpha, p)
            N = int(math.ceil(p**0.5))
            if N**2 < p-1:
                raise Exception("Shanks attack error: bad choice of N")

            j_list = []
            k_list = []
            i = 0
            match = set([])
            while i <= N:
                j_list.append(pow(alpha, i, p))
                k_list.append(pow(beta*pow(alpha_inv, N*i, p), 1, p))
                i += 1

            #print(j_list)
            #print(k_list)
            match = set(j_list).intersection(k_list)

            if len(match) == 0:
                raise Exception("El Gamal shanks attack failed: match={}".format(match))

            match = list(match)[0]
            j = j_list.index(match)
            k = k_list.index(match)

            a = j + N*k

            #print("Private key:",a)

            return self.dec.el_gamal(cipher=cipher, key={'p': p, 'beta': beta, 'alpha': alpha, 'a': a})
        elif appr == "pohlig":
            factors = cutils.prime_factors(p-1)
            #print(factors)
            alpha_inv = cutils.modinv(alpha, p)
            x = 0
            left = pow(alpha, (p-1)/2, p)
            right = pow(beta, (p-1)/2, p)
            if left == 1:
                raise Exception("Pollig-Hellman error: left equal to 1 mod {} therefore solution impossible".format(p))

            if right == 1:
                x = 0
            else:
                x = 1
            i = 2
            while (p-1) % (2**i) == 0:
                right = pow(pow(alpha_inv, x, p)*beta, 1, p)
                right = pow(right, (p-1)/(2**i), p)
                x = x + 2**(i-1)*1 if right == left else x
                i += 1
            a = (x, 2**(i-1))
            limit = math.sqrt(p)
            #print("a is {} mod {}".format(x, 2**(i-1)))

            if len(factors) > 1:
                for prime in factors[1:]:
                    left = pow(alpha, (p-1)/prime, p)
                    right = pow(beta, (p-1)/prime, p)
                    #print(right, p, left)
                    x = cutils.dlog(right, p, left, prime) % prime
                    i = 2
                    while (p-1) % (prime**i) == 0:
                        right = pow(pow(alpha_inv, x, p)*beta, 1, p)
                        right = pow(right, (p-1)/(prime**i), p)
                        if right == left:
                            x = (x + prime**(i-1)*1)
                        elif right != 0:
                            x = x + prime**(i-1)*(cutils.dlog(right, p, left, prime**(i-1)) % prime**(i-1))
                        else:
                            x = x
                        i += 1
                    #print("a is {} mod {}".format(x, prime**(i-1)))
                    a = (cutils.rem(a[0], a[1], x, prime**(i-1)), a[1]*prime**(i-1))

            #print("Using a as {} mod {}".format(a[0], a[1]))
            return self.dec.el_gamal(cipher=cipher, key={'p': p, 'beta': beta, 'alpha': alpha, 'a': a[0]})
        else:
            raise Exception("Unknown attack: {}".format(appr))

    def dsa(self, cipher, pub_key={}, appr = "brute"):
        pass

    def rsa_dec(self, cipher, pub_key={}, appr = "brute"):
        n = pub_key["n"]
        e = pub_key["e"]

        if appr == "brute":
            p = q = 3
            while p < n:
                if n % p == 0:
                    q = n / p
                    phi = (p - 1) * (q - 1)
                    d = cutils.modinv(e, phi)
                    return self.dec.rsa(cipher, {'d': d, 'p': p, 'q': q})
                p += 2
            return ""
        elif appr == "p-1":
            b = 3
            B = 2
            while True:
                b = pow(b, B, n)
                p = fractions.gcd(b - 1, n)
                if p > 1 and p < n:
                    q = n / p
                    phi = (p - 1) * (q - 1)
                    d = cutils.modinv(e, phi)
                    return self.dec.rsa(cipher, {'d': d, 'p': p, 'q': q})

                if B > math.sqrt(n):
                    return ""
                    #raise Exception("P-1 attack error: bound = {} possible no solution exists for n = {}".format(B, n))

                B += 2

            return ""
        else:
            return None

    def rsa_sig(self, cipher, pub_key={}, appr = "brute"):
        pass

