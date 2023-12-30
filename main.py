from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import soapy
import time
import satellites.components

class my_top_block(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        # Variables
        samp_rate = 2e6

        # HackRF source block arguments
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        # Set up the HackRF source block
        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, 92e6)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(30, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(30, 0.0), 62.0))

        