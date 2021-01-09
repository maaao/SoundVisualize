import wave
import scipy
import matplotlib.pyplot as plt
import struct
import numpy as np

class wavedit():
    def __init__(self, filename):
        self.wf = wave.open(filename)
        data = self.wf.readframes(self.wf.getnframes())
        num_data = np.fromstring(data, dtype="int16")

        if(self.wf.getnchannels() == 2):
            self.left = num_data[::2]
            self.right= num_data[1::2]
        else:
            self.left = num_data
            self.right = [0]*len(num_data)
    
    def showParams(self):
        print("channels : "+str(self.wf.getnchannels()))
        print("width : " + str(self.wf.getsampwidth()))
        print("framerate : " + str(self.wf.getframerate()))
        print("nframes : " + str(self.wf.getnframes()))
        print("compname : " + str(self.wf.getcompname()))

    def getnchannels(self):
        return self.wf.getnchannels()
    
    def getsampwidth(self):
        return self.wf.getsampwidth()
    
    def getframerate(self):
        return self.wf.getframerate()
    
    def getnframes(self):
        return self.wf.getnframes()

    def saveMonoWav(self, filename_left="left.wav", filename_right="right.wav"):
        channels = self.wf.getnchannels()
        width = self.wf.getsampwidth()
        framerate = self.wf.getframerate()
        nframes = self.wf.getnframes()
        compname = self.wf.getcompname()

        wf = wave.open(filename_left, "wb")

        wf.setparams([1, width, framerate, nframes, "NONE", compname])
        wf.writeframes(self.left.tobytes())
        wf.close()

        if(channels == 2):
            wf = wave.open(filename_right, "wb")
            wf.setparams([1, width, framerate, nframes, "NONE", compname])
            wf.writeframesraw(self.right.tobytes())
            wf.close()
    
    def getBinData(self):
        return self.left.tobytes(), self.right.tobytes()

def main():
    filename = "voice_10s.wav"

    we = wavedit(filename)
    we.showParams()
    we.saveMonoWav()
    bin_l, bin_r = we.getBinData()
    
    fig, ax = plt.subplots()
    ax.set_ylim(-33000, 33000)
    data_l = np.fromstring(bin_l, dtype="int16")
    print(data_l)
    ax.plot(range(len(data_l)), data_l)
    plt.show()

if __name__ == '__main__':
    main()
    