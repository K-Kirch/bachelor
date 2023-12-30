from reedsolo import RSCodec
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import random
import numpy as np

rsc = RSCodec(10)

def rs_encode(msg):
    # Reed-Solomon encoding
    ec_msg = rsc.encode(msg)
    return ec_msg

def rs_decode(msg):
    # Reed-Solomon decoding
    dc_msg = rsc.decode(msg)

    # Check if message is tampered with, if not return message
    if rsc.check(msg) == False:
        print("False Message Decrypting")
        dc_msg = rsc.decode(msg)
    else:
        return dc_msg[0]


def AES_encrypt(key, iv, msg):
    # Pad the message
    padded_msg = msg + b'\0' * (AES.block_size - len(msg) % AES.block_size)

    # Create a cipher object and encrypt the data
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt message
    encrypt = cipher.encrypt(padded_msg)
    return encrypt

def AES_decrypt(key, iv, msg):
    # Create a cipher object for decryption
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the message
    decrypt_msg = cipher.decrypt(msg)

    # Unpad message
    unpadded_msg = decrypt_msg.rstrip(b'\0')
    
    return unpadded_msg

def inject_errors(encoded_data, error_probability):
    # Simulate errors
    error_location = [i for i in range(len(encoded_data)) if random.random() < error_probability]
    for location in error_location:
        encoded_data[location] = random.randint(0, 255)
    return bytes(encoded_data)

def burst_errors(data, probability, max_burst_length, normal_mean, normal_std):
    induced_data = bytearray(data)

    #Generate normally distributed string
    normal_data = np.random.normal(loc = normal_mean, scale = normal_std, size = len(data)).astype(np.uint8)

    # Iterate over each position in the data
    for i in range(len(data)):
        if random.random() < probability:
            # Induce burst error
            burst_length = random.randint(1, max_burst_length)
            burst_start = i
            burst_end = min(i + burst_length, len(data))

            # Perform logical OR with normally distributed values within the burst range
            induced_data_list = list(induced_data)
            normal_data_list = list(normal_data)
            for j in range(burst_start, burst_end):
                induced_data_list[j] |= normal_data_list[j]

            # Convert back to bytearray
            induced_data = bytearray(induced_data_list)
    return bytes(induced_data)


# Stress test the encryption with larger messages

#with open('msg.txt') as f:
#    message = f.read()

# Generate key
key = get_random_bytes(16)
iv = get_random_bytes(16)
message = (b'This is a test message and my name is Kristian')

# message = (b'This is a message')
print(f'Original: {message}')

aes_ec = AES_encrypt(key, iv, message)
print(f'Encrypted: {aes_ec}')
print(type(aes_ec))
print('-------1--------')

rs_ec = rs_encode(aes_ec)
print(f'Encoded: {rs_ec}')
print(type(rs_ec))
print('-------2--------')
'''
# Inject errors
error_probability = 0.096 # Generate some burst noise
rs_eec = inject_errors(list(rs_ec), error_probability)
'''

# Burst Errors
probability = 0.08
max_burst_length = 3
normal_mean = 10
normal_std = 10

rs_eec = burst_errors(rs_ec, probability, max_burst_length, normal_mean, normal_std)

print(f'Data with Errors: {rs_eec}')
print('---------------------------')

if rs_eec == rs_ec:
    print('True')

rs_dc = rs_decode(rs_eec)
print(f'Decoded: {rs_dc}')
print(type(rs_dc))
print('-------3--------')

aes_dc = AES_decrypt(key, iv, rs_dc)
print(f'Decrypted: {aes_dc}')
print('-------4--------')

if rs_ec == rs_eec:
    print('Message is not tampered with')
else:
    print('Message is tampered with')

'''
# write to new file and close it
with open('new_msg.txt', 'w') as f:
    f.write(rs_dc)'''
