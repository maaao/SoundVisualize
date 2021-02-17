#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import signal

from editWav import wavedit

filename="wav/voice_10s.wav"
we = wavedit(filename)
samplerate = we.getframerate()
bin_l, bin_r = we.getBinData()
data = np.fromstring(bin_l, dtype=np.int16)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.plot(range(len(data)), data.tolist())

# fig = plt.figure()
# ax2 = fig.add_subplot(1, 1, 1)
# ax2.set_ylim(0, 8000)
f,t,Sxx = signal.spectrogram(x=data, fs=samplerate)
dSxx = 10*np.log10(Sxx)
ax2.pcolormesh(t, f, dSxx, shading='gouraud')
# fig.colorbar()
plt.show()