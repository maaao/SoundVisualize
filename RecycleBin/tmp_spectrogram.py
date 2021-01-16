#coding:utf-8

import numpy as np
import scipy.io.wavfile as wio
import matplotlib.pyplot as plt
from scipy import signal

if __name__ == '__main__':
    rate, data = wio.read("wav/createwave.wav")
    numOfPlots = rate*2
    chunk = 8192
    nperseg = 512
    noverlap = 256
    nfft = 512
    
    size_f = int(nfft/2)+1
    size_t = int((numOfPlots-noverlap)/(nperseg-noverlap))
    size_step_t = int((chunk-noverlap)/(nperseg-noverlap))

    plot_sxx = np.zeros((size_f, size_t))
    print(plot_sxx.shape)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for i in range(int(len(data)/chunk)):
        f, t, Sxx = signal.spectrogram(x=data[chunk*i:chunk*(i+1)], fs=rate, nperseg=nperseg, noverlap=noverlap, nfft=nfft)
        # print(np.array(Sxx).shape)
        # print(len(data))
        # print(len(t))
        # print(len(f))
        # print(len(plot_sxx[0]))
        plot_sxx = np.delete(np.hstack((plot_sxx, np.array(Sxx))), np.arange(0, size_step_t), axis=1)

        # print("--------")
        # print(len(plot_sxx[0]))
        # print(size_t)
        print(10*np.log(plot_sxx/plot_sxx.max()))
        hoge = ax.pcolormesh(np.arange(size_t),f,10*np.log(plot_sxx/plot_sxx.max()),cmap="viridis")
        if(i == 0):
            plt.colorbar(hoge)
            print(hoge)

        # 次の描画まで0.01秒待つ
        plt.pause(0.01)
        # グラフをクリア
        plt.cla()