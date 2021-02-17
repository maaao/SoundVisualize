#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import wave

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

class WavLoader():
    def open(self, filename):
        if(filename is None):
            print("filename is empty")
            return -1
        if(not ".wav" in filename):
            print("wrong filename")
            return -1

        wf = wave.open(filename, mode="rb")
        self.framerate = wf.getframerate()

        data_raw = wf.readframes(-1)
        self.data = np.frombuffer(data_raw, dtype=np.int16)
        if(wf.getnchannels() == 2):
            self.data = self.data[::2]
        print(self.data.shape)

    def getframerate(self):
        return self.framerate

    def read(self, CHUNK):
        if(len(self.data) > CHUNK):
            data_stream = self.data[:CHUNK]
            self.data = self.data[CHUNK:]
            return data_stream.tobytes()
        else:
            print(len(self.data))
            return None

# def streamMicrophone():

plot_sxx = None
plot_wave = None

def main():
    RATE = 32000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 8192

    USE_MIC = False

    if(USE_MIC):
        stream = pyaudio.PyAudio().open(
            rate=RATE,
            channels=CHANNELS,
            format=FORMAT,
            input=True,
            output=False,
            frames_per_buffer=CHUNK
        )
    else:
        filename = "data/wav/train/denki/0.wav"
        stream = WavLoader()
        stream.open(filename)
        RATE = stream.getframerate()
    

    # マイクで録音した波形描画用
    numOfPlots = RATE*2
    global plot_wave
    plot_wave = np.zeros(numOfPlots)

    # スペクトログラム解析用の変数
    nperseg = 512           # 時間軸の分解能
    noverlap = nperseg//8    # 取得データ毎の重複量
    nfft = nperseg*64        # 周波数の分解能
    vmin = -200
    vmax = 175
    size_f = int(nfft/2)+1
    size_t = int((numOfPlots-noverlap)/(nperseg-noverlap))
    size_step_t = int((CHUNK-noverlap)/(nperseg-noverlap))
    # size_t = size_step_t # デバッグ用
    f = np.linspace(0, int(RATE/2), size_f)
    t = np.linspace(0, numOfPlots/RATE, size_t)
    
    # スペクトログラム解析結果描画用
    global plot_sxx
    plot_sxx = np.full((size_f, size_t), 1e-10)

    # 描画の準備
    fig = plt.figure()
    gs = fig.add_gridspec(2, 6)
    ax1 = fig.add_subplot(gs[0,:])
    ax2 = fig.add_subplot(gs[1,:])
    
    ax1.set_ylim(np.iinfo(np.int16).min,np.iinfo(np.int16).max)
    line,  = ax1.plot(range(numOfPlots), [0]*numOfPlots)
    
    quad = ax2.pcolormesh(t, f, plot_sxx, shading='auto', cmap="jet", vmin=vmin, vmax=vmax)
    # cb = fig.colorbar(quad, ax=ax2)
    # cb.mappable.set_clim([vmin, vmax])

    def init():
        quad.set_array([])
        return quad
        
    def update(i):
        global plot_wave
        global plot_sxx

        data_raw = stream.read(CHUNK)
        if(data_raw is None):
            exit(0)
        data = np.frombuffer(data_raw, dtype=np.int16)

        # wavデータの可視化
        plot_wave = np.hstack([plot_wave[CHUNK:], data])
        line.set_ydata(plot_wave)

        # スペクトログラム解析
        f, t, Sxx = signal.spectrogram(x=data, fs=RATE, nperseg=nperseg, noverlap=noverlap, nfft=nfft)

        # plot_sxxとSxxを水平に結合し余分な箇所を削除し結果を描画
        plot_sxx = np.delete(np.hstack((plot_sxx, np.array(Sxx))), np.arange(0, size_step_t), axis=1)
        quad.set_array(10*np.log(plot_sxx))
        # quad.set_array(10*np.log(Sxx/Sxx.max()))
        return quad
    
    ani = animation.FuncAnimation(fig, update, init_func=init, interval=0.001)
    plt.show()
        
if __name__ == "__main__":
    main()