import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import librosa
import librosa.display

fig = plt.figure()
ax = fig.add_subplot(111)
ax.axis("off")

labels = ["denki", "senpuki", "tsukete", "keshite"]

for label in labels:
    for i in range(10):
        wavfilepath = "data/wav/train/{0}/{1}.wav".format(label, i)
        y, sr = librosa.load(wavfilepath)

        n_fft = 1024
        S = np.abs(librosa.stft(y, n_fft=n_fft))

        S_db = librosa.amplitude_to_db(S, ref=np.max)

        min_var = -80
        max_var = 0
        img = librosa.display.specshow(S_db, sr=sr, vmin=min_var, vmax=max_var, cmap=cm.hsv, ax=ax)
        fig.set_tight_layout(True)
        imgfilepath = "data/image/train/{0}/{1}.png".format(label, i)
        fig.savefig(imgfilepath, bbox_inches="tight", pad_inches=0)
