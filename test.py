from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from reedsolo import RSCodec
import pickle

def aes_encrypt(key, text):
    iv = get_random_bytes(16)
    cipher =AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(text.encode('utf-8'), AES.block_size)
    encrypted_text = cipher.encrypt(padded_text)
    return iv + encrypted_text

def aes_decrypt(key, iv, encrypted_text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_text = cipher.decrypt(encrypted_text)
    unpadded_text = unpad(decrypted_text, AES.block_size)
    return unpadded_text.decode('utf-8')

def rs_encode(data, ec_symbols):
    rs = RSCodec(ec_symbols)
    encoded_data = rs.encode(data)
    return encoded_data

def rs_decode(encoded_data, ec_symbols):
    rs = RSCodec(ec_symbols)
    decoded_data = rs.decode(encoded_data)
    return decoded_data

def encrypt_and_encode(key, text, ec_symbols):
    
    # AES Encryption
    iv_and_encrypted_text = aes_encrypt(key, text)

    # Reed-Solomon Encoding
    encoded_data = rs_encode(iv_and_encrypted_text, ec_symbols)

    return encoded_data

def decrypt_and_decode(key, combined_data, ec_symbols):
    # Reed-Solomon Decoding
    decoded_data_tuple = rs_decode(combined_data, ec_symbols)
    
    print(f'Input Data: {combined_data}')
    print(f'Output Data: {decoded_data_tuple}')

    # Concatenate bytearrays from the tuple
    decoded_data = bytearray()
    for data_part in decoded_data_tuple:
        decoded_data += data_part

    print(f'Data: {decoded_data}')

    # Ensure the length of encrypted_text is a multiple of 16
    padding_length = len(decoded_data) % 16
    if padding_length != 0:
        decoded_data = decoded_data[:-padding_length]

    # Extract IV and AES Encrypted Text
    iv = decoded_data[:16]
    encrypted_text = decoded_data[16:]

    
    print(f'Data length: {len(decoded_data)}')
    print(f'IV length: {len(iv)}')
    print(f'Encrypted text: {len(encrypted_text)}')

    # AES Decryption
    decrypted_text = aes_decrypt(key, iv, encrypted_text)

    return decrypted_text

# Usage
key = get_random_bytes(16)
text = 'Hello World!'
ec_symbols = 5

# Encrypt and Encode
combined_data = encrypt_and_encode(key, text, ec_symbols)
print(f'Combined data: {combined_data.hex()}')

# Simulate some errors in combined data
combined_data_with_errors = bytearray(combined_data)
combined_data_with_errors[3] ^= 0x01

# Decode and Decrypt
decrypted_text = decrypt_and_decode(key, bytes(combined_data), ec_symbols)
print(f'Decrypted text: {decrypted_text}')