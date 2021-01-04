import sounddevice as sd
import wave
import numpy as np

sd.default.device = 7
rate = 44100
channel = 2
t = 3

print("start")
data = sd.rec(frames=int(rate * t), samplerate=rate, channels=2)
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