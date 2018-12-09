#!/usr/bin/python

"""
PyAudio + PyQtGraph Spectrum Analyzer

Author:@sbarratt
Date Created: August 8, 2015

"""

import pyaudio
import struct
import sys
import numpy as np
import wave
import heatmap

import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore

# Audio Format (check Audio MIDI Setup if on Mac)
FORMAT = pyaudio.paInt16
RATE = 44100
CHANNELS = 2

# Set Plot Range [-RANGE,RANGE], default is nyquist/2
RANGE = None
if not RANGE:
    RANGE = RATE / 2

# Set these parameters (How much data to plot per FFT)
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

# Which Channel? (L or R)
LR = "l"


class SpectrumAnalyzer:
    def __init__(self, use_wav):
        self.pa = pyaudio.PyAudio()
        self.use_wav = use_wav
        if use_wav:
            self.initSpeakers('/Users/alevenberg/Documents/erv/prototype/sound/dt_16bars_102rap.wav')
        else:
            self.initMicrophone()
        self.initUI()
        self.bass_signal_start_index = -1
        self.bass_signal_end_index = -1
        self.treble_signal_start_index = -1
        self.treble_signal_end_index = -1
        self.graphics = heatmap.HeatMap()

    def find_input_device(self):
        device_index = None
        for i in range(self.pa.get_device_count()):
            devinfo = self.pa.get_device_info_by_index(i)
            if devinfo["name"].lower() in ["mic", "input"]:
                device_index = i

        return device_index

    def initSpeakers(self, audio_file):
        self.wf = wave.open(audio_file, 'r')
        self.stream = self.pa.open(
            format=self.pa.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )
        self.bass_signal_start_index = 1100
        self.bass_signal_end_index = 1130


    def initMicrophone(self):
        device_index = self.find_input_device()

        self.stream = self.pa.open(format=FORMAT,
                                   channels=CHANNELS,
                                   rate=RATE,
                                   input=True,
                                   input_device_index=device_index,
                                   frames_per_buffer=INPUT_FRAMES_PER_BLOCK)

    def readAndPlayWavData(self):
        block = self.wf.readframes(INPUT_FRAMES_PER_BLOCK)
        self.stream.write(block)
        count = len(block) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, block)
        return np.array(shorts)

    def readMicData(self):
        block = self.stream.read(INPUT_FRAMES_PER_BLOCK)
        count = len(block) / 2
        format = "%dh" % (count)
        shorts = struct.unpack(format, block)
        if CHANNELS == 1:
            return np.array(shorts)
        else:
            l = shorts[::2]
            r = shorts[1::2]
            if LR == 'l':
                return np.array(l)
            else:
                return np.array(r)

    def initUI(self):
        self.app = QtGui.QApplication([])
        self.app.quitOnLastWindowClosed()

        self.mainWindow = QtGui.QMainWindow()
        self.mainWindow.setWindowTitle("Spectrum Analyzer")
        self.mainWindow.resize(800, 300)
        self.centralWid = QtGui.QWidget()
        self.mainWindow.setCentralWidget(self.centralWid)
        self.lay = QtGui.QVBoxLayout()
        self.centralWid.setLayout(self.lay)

        self.specWid = pg.PlotWidget(name="spectrum")
        self.specItem = self.specWid.getPlotItem()
        self.specItem.setMouseEnabled(y=False)
        self.specItem.setYRange(0, 1000)
        self.specItem.setXRange(-RANGE, RANGE, padding=0)

        self.specAxis = self.specItem.getAxis("bottom")
        self.specAxis.setLabel("Frequency [Hz]")
        self.lay.addWidget(self.specWid)

        self.mainWindow.show()
        self.app.aboutToQuit.connect(self.close)

    def close(self):
        self.stream.close()
        sys.exit()

    def get_spectrum(self, data):
        T = 1.0 / RATE
        N = data.shape[0]
        Pxx = (1. / N) * np.fft.fft(data)
        f = np.fft.fftfreq(N, T)
        Pxx = np.fft.fftshift(Pxx)
        f = np.fft.fftshift(f)

        return f.tolist(), (np.absolute(Pxx)).tolist()


    def get_ratio_signal(self, spectrum, decibels):
        if self.bass_signal_start_index == -1:
            self.bass_signal_start_index = spectrum.index(0)
            self.bass_signal_end_index = spectrum.index(1020)
        if self.treble_signal_start_index == -1:
            self.bass_signal_start_index = spectrum.index(0)
            self.bass_signal_end_index = spectrum.index(1020)
        bass_signal = decibels[self.bass_signal_start_index:self.bass_signal_end_index]
        rest_signal = decibels[self.bass_signal_end_index:]
        total_bass_decibals = np.sum(bass_signal)
        total_rest_decibals = np.sum(rest_signal)
        bass_ratio = total_bass_decibals / (total_rest_decibals + total_bass_decibals)
        treble_ratio = total_rest_decibals / (total_rest_decibals + total_bass_decibals)
        return bass_ratio, treble_ratio


    def mainLoop(self):
        batch_size = 10.
        cnt = 0
        agr_bass = 0
        agr_tre = 0
        while 1:
            # Sometimes Input overflowed because of mouse events, ignore this
            try:
                if self.use_wav:
                    data = self.readAndPlayWavData()
                else:
                    data = self.readMicData()
            except IOError:
                continue
            f, Pxx = self.get_spectrum(data)
            # get signal for TERV/EERV
            bass_signal, rest_signal = self.get_ratio_signal(f, Pxx)
            cnt += 1
            if cnt % int(batch_size) == 0:
                print('{} : {}'.format(agr_bass / batch_size, agr_tre / batch_size))
                agr_bass = 0
                agr_tre = 0
            agr_bass += bass_signal
            agr_tre += rest_signal
            # print('{} : {}'.format(bass_signal, rest_signal))
            # self.graphics.visualize_ratio(bass_signal, rest_signal, 0.1)
            self.specItem.plot(x=f, y=Pxx, clear=True)
            QtGui.QApplication.processEvents()


if __name__ == '__main__':
    sa = SpectrumAnalyzer(False)
    sa.mainLoop()