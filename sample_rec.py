#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = 0
stream = None

def pyaud():
    WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
    
    #基本情報の設定
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 32000
    CHUNK = 44100
    iDeviceIndex = 1
    targetDevice="C920"
    
    audio = pyaudio.PyAudio()
    # for i in range(audio.get_device_count()):
    #     if(targetDevice in audio.get_device_info_by_index(i)["name"]):
    #         iDeviceIndex = i
    #         print(audio.get_device_info_by_index(i))

    if(not targetDevice in audio.get_device_info_by_index(iDeviceIndex)["name"]):
        print("could not find "+targetDevice)
        for i in range(audio.get_device_count()):
            print(audio.get_device_info_by_index(i)["name"])
        exit(-1)
    print("iDeviceIndex : {0}".format(iDeviceIndex))
    print( audio.get_device_info_by_index(iDeviceIndex))
    
    global stream
    stream = audio.open(
        rate=RATE, 
        channels=CHANNELS, 
        format=FORMAT, 
        input=True, output=False, 
        input_device_index = iDeviceIndex,
        output_device_index = None,
        frames_per_buffer=CHUNK
    )

    #--------------録音開始---------------
    print ("recording...")

    numOfFrames = CHUNK
    global x 
    x = [0]*numOfFrames
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylim(-33000, 33000)
    line, = ax.plot(range(numOfFrames), [0]*numOfFrames)

    # mk.0
    # all = []
    # RECORD_SECONDS = 2
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    #     data = stream.read(CHUNK, exception_on_overflow = False)
    #     all.append(data)

    # mk.1
    while(True):
        data = stream.read(CHUNK)
        new_data = np.frombuffer(data, dtype=np.int16).tolist()
        x = x[CHUNK:] + new_data
        # line, = ax.plot(range(numOfFrames), x, color="b", marker='.', linestyle='None')
        line.set_ydata(x)
        fig.canvas.draw()
        fig.show()
        fig.canvas.flush_events()

    # mk.2
    # def init():
    #     print("init")
    #     line.set_ydata(np.ma.array(range(numOfFrames), mask=True))
    #     plt.pause(1)
    #     return line

    # def update(i):
    #     # print("update")

    #     global x
    #     global stream

    #     start = time.time()
    #     data = stream.read(CHUNK,  exception_on_overflow = False)

    #     x = x[CHUNK:] + np.frombuffer(data, dtype=np.int16).tolist()
    #     # pxx, freq, bins, t = plt.specgram(x,Fs = RATE)

    #     line.set_ydata(x)

    #     end = time.time()
    #     proctime=end-start
    #     interval = CHUNK/RATE
    #     # print(end-start)
    #     # print(interval)
    #     if(proctime < interval):
    #         time.sleep(interval-proctime)
    #     time.sleep(1e-3)

    #     return line
    
    # anim = animation.FuncAnimation(fig, update, init_func=init, interval=500)

    # plt.show()
    #--------------録音終了---------------
    stream.stop_stream()
    stream.close()
    audio.terminate()


def main():
    pyaud()
    # sounddev()

if __name__ == "__main__":
    main()