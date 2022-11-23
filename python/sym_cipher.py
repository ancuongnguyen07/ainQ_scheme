from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
import Crypto.Util.Padding as util
import base64
# import time

# implement AES-256
BLOCK_SIZE = AES.block_size
KEY_SIZE = 32

# inspired by https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode

def generate_key():
    # AES-256 requires the key size of 256 bits -> 32 bytes
    return get_random_bytes(KEY_SIZE)

def encrypt(plaintext, private_key):
    # plaintext must be plain string, not bytes
    # start = time.time()
    padded_plaintext = util.pad(plaintext.encode('utf-8'), BLOCK_SIZE)
    cipher = AES.new(private_key, AES.MODE_CBC)
    ciphertext_byte = cipher.encrypt(padded_plaintext)
    iv = cipher.iv
    ciphertext = base64.b64encode(ciphertext_byte).decode('utf-8')
    # end = time.time()
    # print(f'Encryption time: {end - start}')
    return iv, ciphertext

def decrypt(iv, ciphertext, private_key):
    # iv, ciphertext must be bytes, not text string
    # try:
        # iv = base64.b64decode(iv)
        ciphertext = base64.b64decode(ciphertext)
        # start = time.time()
        cipher = AES.new(private_key, AES.MODE_CBC, iv)
        plaintext_byte = cipher.decrypt(ciphertext)       
        plaintext = util.unpad(plaintext_byte, BLOCK_SIZE)
        # end = time.time()
        # print(f'Decryption time: {end - start}')
        return plaintext.decode('utf-8')
    # except (ValueError, KeyError):
    #     print('Incorrect decryption')
    #     return None

def main():
    # key = generate_key()
    key = b'cuong_nguyen_secret_key_comp_sec'
    # iv = b'cuong_nguyen_1912'
    # key_decode = key.decode('utf-8')
    # plaintext = input('input your meassage: ')
    plaintext = 'Welcome to the Security Protocols course'
    iv, ciphertext = encrypt(plaintext, key)
    decrypted_text = decrypt(iv, ciphertext, key)

    print(f'Private key (bytes): {key}')
    print(f'IV (bytes): {iv}')
    print(f'Ciphertext (base64): {ciphertext}')
    print(f'Decrypted text: {decrypted_text}')

if __name__ == '__main__':
    main()