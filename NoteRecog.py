import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from numpy.fft import fft, ifft
from playsound import playsound


def analysis():

    pass


from os.path import dirname, join as pjoin
import scipy.io

# data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
# wav_fname = pjoin(data_dir, 'test-44100Hz-2ch-32bit-float-be.wav')
# fs, raw = read("sine8000hz.wav")
# try:  # some mono Audio doesn't store bits in arrays, so .shape doesn't work
#     print(f"number of channels = {raw.shape[1]}")
#     for channel in raw.shape[1]:
#         plt.plot(channel)
#         plt.show()
# except:
#     print("number of channels = 1")
#     plt.plot(raw)
#
# plt.show()
#
# length = raw.shape[0] / fs
# print(f"length = {length}s")

playsound("C:/Users/Tosin/Documents/TriScore/sine8000hz.wav")

# plt.show()
