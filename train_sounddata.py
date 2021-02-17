import wave
import random 

import cv2
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

import librosa
import librosa.display

def record(label, num, istrain):
    if(istrain):
        filename = "data/wav/train/{0}/{1}.wav".format(label, num)
    else:
        filename = "data/wav/test/{0}/{1}.wav".format(label, num)

    RATE = 48000
    CHANNELS = 1
    FORMAT = pyaudio.paInt16
    CHUNK = 1024
    REC_TIME=1.5 # 1.5s
    audio = pyaudio.PyAudio()
    stream = audio.open(
        rate=RATE,
        channels=CHANNELS,
        format=FORMAT,
        input=True,
        output=False,
        frames_per_buffer=CHUNK
    )

    numOfData = RATE * REC_TIME

    data_sound = []
    
    for i in range(0, int(numOfData/CHUNK)):
        data_sound.append(stream.read(CHUNK))

    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    with wave.open(filename, mode="wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setframerate(RATE)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.writeframes(b''.join(data_sound))

def saveasimage(label, num, istrain):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.axis("off")

    if(istrain):
        wavfilepath = "data/wav/train/{0}/{1}.wav".format(label, num)
    else:
        wavfilepath = "data/wav/test/{0}/{1}.wav".format(label, num)

    y, sr = librosa.load(wavfilepath, dtype=np.int16)

    n_fft = 512
    S = np.abs(librosa.stft(y, n_fft=n_fft))

    S_db = librosa.amplitude_to_db(S, ref=np.max)

    min_var = -80
    max_var = 0
    img = librosa.display.specshow(S_db, sr=sr, vmin=min_var, vmax=max_var, cmap=cm.hsv, ax=ax)
    fig.set_tight_layout(True)

    if(istrain):
        imgfilepath = "data/images/train/{0}/{1}.png".format(label, num)
    else:
        imgfilepath = "data/images/test/{0}/{1}.png".format(label, num)

    fig.savefig(imgfilepath, bbox_inches="tight", pad_inches=0)


def main():
    words = ["denki", "tsukete", "keshite", "senpuki", "eakon"]
    counter = [0]*len(words)

    istrain = False
    numOfData = 35
    while True:
        id = random.randint(0,len(words)-1)
        if(sum(counter)//len(words) == numOfData ):
            break

        if(counter[id] < numOfData):
            img = np.full((300, 400, 3), random.randint(0, 255), np.uint8)
            cv2.putText(img, words[id], (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 0, 255), thickness=5)
            cv2.imshow("img", img)
            cv2.waitKey(1)
        
            record(label=words[id], num=counter[id], istrain=istrain)
            saveasimage(label=words[id], num=counter[id], istrain=istrain)
            counter[id] +=1

        print("電気 : {0} つけて : {1} 消して : {2} 扇風機 : {3} エアコン : {4}".format(counter[0], counter[1], counter[2], counter[3], counter[4]))

if __name__ == '__main__':
	main()