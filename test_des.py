from crypto.encryption import if_perm, expansion, sbox, mangler_perm
from utilities import Utilities as utils

message = "abcdefgh"
# Translate message
binary_msg2 = []
binary_msg = bin(int(message.encode('hex'), 16))[2:]
while len(binary_msg) % 8 != 0:
    binary_msg = "0" + binary_msg

print "message: ", binary_msg

## Key gen
key = utils.generate_keys(algo="des")['k']
print "Key:", key, "\n"

## Encryption
# Initial permutation
post_iperm = [0] * len(binary_msg)
for i in range(len(binary_msg)):
    post_iperm[i] = binary_msg[if_perm[i]]

left_block = post_iperm[:32]
right_block = post_iperm[32:]

## Mangler function
# Expansion
expanded_block = [0] * 48
for i in range(len(expansion)):
    expanded_block[i] = right_block[expansion[i]]
# print "Expanded block size:", len(expanded_block)

# XOR
post_xor_block = []
for i in range(len(expanded_block)):
    new_b = str(int(expanded_block[i]) ^ int(key[i]))
    post_xor_block.append(new_b)

# S-Box
post_sbox = []
for b in range(0, len(post_xor_block), 6):
    lookup = post_xor_block[b:b+6]
    column = ''.join(lookup[1:5])
    row = lookup[0] + lookup[5]
    column = int(column, 2)
    row = int(row, 2)
    four_bits = sbox[row][column]
    bit_array = bin(four_bits)[2:]
    while len(bit_array) < 4:    # Pad byte to 8 bits
        bit_array = "0" + bit_array
    post_sbox.append(bit_array)

post_sbox = ''.join(post_sbox)

# Mangler permutation
mangler_post_perm = [0] * len(post_sbox)
for i in range(len(post_sbox)):
    mangler_post_perm[i] = post_sbox[mangler_perm[i]]

# XOR: Mangler out and left block
post_final_xor = []
for i in range(len(left_block)):
    out = str(int(mangler_post_perm[i]) ^ int(left_block[i]))
    post_final_xor.append(out)

final_left_block = ''.join(right_block)
final_right_block = ''.join(post_final_xor)

# Final permutation
pre_fperm = final_left_block + final_right_block
post_fperm = [0] * len(pre_fperm)
for i in range(len(pre_fperm)):
    post_fperm[if_perm[i]] = pre_fperm[i]
cipher = ''.join(post_fperm)

print "CIPHER: ", cipher, "\n"

## Decryption: Do the same thing, but reverse the order of keys

# Initial permutation
post_iperm = [0] * len(cipher)
for i in range(len(cipher)):
    post_iperm[i] = cipher[if_perm[i]]

left_block = post_iperm[:32]
right_block = post_iperm[32:]

## Mangler function
# Expansion
expanded_block = [0] * 48
for i in range(len(expansion)):
    expanded_block[i] = right_block[expansion[i]]
# print "Expanded block size:", len(expanded_block)

# XOR
post_xor_block = []
for i in range(len(expanded_block)):
    new_b = str(int(expanded_block[i]) ^ int(key[i]))
    post_xor_block.append(new_b)

# S-Box
post_sbox = []
for b in range(0, len(post_xor_block), 6):
    lookup = post_xor_block[b:b+6]
    column = ''.join(lookup[1:5])
    row = lookup[0] + lookup[5]
    column = int(column, 2)
    row = int(row, 2)
    four_bits = sbox[row][column]
    bit_array = bin(four_bits)[2:]
    while len(bit_array) < 4:    # Pad byte to 8 bits
        bit_array = "0" + bit_array
    post_sbox.append(bit_array)

post_sbox = ''.join(post_sbox)

# Mangler permutation
mangler_post_perm = [0] * len(post_sbox)
for i in range(len(post_sbox)):
    mangler_post_perm[i] = post_sbox[mangler_perm[i]]


# XOR: Mangler out and left block
post_final_xor = []
for i in range(len(left_block)):
    out = str(int(mangler_post_perm[i]) ^ int(left_block[i]))
    post_final_xor.append(out)

final_left_block = ''.join(right_block)
final_right_block = ''.join(post_final_xor)

# Final permutation
pre_fperm = final_left_block + final_right_block
post_fperm = [0] * len(pre_fperm)
for i in range(len(pre_fperm)):
    post_fperm[if_perm[i]] = pre_fperm[i]
plaintxt = ''.join(post_fperm)

print "PLAIN:  ", plaintxt, "\n"