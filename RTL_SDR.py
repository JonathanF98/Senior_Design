#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM Reciever
# Author: MLJ SYSTEMS
# Copyright: 2020
# GNU Radio version: 3.8.1.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
import osmosdr
import time
from gnuradio import qtgui

class RTL_SDR(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM Reciever")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM Reciever")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
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

        self.settings = Qt.QSettings("GNU Radio", "RTL_SDR")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.rf_gain = rf_gain = 50
        self.audio_decim = audio_decim = 5
        self.Volume = Volume = 300m
        self.Tuning = Tuning = 100.3M
        self.Samp_rate = Samp_rate = 240k
        self.Presets = Presets = 102.1M
        self.Deviation = Deviation = 75k

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + "rtl=0"
        )
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(Samp_rate)
        self.rtlsdr_source_0.set_center_freq(100.3e6, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_gain(50, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(200k, 0)
        self._rf_gain_range = Range(0, 70, 1, 50, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, 'RF Gain', "slider", int)
        self.top_grid_layout.addWidget(self._rf_gain_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(300m)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=Samp_rate,
        	audio_decim=audio_decim,
        	deviation=Deviation,
        	audio_pass=16k,
        	audio_stop=20k,
        	gain=1.0,
        	tau=75e-6,
        )
        self._Volume_range = Range(0, 1, 50m, 300m, 200)
        self._Volume_win = RangeWidget(self._Volume_range, self.set_Volume, 'VolumeTuner', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Volume_win)
        self._Tuning_range = Range(87.9M, 108.1M, 100k, 100.3M, 200)
        self._Tuning_win = RangeWidget(self._Tuning_range, self.set_Tuning, 'tuning', "counter_slider", float)
        self.top_grid_layout.addWidget(self._Tuning_win)
        # Create the options list
        self._Presets_options = (102.1M, 96.9M, 89.3M, 99.1M, )
        # Create the labels list
        self._Presets_labels = ('WDRM', 'WRSA', 'WLRH', 'WAHR', )
        # Create the combo box
        self._Presets_tool_bar = Qt.QToolBar(self)
        self._Presets_tool_bar.addWidget(Qt.QLabel('Station' + ": "))
        self._Presets_combo_box = Qt.QComboBox()
        self._Presets_tool_bar.addWidget(self._Presets_combo_box)
        for _label in self._Presets_labels: self._Presets_combo_box.addItem(_label)
        self._Presets_callback = lambda i: Qt.QMetaObject.invokeMethod(self._Presets_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._Presets_options.index(i)))
        self._Presets_callback(self.Presets)
        self._Presets_combo_box.currentIndexChanged.connect(
            lambda i: self.set_Presets(self._Presets_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._Presets_tool_bar)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.analog_fm_demod_cf_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "RTL_SDR")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_audio_decim(self):
        return self.audio_decim

    def set_audio_decim(self, audio_decim):
        self.audio_decim = audio_decim

    def get_Volume(self):
        return self.Volume

    def set_Volume(self, Volume):
        self.Volume = Volume

    def get_Tuning(self):
        return self.Tuning

    def set_Tuning(self, Tuning):
        self.Tuning = Tuning

    def get_Samp_rate(self):
        return self.Samp_rate

    def set_Samp_rate(self, Samp_rate):
        self.Samp_rate = Samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.Samp_rate)

    def get_Presets(self):
        return self.Presets

    def set_Presets(self, Presets):
        self.Presets = Presets
        self._Presets_callback(self.Presets)

    def get_Deviation(self):
        return self.Deviation

    def set_Deviation(self, Deviation):
        self.Deviation = Deviation



def main(top_block_cls=RTL_SDR, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
