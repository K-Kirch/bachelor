"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, key = b'', iv = b'', mode = AES.MODE_CBC, key_size = 16, block_size = AES.block_size, padding = b'\0', **kwargs):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='AES Encrypt',   # will show up in GRC
            in_sig=[np.float32],
            out_sig=[np.uint8]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.key = key
        self.iv = iv
        self.mode = mode
        self.key_size = key_size
        self.block_size = block_size
        self.padding = padding

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        # Generate a random key
        self.key = get_random_bytes(self.key_size)
        
        # Pad the message
        p_msg = input_items + b'\0' * (AES.block_size - len(self.key) % AES.block_size)

        # Create a cipher object
        cipher = AES.new(self.key, AES.MODE_CBC)

        # Encrypt the message
        output_items = cipher.encrypt(p_msg)
        return self.key, output_items