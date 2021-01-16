import math

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_sin_wave():
    time = 120
    x = range(time)
    y = [0]*time

    fig, ax = plt.subplots()
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 120)

    i=0
    while(True):
        y[i%time] = math.sin(math.pi*0.01*i)
        line, = ax.plot(x, y, color="b", marker='.', linestyle='None')
        plt.pause(1e-10)
        line.remove()
        i+=1

def plot_animation_sample():
    fig, ax = plt.subplots()
    ax.set_ylim(-5, 5)
    x = np.arange(0, 4*np.pi, 4*np.pi/44100)
    line, = ax.plot(x, np.sin(x))

    def animate(i):
        line.set_ydata(np.sin(x + i/10.0) + np.sin(x + i/9.0) + np.sin(x + i/7.0) )  # update the data
        return line,

    # Init only required for blitting to give a clean slate.
    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init, interval=25, blit=True)
    plt.show()

def plot_animation():
    fig = plt.figure()
    ax = fig.add_subplot(111, aspect=1)

    theta = np.linspace(0, 2*np.pi, 128)

    def update(f):
        ax.cla() # ax をクリア
        ax.grid()
        ax.plot(np.cos(theta), np.sin(theta), c="gray")
        ax.plot(np.cos(f), np.sin(f), "o", c="red")
        print(f)

    anim = animation.FuncAnimation(fig, update, frames=np.pi*np.arange(0,2,0.25), interval=200)

    plt.show()

def plot_rand():
    fig = plt.figure()
    ims = []
    
    for i in range(3):
        rand = np.random.randn(100) # 100個の乱数を作成
        
        img = plt.plot(rand) # グラフを作成
        plt.title("sample animation")
        plt.ylim(-10,10)
    
        ims.append(img) # グラフを配列に追加
        print(i)
    
    # 100枚のプロットを 100ms ごとに表示するアニメーション
    ani = animation.ArtistAnimation(fig, ims, interval=1000)
    plt.show()

def plot_wav():
    frame = 44100
    disp_range = 44100
    step = int(44100/4)
    interval = int(step/frame*1000)
    fig, ax = plt.subplots()
    ax.set_ylim(-33000, 33000)

    with open("voice_10s_left.bin", mode="rb") as f:
        data = np.fromfile(f, np.int16)
        length = len(data)
        print(length)
        print(int((length-disp_range)/step)*step-1)
        print(range(length-disp_range))
        i=0
        print(data[i:disp_range+i])

        x = np.arange(i*step/frame, (i*step+disp_range)/frame, disp_range/10/frame)
        ax.plot(np.arange(i*step, disp_range+i*step), data[i*step:disp_range+i*step])

        def hoge(i):
            ax.cla() # ax をクリア
            ax.set_ylim(-33000, 33000)
            x = np.arange(i*step, disp_range+i*step)/frame
            y = data[i*step:disp_range+i*step]
            x_label = np.arange(i*step/frame, (i*step+disp_range)/frame, disp_range/10/frame)
            x_label = [10, 20, 30]
            # plt.xticks(x, x_label)
            ax.plot(x, y)
            # ax.plot(np.arange(i*step, disp_range+i*step), data[i*step:disp_range+i*step])
            # print(i)

        ani = animation.FuncAnimation(fig, hoge, frames=np.arange(0,int((length-disp_range)/step)-1, 1), interval=interval)
        plt.show()
        

def main():
    # plot_sin_wave()
    # plot_animation()
    plot_animation_sample()
    # plot_rand()
    # plot_wav()

if __name__ == "__main__":
    main()