import wave
import scipy
import matplotlib.pyplot as plt
import struct
import numpy as np

class wavedit():
    def __init__(self, filename):
        self.wf = wave.open(filename)
    
    def showParams(self):
        print("channels : "+str(self.wf.getnchannels()))
        print("width : " + str(self.wf.getsampwidth()))
        print("framerate : " + str(self.wf.getframerate()))
        print("nframes : " + str(self.wf.getnframes()))
        print("compname : " + str(self.wf.getcompname()))

    def convToMono(self):
        data = self.wf.readframes(self.wf.getnframes())
        num_data = np.fromstring(data, dtype="int16")

        if(self.wf.getnchannels() == 2):
            self.left = num_data[::2]
            self.right= num_data[1::2]
        else:
            self.left = num_data
            self.right = [0]*len(num_data)

    def plotWave(self):
        # left channel
        plt.subplot(2, 1, 1)
        plt.plot(self.left,label="left")
        plt.legend()

        # right channel
        plt.subplot(2, 1, 2)
        plt.plot(self.right,label="right")
        plt.legend()
        plt.show()

    def saveMonoWav(self):
        channels = self.wf.getnchannels()
        width = self.wf.getsampwidth()
        framerate = self.wf.getframerate()
        nframes = self.wf.getnframes()
        compname = self.wf.getcompname()

        wf = wave.open("left.wav", "wb")
        
        wf.setparams([1, width, framerate, nframes, "NONE", compname])
        wf.writeframes(self.left.tobytes())
        wf.close()

        if(channels == 2):
            wf = wave.open("right.wav", "wb")
            wf.setparams([1, width, framerate, nframes, "NONE", compname])
            wf.writeframesraw(self.right.tobytes())
            wf.close()


def main():
    filename = "wav/voice_10s.wav"
    filename = "hoge.wav"
    we = wavedit(filename)
    we.showParams()
    we.convToMono()
    we.plotWave()  
    we.saveMonoWav()

if __name__ == '__main__':
    main()
    