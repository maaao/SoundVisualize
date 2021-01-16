import numpy as np
from matplotlib import pyplot as plt
import wave
import struct


def create_wave(A,f0,fs,t, fname):#A:振幅,f0:基本周波数,fs:サンプリング周波数,再生時間[s]
    #nポイント
    #--------------------------------------------------------------------------------------------------------------------
    point = np.arange(0,fs*t)
    sin_wave =A* np.sin(2*np.pi*f0*point/fs)

    sin_wave = [int(x * 32767.0) for x in sin_wave]#16bit符号付き整数に変換

    #バイナリ化
    binwave = struct.pack("h" * len(sin_wave), *sin_wave)

    if(not (".wav" in fname)):
        fname = fname + ".wav"

    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write(fname)
    p = (2, 2, fs, len(binwave), 'NONE', 'not compressed')#(チャンネル数(1:モノラル,2:ステレオ)、サンプルサイズ(バイト)、サンプリング周波数、フレーム数、圧縮形式(今のところNONEのみ)、圧縮形式を人に判読可能な形にしたもの？通常、 'NONE' に対して 'not compressed' が返されます。)
    w.setparams(p)
    w.writeframes(binwave)
    w.close()


def main():
    RATE = 48000
    CHUNK = 1024
    REC_TIME = 10

    t = np.arange(0, RATE*REC_TIME)
    # data_sin = np.sin(2*np.pi*440*t/RATE)
    data_sin = np.sin(2*np.pi*(36*t/RATE+440)*t/RATE) + np.sin(2*np.pi*(192*t/RATE+440)*t/RATE)
    data = [int(x*16000) for x in data_sin]#16bit符号付き整数に変換

    data_bin = np.array(data).tobytes()

    w = wave.Wave_write("wav/createwave.wav")
    w.setparams((1, 2, RATE, len(data_bin), 'NONE', 'not compressed'))
    w.writeframes(data_bin)
    w.close()


if __name__ == '__main__':
    main()