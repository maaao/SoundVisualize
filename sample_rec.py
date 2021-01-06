import sounddevice as sd
import wave
import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt

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

def pyaud():
    RECORD_SECONDS = 2 #録音する時間の長さ（秒）
    WAVE_OUTPUT_FILENAME = "sample.wav" #音声を保存するファイル名
    iDeviceIndex = 11 #録音デバイスのインデックス番号
    
    #基本情報の設定
    FORMAT = pyaudio.paInt16 #音声のフォーマット
    CHANNELS = 1             #モノラル
    RATE = 32000             #サンプルレート
    # RATE = 44100             #サンプルレート
    CHUNK = 1024           #データ点数
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
    numOfFrames = RATE*10
    frames = [0]*numOfFrames
    i=0
    # for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    while(True):
        data = stream.read(2)
        # frames.append(data)
        print(data)
        print(type(data))
        frames[i]=struct.unpack("<h", data)
        plt.plot(range(numOfFrames), frames)
        plt.pause(0.01)
        i+=1    
    
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