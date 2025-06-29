#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: aukustiharris
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import audio
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import sip
import threading



class hrf(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "hrf")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 20000000
        self.rtl_samp_rate = rtl_samp_rate = 2048000
        self.qrate = qrate = 192000
        self.mult_const = mult_const = 500e-3
        self.freq = freq = 99.1e6
        self.bandwidth = bandwidth = 2e6
        self.audio_dec = audio_dec = 4

        ##################################################
        # Blocks
        ##################################################

        self.soapy_hackrf_source_1 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_1 = soapy.source(dev, "fc32", 1, "a18c63dc2c37be13",
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_1.set_sample_rate(0, 8000000)
        self.soapy_hackrf_source_1.set_bandwidth(0, 0)
        self.soapy_hackrf_source_1.set_frequency(0, freq)
        self.soapy_hackrf_source_1.set_gain(0, 'AMP', True)
        self.soapy_hackrf_source_1.set_gain(0, 'LNA', min(max(40, 0.0), 40.0))
        self.soapy_hackrf_source_1.set_gain(0, 'VGA', min(max(32, 0.0), 62.0))
        self.rational_resampler_xxx_0_1 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=125,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            32768, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self._qrate_range = qtgui.Range(0, 500000, 10e3, 192000, 200)
        self._qrate_win = qtgui.RangeWidget(self._qrate_range, self.set_qrate, "'qrate'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._qrate_win)
        self._mult_const_range = qtgui.Range(0, 1, 10e-3, 500e-3, 200)
        self._mult_const_win = qtgui.RangeWidget(self._mult_const_range, self.set_mult_const, "'mult_const'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._mult_const_win)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self._audio_dec_range = qtgui.Range(0, 10, 1, 4, 200)
        self._audio_dec_win = qtgui.RangeWidget(self._audio_dec_range, self.set_audio_dec, "'audio_dec'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._audio_dec_win)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=(48000*4),
        	audio_decimation=4,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_1, 0), (self.analog_wfm_rcv_0, 0))
        self.connect((self.soapy_hackrf_source_1, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.soapy_hackrf_source_1, 0), (self.rational_resampler_xxx_0_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "hrf")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_rtl_samp_rate(self):
        return self.rtl_samp_rate

    def set_rtl_samp_rate(self, rtl_samp_rate):
        self.rtl_samp_rate = rtl_samp_rate

    def get_qrate(self):
        return self.qrate

    def set_qrate(self, qrate):
        self.qrate = qrate

    def get_mult_const(self):
        return self.mult_const

    def set_mult_const(self, mult_const):
        self.mult_const = mult_const

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_hackrf_source_1.set_frequency(0, self.freq)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth

    def get_audio_dec(self):
        return self.audio_dec

    def set_audio_dec(self, audio_dec):
        self.audio_dec = audio_dec




def main(top_block_cls=hrf, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
