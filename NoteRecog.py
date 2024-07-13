import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from numpy.fft import fft, ifft, fftshift
from playsound import playsound
from graphics import *


def time_span(data, rate):
    length = data.shape[0] / rate
    # print(f"length = {length}s")


def spect_plot(ift_val, ift_freq, t_step):
    ift_vals = np.abs(ift_val)
    peak = max(max(spec_set) for spec_set in ift_vals)
    n_ift_data = ift_val/peak
    for i in range(1):  # len(n_ift_data)):
        x = i*t_step
        # print(f"max arg = {n_ift_data[i].argmax()}")
        # print(n_ift_data[i])
        for j in range(len(n_ift_data[i])):
            if n_ift_data[i][j] < 0.5:
                pass
            else:
                plt.scatter(x, ift_freq[j], s=4, alpha=n_ift_data[i][j])


class audio:
    def __init__(self, data, rate, fw=None, st=None):
        self.data = data  # raw data
        self.rate = rate  # impressions per second
        self.ts = 1/rate  # time step
        self.count = len(data)  # Number of frames
        self.fs = rate / self.count  # frequency step

        self.fw = fw
        self.st = st

        if st is not None:
            self.fts = st * self.ts

        if fw is not None and st is not None:
            self.slice(fw, st)
        else:
            self.split = None
            self.fts = None

    def axis(self, var):
        if var in ["t", "time"]:
            return np.linspace(0, (self.count - 1)*self.ts, self.count)
        elif var in ["f", "freq", "frequency"]:
            return np.linspace(0, (self.count - 1)*self.fs, self.count)
        elif var in ["c", "count"]:
            return np.linspace(0, self.count - 1, self.count)
        else:
            raise ValueError("Invalid .axis argument \n"
                             "Argument not in ('t','time','f','freq','frequenct','c','count')")

    def slice(self, frame_w, step):
        t_steps = len(self.data - frame_w)//step
        self.split = []
        for i in range(t_steps):
            self.split.append(self.data[step:frame_w + step])


def f_plot(time, data, freq, bfrange):
    figure, axis = plt.subplots(3, 1)
    new_data = fft(data)
    axis[0].plot(time, data)
    axis[1].plot(freq[:bfrange//30], np.abs(new_data)[:bfrange//30])
    print(freq[np.abs(new_data)[:bfrange].argmax()])
    axis[2].plot(time, np.real(ifft(new_data)))
    plt.show()


def analysis(data, rate, frame_w=None, frame_step=None):
    # Based on human hearing 20Hz - 20000Hz
    if frame_w is None:
        pass
    else:
        if frame_step is None:
            frame_step = frame_w/2

    a_file = audio(data, rate, frame_w, frame_step)

    n = len(data)
    ts = 1/rate  # time step
    t = np.linspace(0, (n-1)*ts, n)  # time axis
    fs = rate / len(data)  # frequency step
    freq = np.linspace(0, (n-1)*fs, n)  # frequency axis
    bfrange = n//2 + 1
    frange = frame_w//2 + 1
    tstep = frame_step * ts
    # todo - make a lil nice function for work above

    # print(f"length of data: {len(data)}")
    # f_data = [[],[]]
    # for i in range((len(data)-frame_w)//frame_step):
    #     shift = i*frame_step
    #     ft_of_frame = np.abs(fft(data[shift:shift+frame_w]))
    #     f_data[0].append(ft_of_frame[:frange])
    #     f_data[1].extend([shift*ts]*frame_w)
    spect_plot(a_file.split, a_file.fs, a_file.fts)
    f_plot(t, data, freq, bfrange)
    pass


fss, raw = read("sine.wav")
raw = raw[0:1000]
try:  # some mono Audio doesn't store bits in arrays, so .shape doesn't work
    print(f"number of channels = {raw.shape[1]}")
    for channel in raw.shape[1]:
        analysis(channel, fss) #watch todo
        # plt.plot(channel)
        # plt.show()
except:
    print("number of channels = 1")
    analysis(raw, fss, 400, 200)


plt.show()



# playsound("C:/Users/Tosin/Documents/TriScore/sine8000hz.wav")

# plt.show()
