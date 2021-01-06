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

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))

    def animate(i):
        plt.pause(2)
        line.set_ydata(np.sin(x + i/10.0))  # update the data
        return line,

    # Init only required for blitting to give a clean slate.
    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    ani = animation.FuncAnimation(fig, animate, np.arange(1, 200), init_func=init,
                                interval=25, blit=True)
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


def main():
    # plot_sin_wave()
    # plot_animation()
    plot_animation_sample()

if __name__ == "__main__":
    main()