#!/usr/bin/env Python3

from gnuradio import gr
from gnuradio import blocks
from gnuradio import analog
from gnuradio import uhd
from gnuradio import audio
from gnuradio import qtgui
from gnuradio import fft
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow
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

        # Set up FFT block
        self.fft = fft.fft_vcc(1024, True, ())

        # Set up the QT Frequency Sink block to display the FFT output in a popup window
        self.sink = qtgui.freq_sink_c(
            1024, # FFT size
            qtgui.window().winId(), # Parent widget ID 
            title = "FFT Output", # Window title
            f_range = (0, 2e6), # Frequency range
            y_divs = 10 # Number of vertical divisions
        )
        self.sink.set_update_time(0.1) # Update interval in seconds

        # Set up the sink block to write samples to a file
        # self.sink = blocks.file_sink(gr.sizeof_gr_complex * 1, "output.dat")

        # Set up the audio sink block
        self.audio_sink = audio.sink(32000, "")
        
        # Connect the blocks
        self.connect(self.soapy_hackrf_source_0, self.fft, self.sink)
        self.connect(self.soapy_hackrf_source_0, self.sink)
        self.connect(self.soapy_hackrf_source_0, self.audio_sink)
        
        # Start the QT GUI main loop in a separate thread
        self.qapp = QtGui.QApplication([])
        self.sink.show()
        self.qapp.exec_()

if __name__ == '__main__':
    try:
        tb = my_top_block()
        tb.start()
        time.sleep(10)

    except KeyboardInterrupt:
        pass