import numpy as np 
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 
from scipy import signal

CHUNK = 8192
FORMAT = pa.paInt16
CHANNELS = 1
RATE = 44100 # in Hz

p = pa.PyAudio()

stream = p.open(
    format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)



fig = plt.figure()
ax = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

numOfPlots = RATE*2
plot_data = [0]*numOfPlots
x = np.arange(0,numOfPlots)
line, = ax.plot(x, np.random.rand(numOfPlots),'r')
ax.set_ylim(np.iinfo(np.int16).min,np.iinfo(np.int16).max)
ax.ser_xlim = (0,CHUNK)
fig.show()

nperseg = 512
size_f = int(1 + RATE / 2)
size_t = int(numOfPlots/nperseg)
size_t_step = int(CHUNK/nperseg)
plot_Sxx = np.zeros((size_t, size_f))


while 1:
    data = stream.read(CHUNK)
    data_buffer = np.frombuffer(data, dtype=np.int16)
    plot_data = plot_data[CHUNK:] + data_buffer.tolist()
    line.set_ydata(plot_data)

    # スペクトログラムの出力について
    # f.size = int(1 + sampling_frequency / 2)
    # t.size = int(len(data) - noverlap) / (nperseg - noverlap))

    # f,t,Sxx = signal.spectrogram(x=np.array(plot_data[int(numOfPlots/2):]), fs=RATE, nperseg=512)
    f,t,Sxx = signal.spectrogram(x=data_buffer, fs=RATE, nperseg=512, noverlap=0)
    dSxx = 10*np.log10(Sxx)
    # plot_Sxx = plot_Sxx[size_t_step:]+dSxx
    
    print(len(plot_Sxx))
    print(plot_Sxx)
    print(len(dSxx))
    print(dSxx)
    # plot_Sxx = np.hstack([plot_Sxx, dSxx])
    print(plot_Sxx)
    ax2.pcolormesh(t,f,dSxx,vmax=1e-6,cmap="GnBu")

 
    fig.canvas.draw()
    fig.canvas.flush_events()
 