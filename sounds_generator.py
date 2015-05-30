#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 15:19:57 2015

@author: pavel
"""
from sys import argv
from struct import pack
import wave, numpy, os

#import matplotlib.pyplot as plt



NUM_CHANNELS = 1
SAMPLE_WIDTH = 2
FRAME_RATE = 44100

def mkdir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def write_file(path, data):
    mkdir(path)

    wf = wave.open(path, 'wb')
    wf.setnchannels(NUM_CHANNELS)
    wf.setframerate(FRAME_RATE)
    wf.setsampwidth(SAMPLE_WIDTH)


    wfData = ""
    for i in range(len(data)):
        if NUM_CHANNELS == 1:
            wfData += pack('h', data[i])
        elif NUM_CHANNELS > 1:
            for ch in range(NUM_CHANNELS):
                wfData += pack('h', data[ch][i])

    wf.writeframes(wfData)
    wf.close()


def sine_wave(freq, time_ms, amp=15000):
    num_frames = numpy.int(time_ms*FRAME_RATE/1000.0)
    omega = 2.0*numpy.pi*freq/FRAME_RATE
    x = numpy.array([omega*i for i in xrange(num_frames)])
    return amp*numpy.sin(x)

def full_period_sine_wave_time(freq, appr_time_ms, amp=15000):
    wave_period_ms = 1000.0 / freq #ms
    repeats = round(appr_time_ms/wave_period_ms)

    time_ms = repeats*wave_period_ms

    return sine_wave(freq, time_ms, amp)

def full_period_sine_wave(freq, amp=15000):
    num_frames = FRAME_RATE #- 1
    omega = 2.0*numpy.pi*freq/FRAME_RATE
    x = numpy.array([omega*i for i in xrange(num_frames)])
    return amp*numpy.sin(x)


def amplify(signal, amp = 15000):
    return amp*signal

def decay(signal, time_const=None, factor=3.0):
        if not time_const:
            time_const = 1.0*len(signal)/FRAME_RATE / factor

        k = -1.0/(time_const*FRAME_RATE)
        new_signal = numpy.zeros(len(signal))

        for i in xrange(len(signal)):
            new_signal[i] = signal[i]*numpy.exp(k*i)

        return new_signal


def generate_full_period_wave(freq, path, decayed= True):
    data = full_period_sine_wave(freq)
    if decayed:
        data = decay(data)
    write_file(path, data)






def main(arg):
    pass

if __name__ == "__main__":
    main(argv)
