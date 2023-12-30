"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
from reedsolo import RSCodec


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, message = b'', rsc = RSCodec(10)):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Reed-Solomon Encoding',   # will show up in GRC
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message = message
        self.rsc = rsc

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        enc_msg = self.rsc.encode(input_items)
        return enc_msg
