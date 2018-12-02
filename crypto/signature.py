import crypto_utils as utils

class Signature(object):
    def __init__(self):
        pass

    def rsa(self, message, key={}):
        d = key['d']
        p = key['p']
        q = key['q']
        n = p * q
 
        msg = message.encode('hex')
        msg = int(msg, 16)

        if msg > n:
            raise Exception("WeakKeyError: message is larger than n potential loss of data")

        msg = pow(msg, d, n)
        msg = hex(int(msg))[2:]
        if msg[-1] == "L":
            msg = msg[:-1]
        return (message, msg)

    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        a = key['a']
        msg = message.encode('hex')
        msg = int(msg, 16)
        if msg > p:
            raise Exception("WeakKeyError: message is larger than prime (p) potential loss of data")

        # choose k gcd(k,p-1)=1
        k = random.randint(3, p-1)
        g, _, _ = utils.egcd(k, p-1)
        while g != 1:
            k = random.randint(3, p-1)
            g, _, _ = utils.egcd(k, p-1)
        # r = alpha**k mod p
        r = pow(alpha, k, p)

        # s = k**-1 *(m-a*r) mod p-1
        k_inv = utils.modinv(k, p-1)
        s = (k_inv * (msg - a * r)) % (p-1)

        hex_r = hex(int(r))[2:]
        hex_s = hex(int(s))[2:]
        if hex_r[-1] == "L":
            hex_r = hex_r[:-1]
        if hex_s[-1] == "L":
            hex_s = hex_s[:-1]
        return (message, hex_r, hex_s)

    def dsa(self, message, key={}):
        p = key['p']
        q = key['q']
        a = key['a']
        alpha = key['alpha']

        msg = message.encode('hex')
        msg = int(msg, 16)

        if msg > q:
            raise Exception("WeakKeyError: message is larger than prime (q) potential loss of data")
        
        if pow(key['alpha'], (p-1)/2, p) != 1:
            raise Exception("KeyError: private key is not configured correctly")

        # pick k from 1 to q-1
        k = random.randint(1, q-1)
        # r = (a^k mod p) mod q
        r = pow(alpha, k, p) % q

        # s = k^(-1)(m + a*r) mod q
        kinv = utils.modinv(k, q)
        ar = pow(a * r, 1, q)
        s = pow(kinv * (msg + ar), 1, q)
        
        hex_r = hex(int(r))[2:]
        hex_s = hex(int(s))[2:]
        if hex_r[-1] == "L":
            hex_r = hex_r[:-1]
        if hex_s[-1] == "L":
            hex_s = hex_s[:-1]
        return (message, hex_r, hex_s)

    def verify(self, signedmsg, key, option='e'):
        ''' Options:
        e = el_gamal
        r = rsa
        d = dsa
        '''
        msg = signedmsg[0].encode('hex')
        msg = int(msg, 16)

        # el gamal:
        if option == 'e':
            r = int(signedmsg[1], 16)
            s = int(signedmsg[2], 16)

            p = key['p']
            alpha = key['alpha']
            beta = key['beta']

            betator = pow(beta, r, p)
            rtos = pow(r, s, p)

            v1 = (betator * rtos) % p
            v2 = pow(alpha, msg, p)
            return v1 == v2

        # rsa
        elif option == 'r':
            sig = int(signedmsg[1], 16)

            e = key['e']
            p = key['p']
            q = key['q']
            n = p * q

            test = pow(sig, e, n)
            return msg == test

        elif option == 'd':
            r = int(signedmsg[1], 16)
            s = int(signedmsg[2], 16)
            
            p = key['p']
            q = key['q']
            alpha = key['alpha']
            beta = key['beta']

            sinv = utils.modinv(s, q)
            
            # u1 = s^(-1)*m mod q
            u1 = pow(sinv*msg, 1, q)

            # u2 = s^(-1)*r mod q
            u2 = pow(sinv*r, 1, q)

            # v = (alpha^u1 * beta^u2 mod p)mod q
            v = pow(pow(alpha, u1, p) * pow(beta, u2, p), 1, p) % q
            return v == r
        else:
            raise Exception("Unkown verification option:",option,"(e: El Gamal, r: RSA, d: DSA)")