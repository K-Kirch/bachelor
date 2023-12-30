from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from reedsolo import RSCodec

def encrypt(plaintext, key, iv):
    aes_block_size = 16
    aes_cipher = AES.new(key, AES.MODE_CBC, iv)

    # Add padding to the plaintext
    padded_data = pad(plaintext.encode('utf-8'), aes_block_size)

    # Encrypt the padded data using AES in CBC mode
    ciphertext = aes_cipher.encrypt(padded_data)
    return ciphertext

def decrypt(ciphertext, key, iv):
    aes_block_size = 16
    aes_cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the ciphertext using AES in CBC mode
    decrypted_data = aes_cipher.decrypt(ciphertext)

    # Remove padding
    plaintext = unpad(decrypted_data, aes_block_size).decode('utf-8')
    return plaintext

def add_reed_solomon(data, rs_syndrome_size=10):
    rs_codec = RSCodec(rs_syndrome_size)

    # Add Reed-Solomon error correction to the data
    encoded_data = rs_codec.encode(data)
    return encoded_data

def decode_reed_solomon(data, rs_syndrome_size=10):
    rs_codec = RSCodec(rs_syndrome_size)

    # Decode Reed-Solomon error correction from the data
    decoded_data = rs_codec.decode(data)
    return decoded_data[0]  # Return the first element as bytes

# Generate a random 128-bit key and IV for AES
aes_key = get_random_bytes(16)
iv = get_random_bytes(16)

# Example data
original_data = "Hello, this is a test message."

# Encryption and Reed-Solomon encoding
encrypted_data = encrypt(original_data, aes_key, iv)
encoded_data = add_reed_solomon(encrypted_data)

# Reed-Solomon decoding and decryption
decoded_data = decode_reed_solomon(encoded_data)
decrypted_data = decrypt(decoded_data, aes_key, iv)

print("Original Data:", original_data)
print("Encrypted Data:", encrypted_data)
print("Encoded Data:", encoded_data)
print("Decoded Data:", decoded_data)
print("Decrypted Data:", decrypted_data)