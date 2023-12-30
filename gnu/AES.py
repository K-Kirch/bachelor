import numpy as np
from gnuradio import gr
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class AES(gr.sync_block):
    """
    docstring for block AES
    """
    def __init__(self, key, iv, mode, key_size, block_size, padding, **kwargs):
        gr.sync_block.__init__(self,
            name="AES",
            in_sig=[np.uint8],
            out_sig=[np.uint8])
        self.key = key
        self.iv = iv
        self.mode = mode
        self.key_size = key_size
        self.block_size = block_size
        self.padding = padding

    def AESencrypt(self, input_items, output_items):
        # Generate a random key
        self.key = get_random_bytes(self.key_size)
        
        # Pad the message
        p_msg = input_items + b'\0' * (AES.block_size - len(self.key) % AES.block_size)

        # Create a cipher object
        cipher = AES.new(self.key, AES.MODE_CBC)

        # Encrypt the message
        output_items = cipher.encrypt(p_msg)
        return self.key, output_items
    
    def AESdecrypt(self, input_items, output_items):
        # Create a cipher object
        cipher = AES.new(self.key, AES.MODE_CBC)

        # Decrypt the message
        d_msg = cipher.decrypt(input_items)
        
        # Unpad the message
        output_items = d_msg.rstrip(b'\0')
        return output_items    
    def AESdecrypt(self, input_items, output_items):
        # Create a cipher object
        cipher = AES.new(self.key, AES.MODE_CBC)

        # Decrypt the message
        d_msg = cipher.decrypt(input_items)
        
        # Unpad the message
        output_items = d_msg.rstrip(b'\0')
        return output_items