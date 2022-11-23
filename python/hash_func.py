import hashlib

def generate_hash(plaintext):
    h = hashlib.new('sha256')
    h.update(plaintext.encode('utf-8'))
    return int(h.hexdigest(), base=16)