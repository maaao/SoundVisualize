import pyaudio
import librosa

import numpy as np
import matplotlib.pyplot as plt

from editWav import wavedit

def fft(rate, data):
    ##### 周波数成分を表示する #####
    #縦軸：dataを高速フーリエ変換する（時間領域から周波数領域に変換する）
    data = data / 32768.0 # 符号付き16bitのため2^15の値で正規化
    fft_data = np.abs(np.fft.fft(data))    
    #横軸：周波数の取得　　#np.fft.fftfreq(データ点数, サンプリング周期)
    freqList = np.fft.fftfreq(data.shape[0], d=1.0/rate)  
    
    return freqList, fft_data


def showSpectrogram(rate, data):
    # フレーム長
    fft_size = 1024                 
    # フレームシフト長 
    hop_length = int(fft_size / 4)  
    
    # 短時間フーリエ変換実行
    amplitude = np.abs(librosa.core.stft(data, n_fft=fft_size, hop_length=hop_length))
    
    # 振幅をデシベル単位に変換
    log_power = librosa.core.amplitude_to_db(amplitude)
    
    # グラフ表示
    librosa.display.specshow(log_power, sr=rate, hop_length=hop_length, x_axis='time', y_axis='hz', cmap='magma')
    plt.colorbar(format='%+2.0f dB')  
    plt.show()

def main():
    #音声ファイル読み込み
    filename = "voice_10s.wav"
    # filename = "test.wav"
    we = wavedit(filename)
    samplerate = we.getframerate()
    bin_l, bin_r = we.getBinData()
    data = np.fromstring(bin_l, dtype=np.int16)
    print(data)

    fig = plt.figure()
    ax1 = fig.add_subplot(3, 1, 1)
    ax2 = fig.add_subplot(3, 1, 3)
    ax3 = fig.add_subplot(3, 1, 2)

    freq, data_fft = fft(samplerate, data)

    ax1.set_ylim(np.iinfo(np.int16).min, np.iinfo(np.int16).max)
    ax1.plot(np.arange(0, len(data)/samplerate, 1/samplerate), data)

    ax2.set_xlim(0, 10000)
    ax2.plot(freq, data_fft)

    pxx, freq, bins, t = plt.specgram(data,Fs = samplerate)

    plt.show()

if __name__=='__main__':
    main()