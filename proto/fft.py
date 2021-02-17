import pyaudio
import numpy as np
import matplotlib.pyplot as plt

RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
CHUNK = RATE

audio = pyaudio.PyAudio()
stream = audio.open(
    rate=RATE,
    channels=CHANNELS,
    format=FORMAT,
    input=True,
    output=False,
    frames_per_buffer=CHUNK
)

len_fig = RATE * 3       # num of plots in figure
len_win = 1000
len_overlap = len_win//2   

plot_wave = np.zeros(len_fig)  # array for plot wav data
fig_wave , ax_wave = plt.subplots()
line_wave, = ax_wave.plot(plot_wave)
ax_wave.set_ylim(np.iinfo(np.int16).min,np.iinfo(np.int16).max)

min_var = 0
max_var = 80
fig_fft = plt.figure()
ax_fft = fig_fft.add_subplot(111)
# https://matplotlib.org/2.0.2/examples/pylab_examples/pcolor_demo.html

# 1024はどうやって指定する？
# fft結果のサイズに依存
popoi = (CHUNK - len_win + len_overlap)//len_overlap
popoi2 = (len_fig - len_win + len_overlap)//len_overlap
y, x = np.mgrid[slice(0, popoi2 +1, 1), slice(0, len_win+1, 1)]
plot_fft = np.full(((len_fig - len_win + len_overlap)//len_overlap, len_win), 1e-2)  

while True:
    data_raw = stream.read(CHUNK)
    if(data_raw is None):
        exit(0)
    data = np.frombuffer(data_raw, dtype=np.int16).astype(np.float64)

    # wavデータの可視化
    plot_wave = np.hstack([plot_wave[CHUNK:], data])
    line_wave.set_ydata(plot_wave)
    

    fft_data_out = np.zeros((popoi, len_win)) 

    for i in range(popoi):
        begin = i*(len_win - len_overlap)
        end = begin + len_win
        fft_data_in = data[begin:end]
        fft_data_out[i] = np.abs(np.fft.fft(fft_data_in))

    plot_fft = np.vstack([plot_fft, fft_data_out])[popoi:]

    ax_fft.pcolorfast(y, x, np.log10(plot_fft)*10, cmap='hsv', vmin=min_var, vmax=max_var)

    fig_wave.canvas.draw()
    fig_wave.show()
    fig_wave.canvas.flush_events()

    fig_fft.canvas.draw()
    fig_fft.show()
    fig_fft.canvas.flush_events()