import sys, base64
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC

# inspired by https://pycryptodome.readthedocs.io/en/latest/src/signature/dsa.html

def sign(mess, private_key):
    hash_mess = SHA256.new(mess)
    # signed_hash_mess = rsa.encrypt(hash_mess, private_key)
    # return signed_hash_mess
    key = ECC.import_key(private_key)
    signer = DSS.new(key, 'fips-186-3')
    return signer.sign(hash_mess)

def verify(mess, public_key, signature):
    hash_mess = SHA256.new(mess)
    # decrypted_hash_mess = rsa.decrypt(signed_hash_mess, public_key)
    # return hash_mess == decrypted_hash_mess
    key = ECC.import_key(public_key)
    verifier = DSS.new(key, 'fips-186-3')
    try:
        verifier.verify(hash_mess, signature)
        return True
    except:
        return False

def main():
    file_path, pub_key_file, pri_key_file = sys.argv[1:4]
    message = open(file_path, 'rb').read()
    pub_key = open(pub_key_file, 'r').read()
    pri_key = open(pri_key_file, 'r').read()

    signed = sign(message, pri_key)
    signed_base64 = base64.b64encode(signed)
    print(f'Signature (base64): {signed_base64}')
    verify(message, pub_key, signed)

if __name__ == '__main__':
    main()