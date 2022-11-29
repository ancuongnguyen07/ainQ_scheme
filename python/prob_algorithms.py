import sym_cipher
import hash_func as hash
import EC_operation as ec
from random import randint

# 7 probabilistic algorithns


def gen_secret_value(q,G):
    '''
    Run by each edge drone and a team leader
    Generate a pair of secret/public key for each edge drone d_i or team leader
    '''
    # ---- STEP 1
    # generate a secret key
    x_i = randint(0,q)

    # ---- STEP 2
    # compute corresponding public key
    P_i = G.__rmul__(x_i)

    return x_i, P_i

def full_key_gen(x_i,s_i,P_i,R_i):
    '''
    Run by each edge drone
    Generate full key pair for each drone
    in the format: (partial_key, key)
    '''
    # full private key
    full_priv_key = (s_i, x_i)

    # full public key
    full_pub_key = (R_i, P_i)

    return full_priv_key, full_pub_key

def gen_group_key(q,G,drone_list):
    '''
    Run by team leader
    Generate a symmetric group session key
    '''
    # ----- STEP 1
    K_g = randint(0,q)
    l_k = randint(0,q)

    # ----- STEP 2
    V = G.__rmul__(l_k)

    # ----- STEP 3
    for drone in drone_list:


def key_retrieval():
    pass

def re_key():
    pass


## ==================== Start your implementation below this line ============================== ##
## ==================== Feel free to pull the parameters into another file if you wish ========= ##
## ==================== If you notice any bugs, kindly draw our attention to it ================ ##

# # secret key x_i each user
# x_Alice = randint(0, q)
# x_Bob = randint(0, q)

# # Public key P_pub_i each user
# P_pub_Alice = G.__rmul__(x_Alice)
# P_pub_Bob = G.__rmul__(x_Bob)

# # Partial private key R_i
# r_Alice = randint(0, q)
# R_Alice = G.__rmul__(r_Alice)
# r_Bob = randint(0, q)
# R_Bob = G.__rmul__(r_Bob)

# # Partial private key d_i
# ID_Alice = 'ID_Alice'
# ID_Bob = 'ID_Bob'
# d_Alice = r_Alice + x * generate_hash(f'{ID_Alice},{R_Alice},{P_pub_Alice}')
# d_Bob = r_Bob + x * generate_hash(f'{ID_Bob},{R_Bob},{P_pub_Bob}')

# # Full private key SK_i
# SK_Alice = (d_Alice, x_Alice)
# SK_Bob = (d_Bob, x_Bob)

# # Full public key PK_i
# PK_Alice = (R_Alice, P_pub_Alice)
# PK_Bob = (R_Bob, P_pub_Bob)

## ============ Initialize the secure communication channel
## ============ Encryption and Encapsualtion - Alice's side

l_Alice = randint(0, q)
h_Alice = randint(0, q)
U = G.__rmul__(l_Alice)
V = G.__rmul__(h_Alice)

Y = P_pub_Bob.__add__(R_Bob.__add__(P_pub.__rmul__(generate_hash(f'{ID_Bob},{R_Bob},{P_pub_Bob}'))))
T = Y.__rmul__(h_Alice)

# Session key K_AB
K_AB = generate_hash(f'{Y},{V},{T},{ID_Bob},{P_pub_Bob}')

# Encrypting with AES using session key K_AB
plaintext = 'Security Protocol'
iv, ciphertext = sc.encrypt(plaintext, bytes.fromhex(hex(K_AB)[2:]))
C_AB = ciphertext

# Encapsulating K_AB and ciphertext C_AB
H = generate_hash(f'{U},{C_AB},{T},{ID_Alice},{ID_Bob},{P_pub_Alice},{P_pub_Bob}')
W = d_Alice + l_Alice * H + x_Alice * H
phi = (U, V, W)

## =============== Decapsulation and Decryption - Bob's side

# Retrieving Y and T from Alice's side
Y_prime = G.__rmul__(d_Bob + x_Bob)
T_prime = V.__rmul__(d_Bob + x_Bob)

assert Y_prime == Y, 'Y should equal Y_prime'
print(f'Encapsulated Y: {Y}')
print(f'Decapsulated Y: {Y_prime}')

assert T_prime == T, 'T should equal T_prime'
print('=====================')
print(f'Encapsulated T: {T}')
print(f'Decapsulated T: {T_prime}')

# Retrieving session key K_AB from Alice's side
H_prime = generate_hash(f'{U},{C_AB},{T_prime},{ID_Alice},{ID_Bob},{P_pub_Alice},{P_pub_Bob}')
K_AB_prime = generate_hash(f'{Y_prime},{V},{T_prime},{ID_Bob},{P_pub_Bob}')
assert K_AB_prime == K_AB, 'K_AB should equal K_AB_prime'

# Decrypting with AES using session key K_AB_prime
decrypted_text = sc.decrypt(iv, C_AB, bytes.fromhex(hex(K_AB_prime)[2:]))
assert decrypted_text == plaintext, 'decrypted text should same as the plaintext'
print('=====================')
print(f'Plaintext: {plaintext}')
print(f'Ciphertext: {ciphertext}')
print(f'Decrypted text: {decrypted_text}')
