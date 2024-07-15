import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from numpy.fft import fft, ifft, fftshift
from playsound import playsound
from graphics import *
import subprocess


def spect_plot(ift_val, ift_freq, t_step):
    ift_vals = np.abs(ift_val)
    peak = max(max(spec_set) for spec_set in ift_vals)
    n_ift_data = ift_vals/peak
    print(ift_freq[0:10])
    for i in range(100):  # len(n_ift_data)):
        x = i*t_step
        # print(f"max arg = {n_ift_data[i].argmax()}")
        # print(n_ift_data[i])
        for j in range(len(n_ift_data[i])//2):
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
        self.frange = self.count//2 + 1  # frequency range

        self.fw = min(fw, self.count)  # frame width
        self.st = min(fw, st, self.count)  # step in # of frames

        if st is not None:
            self.fts = self.st * self.ts  # frame time step

        if fw is not None and st is not None:
            self.slice(self.fw, self.st)
            self.ft_slice(self.fw, self.st)
            self.fw_fs = self.rate / self.fw
        else:
            self.split = None
            self.fts = None
            self.ft_split = None
            self.fw_fs = None  # frequency step based on frequency Width

    def axis(self, var):
        if var in ["t", "time"]:
            return np.linspace(0, (self.count - 1) * self.ts, self.count)
        elif var in ["f", "freq", "frequency"]:
            return np.linspace(0, (self.count - 1) * self.fs, self.count)
        elif var in ["fr", "frame", "frame_frequency"]:
            return np.linspace(0, (self.count - 1) * self.fw_fs, self.count)
        elif var in ["fts", "freq_time", "frequency_time"]:
            return np.linspace(0, (self.count - 1) * self.fts, self.count)
        elif var in ["c", "count"]:
            return np.linspace(0, self.count - 1, self.count)
        else:
            raise ValueError("Invalid .axis argument \n"
                             "Argument not in ('t','time','f','freq','frequenct','c','count')")

    def slice(self, frame_w, step):
        t_steps = (len(self.data) - frame_w)//step + 1
        self.split = []
        for i in range(t_steps):
            self.split.append(self.data[step:frame_w + step])

    def ft_slice(self, frame_w, step):
        t_steps = (self.count - frame_w) // step + 1
        self.ft_split = []
        for i in range(t_steps):
            self.ft_split.append(fft(self.data[i*step:frame_w + i*step]))
            # print(self.axis("f"))
            # print(self.axis("f")[np.abs(self.ft_split[i])[:self.count//2].argmax()])


def f_plot(time, data, freq, bfrange):
    figure, axis = plt.subplots(3, 1)
    new_data = fft(data)
    axis[0].plot(time, data)
    axis[1].plot(freq[:bfrange//30], np.abs(new_data)[:bfrange//30]) # //30 to crop to frame
    print(freq[np.abs(new_data)[:bfrange].argmax()])
    axis[2].plot(time, np.real(ifft(new_data)))
    plt.show()


def analysis(data, rate, frame_w=None, frame_step=None):
    # Based on human hearing 20Hz - 20000Hz
    if frame_w is None:
        frame_w = rate/10
    else:
        if frame_step is None:
            frame_step = frame_w/2

    a_file = audio(data, rate, frame_w, frame_step)
    spect_plot(a_file.ft_split, a_file.axis("fr"), a_file.fts)
    f_plot(a_file.axis("t"), a_file.data, a_file.axis("f"), a_file.frange)


# subprocess.call(['ffmpeg', '-i', 'filename.mp3', 'filename.wav'])
fss, raw = read("sine.wav")
# raw = raw[0:1000]  # To test on a smaller sample
try:  # some mono Audio doesn't store bits in arrays, so .shape doesn't work
    print(f"number of channels = {raw.shape[1]}")
    for channel in raw.shape[1]:
        analysis(channel, fss)

except IndexError:
    analysis(raw, fss, fss//10, 200)
    # plt.specgram(raw, Fs=fss)
    # plt.show()

# playsound("C:/Users/Tosin/Documents/TriScore/sine8000hz.wav")
