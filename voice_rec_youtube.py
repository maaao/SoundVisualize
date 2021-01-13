import numpy as np 
import pyaudio as pa 
import struct 
import matplotlib.pyplot as plt 
from scipy import signal

CHUNK = 1024 * 2
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

numOfPlots = RATE
plot_data = [0]*numOfPlots
x = np.arange(0,numOfPlots)
line, = ax.plot(x, np.random.rand(numOfPlots),'r')
ax.set_ylim(np.iinfo(np.int16).min,np.iinfo(np.int16).max)
ax.ser_xlim = (0,CHUNK)
fig.show()

while 1:
    data = stream.read(CHUNK)
    data_buffer = np.frombuffer(data, dtype=np.int16)
    plot_data = plot_data[CHUNK:] + data_buffer.tolist()
    line.set_ydata(plot_data)

    # f,t,Sxx = signal.spectrogram(x=np.array(plot_data[int(numOfPlots/2):]), fs=RATE, nperseg=512)
    f,t,Sxx = signal.spectrogram(x=data_buffer, fs=RATE, nperseg=32)
    ax2.pcolormesh(t,f,Sxx,vmax=1e-6,cmap="GnBu")
    fig.canvas.draw()
    fig.canvas.flush_events()