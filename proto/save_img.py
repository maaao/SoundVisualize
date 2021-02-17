import wave

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import librosa

def save_fig(data, RATE):
    # スペクトログラム解析用の変数
    nperseg = 8192          # 時間軸の分解能
    noverlap = nperseg//8    # 取得データ毎の重複量
    nfft = nperseg//1024       # 周波数の分解能
    vmin = -100
    vmax = 100

    data_int = np.frombuffer(data, dtype=np.int16)

    frequencies, times, spectrogram = signal.spectrogram(x=data_int, fs=48000)
    print(10*np.log10(spectrogram).max())
    print(10*np.log10(spectrogram).min())

    # frequencies, times, spectrogram = signal.spectrogram(x=data_int, fs=48000, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
    plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), cmap="hsv", vmin=vmin, vmax=vmax)
    # plt.pcolormesh(times, frequencies, spectrogram)
    # plt.pcolormesh(times, frequencies, 10*np.log10(spectrogram), shading='auto', cmap="jet", vmin=vmin, vmax=vmax)

    # pxx, freq, bins, t = plt.specgram(data_int,Fs = 48000)
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(np.frombuffer(data, dtype=np.int16))
    plt.show()

words = ["denki", "tsukete"]
for word in words:
    for i in range(1):
        print("wav/"+word+"/"+str(i)+".wav")
        # with wave.open("wav/createwave.wav", mode="rb") as wf:
        with wave.open("wav/"+word+"/"+str(i)+".wav", mode="rb") as wf:
            RATE = wf.getframerate
            data = wf.readframes(-1)

        save_fig(data, RATE)
            