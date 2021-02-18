# http://nalab.mind.meiji.ac.jp/~mk/lecture/fourier-2018/python-sound/node6.html

import wave
import numpy as np
import matplotlib.pyplot as plt

fname = '../data/wav/test/denki/0.wav'
wfile = wave.open(fname, 'r')
numch = wfile.getnchannels()
samplewidth = wfile.getsampwidth()
samplerate = wfile.getframerate()
numsamples = wfile.getnframes()
print("チャンネル数 = ", numch)
print("サンプル幅 (バイト数) = ", samplewidth)
print("サンプリングレート(Hz) =", samplerate)
print("サンプル数 =", numsamples)
print("録音時間 =", numsamples / samplerate)
# すべてのフレームを読み込む (bytesオブジェクトになる)
buf = wfile.readframes(numsamples)
wfile.close()
# numpy の ndarray に変換する
if samplewidth == 2:
    data = np.frombuffer(buf, dtype='int16')
    data = data / 32768.0
elif samplewidth == 4:
   data = np.frombuffer(buf, dtype='int32')
   data = data / 2147483648.0
# ステレオの場合は左チャンネルだけを取り出す
# (0 から最後まで2つおきに、つまり 0,2,4,.. 番目を取り出す)
if numch == 2:
    #l_channel = data[0::2]
    #r_channel = data[1::2]
    data = data[0::2]
# 62000番目から1秒分 (samplerate 個) 取り出し、離散フーリエ変換する
start = 0
N = 1024
c = np.fft.fft(data[start:start+N])
c = abs(c)
plt.subplot(2,1,1)
plt.title('data')
plt.plot(range(start, start+N), data[start:start+N])
plt.subplot(2,1,2)
plt.title('frequency spectrum')
# 対数目盛りにするには次の3行をアンコメントする(注釈を外す)
#ax = plt.gca()
#ax.set_yscale('log')
#ax.set_xscale('log')
# plt.plot(c, linestyle='-')
#横軸を周波数(Hz)にするには、次の2行をアンコメントする
freqList = np.fft.fftfreq(N, d=1.0/samplerate)
print(c.shape)
print(freqList.shape)
print(c)
print(freqList)
for i, freq in enumerate(freqList):
    print("i : {0}, freq : {1}".format(i, freq))
plt.plot(freqList, c, linestyle='-')
plt.tight_layout()  # タイトルの被りを防ぐ
plt.show()