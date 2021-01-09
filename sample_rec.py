import sounddevice as sd
import wave
import time
import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style as mplstyle

def sounddev():
    sd.default.device = 11
    rate = 32000
    rate = 44100
    channel = 1
    t = 3

    print("start")

    data = sd.rec(frames=int(rate * t), samplerate=rate, channels=1)
    sd.wait()

    print("done")

    data = data / data.max() * np.iinfo(np.int16).max
    data = data.astype(np.int16)

    FILE_NAME="rec.wav"
    with wave.open(FILE_NAME, mode='wb') as wb:
        wb.setnchannels(1)  # モノラル
        wb.setsampwidth(2)  # 16bit=2byte
        wb.setframerate(rate)
        wb.writeframes(data.tobytes())  # バイト列に変換

x = 0

def pyaud():
    RECORD_SECONDS = 2 #録音する時間の長さ（秒）
    WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
    iDeviceIndex = 11 #録音デバイスのインデックス番号
    
    #基本情報の設定
    FORMAT = pyaudio.paInt16 #音声のフォーマット
    CHANNELS = 1             #モノラル
    RATE = 44100             #サンプルレート
    # RATE = 44100             #サンプルレート
    CHUNK = int(RATE/5)         #データ点数
    audio = pyaudio.PyAudio() #pyaudio.PyAudio()
    
    stream = audio.open(format=FORMAT, channels=CHANNELS,
            rate=RATE, input=True,
            input_device_index = iDeviceIndex, #録音デバイスのインデックス番号
            frames_per_buffer=CHUNK)
    # stream = audio.open(format=FORMAT, channels=CHANNELS,
    #         rate=RATE, input=True,
    #         input_device_index = iDeviceIndex #録音デバイスのインデックス番号
    #         )
    
    #--------------録音開始---------------
    
    print ("recording...")
    numOfFrames = RATE*2
    global x 
    x = [0]*numOfFrames
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim(-33000, 33000)
    line, = ax.plot(range(numOfFrames), [0]*numOfFrames)
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):

    # mk.1
    # while(True):
    #     data = stream.read(CHUNK)
    #     # frames.append(data)
    #     # print(data)
    #     # print(type(data))
    #     x = x[CHUNK:] + np.fromstring(data, dtype=np.int16).tolist()
    #     line, = ax.plot(range(numOfFrames), x, color="b", marker='.', linestyle='None')
    #     plt.pause(1e-10)
    #     line.remove()

    # mk.2
    def init():
        line.set_ydata(np.ma.array(range(numOfFrames), mask=True))
        return line

    def update(i):
        global x
        start = time.time()
        data = stream.read(CHUNK)
        end = time.time()
        # print(end-start)
        x = x[CHUNK:] + np.fromstring(data, dtype=np.int16).tolist()
        line.set_ydata(x)
        return line
    
    anim = animation.FuncAnimation(fig, update, init_func=init)

    plt.show()
    print("hoge")
    exit(1)
    print ("finished recording")
    
    #--------------録音終了---------------
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()


def main():
    pyaud()
    # sounddev()

if __name__ == "__main__":
    main()