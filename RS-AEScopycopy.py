from reedsolo import RSCodec
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

rsc = RSCodec(10)

def encrypt(key, iv, data):
    p_msg = data + b'\0' * (AES.block_size - len(key) % AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypt_data = cipher.encrypt(p_msg, AES.block_size)
    return encrypt_data

def encode_rs(data):
    encoded_data = rsc.encode(data)
    return encoded_data

def decrypt(key, iv, data):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decoded_data = cipher.decrypt(unpad(data, AES.block_size))
    return decoded_data

def decode_rs(data):
    decode_data = rsc.decode(data)
    return decode_data

# Usage
key = get_random_bytes(16)
iv = get_random_bytes(16)
data = 'Hello World!'
print(b'data')
print('--------1--------')

enc_data = encrypt(key, iv, data)
print(b'enc_data')
print('--------2--------')

encode_data = encode_rs(enc_data)
print(b'encode_data')
print('--------3--------')

decode_data = decode_rs(encode_data)
print(b'decode_data')
print('--------4--------')

dec_data = decrypt(key, iv, decode_data)
print(b'dec_data')
print('--------5--------')