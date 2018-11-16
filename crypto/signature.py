class Signature(object):
    def __init__(self):
        pass

    def rsa(self, message):
        return ""

    def el_gamal(self, message, key={}):
        p = key['p']
        alpha = key['alpha']
        beta = key['beta']
        # choose k gcd(k,p-1)=1
        # r = alpha**k mod p
        # s = k**-1 *(m-a*r) mod p-1
        # return (m, r, s)
        pass

    def dsa(self, message):
        pass

    def verify(self, signedmsg, key, option='e'):
        ''' Options:
        e = el_gamal
        r = rsa
        d = dsa
        '''
        # el gamal:
        # message = signedmsg[0]
        # r = message[1]
        # s = message[2]
        # p = key[0]
        # alpha = key[1]
        # beta = key[2]
        # v1 = beta**r * r**s mod p
        # v2 = alpha**m mod p
        # verify v1 === v2 mod p
        
        pass