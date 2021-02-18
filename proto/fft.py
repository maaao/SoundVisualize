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
len_win = 3000
len_overlap = 2000   

data = np.zeros(len_overlap+CHUNK)

plot_wave = np.zeros(len_fig)  # array for plot wav data
fig_wave , ax_wave = plt.subplots()
line_wave, = ax_wave.plot(plot_wave)
ax_wave.set_ylim(np.iinfo(np.int16).min,np.iinfo(np.int16).max)

min_var = 0
max_var = 80
fig_fft = plt.figure()
ax_fft = fig_fft.add_subplot(111)
# https://matplotlib.org/2.0.2/examples/pylab_examples/pcolor_demo.html

num_fft = (CHUNK - len_win)//(len_win - len_overlap) + 1
num_fft_disp = num_fft * len_fig // CHUNK 

y, x = np.mgrid[slice(0, num_fft_disp +1, 1), slice(0, len_win//2+1, 1)]
plot_fft = np.full((num_fft_disp , len_win//2), 1e-2)  

print("num_fft : {0}".format(num_fft))
print("num_fft_disp : {0}".format(num_fft_disp))

while True:
    data_raw = stream.read(CHUNK)
    if(data_raw is None):
        exit(0)
    data = np.hstack([data, np.frombuffer(data_raw, dtype=np.int16).astype(np.float64)])[CHUNK:]

    # wavデータの可視化
    plot_wave = np.hstack([plot_wave[CHUNK:], data[len_overlap:]])
    line_wave.set_ydata(plot_wave)
    

    # fft_data_out = np.zeros((num_fft, len_win//2 )) 

    # i=0
    # begin = i*(len_win - len_overlap)
    # end = begin + len_win
    # while end <= CHUNK:
    #     print("i : {0}, begin : {1}, end : {2}".format(i, begin, end))

    #     fft_data_out[i] = np.abs(np.fft.fft(data[begin:end]))[:len_win//2]
    #     i+=1
    #     begin = i*(len_win - len_overlap)
    #     end = begin + len_win

    # print(plot_fft.shape)
    # print(fft_data_out.shape)
    # plot_fft = np.vstack([plot_fft, fft_data_out])[num_fft:]
    # ax_fft.pcolorfast(x, y, np.log10(plot_fft)*10, cmap='hsv', vmin=min_var, vmax=max_var)

    fig_wave.canvas.draw()
    fig_wave.show()
    fig_wave.canvas.flush_events()

    fig_fft.canvas.draw()
    fig_fft.show()
    fig_fft.canvas.flush_events()