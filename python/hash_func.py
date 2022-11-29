import hashlib

def H1(plaintext):
    '''Generate a hash digest in bytes'''
    h = hashlib.new('sha256')
    h.update(plaintext.encode('utf-8'))
    return h.hexdigest()

def H0(plaintext, q):
    '''Generate a hash digest and transform it to finite prime field'''
    return int(H1(plaintext), base=16) % q

HASH_FUNC_DICT = {'H0': H0, 'H1': H1}