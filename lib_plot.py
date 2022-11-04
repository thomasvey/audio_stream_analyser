import time
from matplotlib import pyplot as plt
import numpy as np

class fast_plot():

    def __init__(s, frames) -> None:
        s.x = np.linspace(0,20000., num=frames)

        #W = fftfreq(y.size, d=x[1]-x[0])

        #s.X,s.Y = np.meshgrid(s.x,s.x)
        s.fig = plt.figure()
        
        s.ax1 = s.fig.add_subplot(1, 1, 1)
        
        s.line, = s.ax1.plot([], lw=3)
        s.text = s.ax1.text(0.8,0.5, "")

        #s.ax1.set_xlim(s.x.min(), s.x.max())
        s.ax1.set_ylim([-1.1, 1.1])
        s.ax1.set_xscale('log')
        s.ax1.set_xlim(10**(-6), 10**(-5))


        s.fig.canvas.draw()   # note that the first draw comes before setting data 

        # cache the background => speed up fps
        s.axbackground = s.fig.canvas.copy_from_bbox(s.ax1.bbox)

        plt.show(block=False)
        s.t_start = time.time()

    def update_plot(s, i, data):
        
        s.line
        s.line.set_data(s.x, data)
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - s.t_start)) ) 
        s.text.set_text(tx)
        #print tx
        
        
        
        # restore background => speedup fps
        s.fig.canvas.restore_region(s.axbackground)
        
        # redraw just the points
        s.ax1.draw_artist(s.line)
        s.ax1.draw_artist(s.text)
        
        # fill in the axes rectangle
        s.fig.canvas.blit(s.ax1.bbox)

        s.fig.canvas.flush_events()

if __name__ == '__main__':
    fp = fast_plot()

    k = 0
    for i in range(1000):
        fp.update_plot(i, np.sin(3.+k))
        k+=0.11