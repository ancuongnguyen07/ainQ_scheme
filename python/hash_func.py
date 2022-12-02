import hashlib

def H(plaintext):
    '''Generate a hash digest in bytes'''
    h = hashlib.new('sha256')
    h.update(plaintext.encode('utf-8'))
    return h.hexdigest()

def H1(plaintext):
    '''Generate a hash digest in binary form {0,1} for later XORing
    but it is needed to convert back to int form for XORing in Python'''
    return int(H(plaintext), base=16)

def H0(plaintext, q):
    '''Generate a hash digest and transform it to finite prime field'''
    return int(H(plaintext), base=16) % q

HASH_FUNC_DICT = {'H0': H0, 'H1': H1}