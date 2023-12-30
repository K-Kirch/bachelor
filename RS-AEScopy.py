from reedsolo import RSCodec
import json
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

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
        dc_msg = rsc.decode(msg)
    else:
        return dc_msg


def AES_encrypt(msg):
    # Generate a random key
    key = get_random_bytes(16)

    # Create a cipher object and encrypt the data
    cipher = AES.new(key, AES.MODE_CBC)

    # Encrypt message
    encrypt = cipher.encrypt(pad(msg, AES.block_size))
    
    iv = b64encode(cipher.iv).decode('utf-8')
    encrypt = b64encode(encrypt).decode('utf-8')
    
    result = json.dumps({'iv':iv, 'ciphertext':encrypt})

    return key, result

def AES_decrypt(key, msg):
    try:
        b64 = json.loads(msg)
        iv = b64decode(b64['iv'])
        msg = b64decode(b64['ciphertext'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypt_msg = unpad(cipher.decrypt(msg), AES.block_size)
        return decrypt_msg
    
    except (ValueError, KeyError):
        print('Incorrect decryption')


# Stress test the encryption with larger messages

#with open('msg.txt') as f:
#    message = f.read()

message = (b'Hello World!')

# message = (b'This is a message')
print(f'Original: {message}')

key, aes_ec = AES_encrypt(message)
print(f'Encrypted: {aes_ec}')

rs_ec = rs_encode(aes_ec)
print(f'Encoded: {rs_ec}')

rs_dc = rs_decode(rs_ec)
print(f'Decoded: {rs_dc}')


aes_dc = AES_decrypt(key, rs_dc)
print(f'Decrypted: {aes_dc}')

'''
# write to new file and close it
with open('new_msg.txt', 'w') as f:
    f.write(rs_dc)
    '''