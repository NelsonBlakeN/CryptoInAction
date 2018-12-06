from crypto.encryption import if_perm
from utilities import Utilities
import crypto_utils as cutils
from pprint import pprint

message = "abcdefgh"

# Key gen
keys = Utilities.generate_keys(algo="des")

# Encryption
# Translate message
binary_msg = bin(int(message.encode('hex'), 16))[2:]
while len(binary_msg) < 64:
    binary_msg = "0" + binary_msg

print "message:\t", binary_msg
print "message (hex):\t", hex(int(binary_msg, 2))

### METHOD STARTS HERE

# Obtain key
keys = keys['k']

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

    final_round_block = right_block + post_final_xor

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

print "\n", hex(int(''.join(post_fperm), 2))
