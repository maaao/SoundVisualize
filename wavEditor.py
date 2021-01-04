import wave
import scipy
import matplotlib.pyplot as plt
import struct
import numpy as np

class wavedit():
    def __init__(self, filename):
        self.wf = wave.open(filename)
    
    def getParams(self):
        channels = self.wf.getnchannels()
        width = self.wf.getsampwidth()
        framerate = self.wf.getframerate()
        nframes = self.wf.getnframes()
        compname = self.wf.getcompname()

        print("channels : "+str(channels))
        print("width : " + str(width))
        print("framerate : " + str(framerate))
        print("nframes : " + str(nframes))
        print("compname : " + str(compname))

        return channels, width, framerate, nframes, compname

    def convToMono(self):
        data = self.wf.readframes(self.wf.getnframes())
        print(data)
        num_data = scipy.fromstring(data, dtype="int16")

        if(self.wf.getnchannels() == 2):
            self.left = num_data[::2]
            self.right= num_data[1::2]
        else:
            self.left = num_data
            self.right = [0]*len(num_data)

        print(self.left)
        

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
        channels, width, framerate, nframes, compname = self.getParams()
        wf = wave.open("left.wav", "wb")
        
        print(type(self.left))

        # Fixme : self.left は現状numpy.ndarray型のため、byte型に変換する必要がある。
        #         http://www.kurigohan.com/article/20180921_python_sine_wave.html
        wf.setparams([1, width, framerate, nframes, "NONE", compname])
        wf.writeframes(data)
        wf.close()

        wf = wave.open("right.wav", "wb")
        wf.setparams([1, width, framerate, nframes, "NONE", compname])
        wf.writeframesraw(self.right)
        wf.close()


def main():
    filename = "voice_10s.wav"
    we = wavedit(filename)
    # we.getParams()
    we.convToMono()
    we.plotWave()  
    we.saveMonoWav()

if __name__ == '__main__':
    main()
    