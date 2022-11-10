import time
from matplotlib import pyplot as plt
from scipy.fftpack import fft
import numpy as np

class fast_plot():

    def __init__(s, frames = 3200, spr=96000) -> None:

        t_frame = 1/(spr/frames)
        s.xt = np.linspace( start = 0, 
                            stop  = t_frame,
                            num   = frames)

        s.fig, s.ax = plt.subplots(nrows=2, ncols=1)
        s.fig.set_size_inches(15,15)
        s.text = s.fig.text(0.7,0.8, "")

        s.waveform, = s.ax[0].plot([], lw=3)
        s.ax[0].set_title('Waveform')
        s.ax[0].set_xlabel('Time (s)')
        s.ax[0].set_ylabel('Amplitude')
        s.ax[0].set_ylim([-1.1, 1.1])
        s.ax[0].set_xlim(0, t_frame)


        #s.ax1.set_xlim(s.x.min(), s.x.max())
        # s.ax[1].set_xscale('log')
        # s.ax[1].set_ylim([-1.1, 1.1])
        # s.ax[1].set_xlim(10**(-6), 10**(-5))

        s.nyquist_shannon = int(spr / 2)       
        s.xt_fft = np.arange(s.nyquist_shannon)
        s.plt_fft, = s.ax[1].plot([])      
        s.ax[1].set_title('Double Sided FFT - without FFTShift')
        s.ax[1].set_xlabel(f'Sample points (N-point DFT)')       
        s.ax[1].set_xscale('log') 
        s.ax[1].set_ylabel('DFT Values')
        s.ax[1].set_ylim([0, 600])
        s.ax[1].set_xlim(0, s.nyquist_shannon)

        s.fig.canvas.draw()   # note that the first draw comes before setting data 
        # cache the background => speed up fps
        s.ax0background = s.fig.canvas.copy_from_bbox(s.ax[0].bbox)
        s.ax1background = s.fig.canvas.copy_from_bbox(s.ax[1].bbox)

        plt.show(block=False)
        s.t_start = time.time()

    def update_plot(s, i, data, spr=96000):

        # show fps
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - s.t_start)) ) 
        s.text.set_text(tx)

        # display waveform
        s.waveform.set_data(s.xt, data)

        # display fft
        data = data.reshape(-1)
        sig_fft = np.abs(fft(data, spr))
        sig_fft = sig_fft[:s.nyquist_shannon]
        s.plt_fft.set_data(s.xt_fft, sig_fft)

        # plot ax0
        s.fig.canvas.restore_region(s.ax0background)
        s.ax[0].draw_artist(s.text)
        s.ax[0].draw_artist(s.waveform)
        s.fig.canvas.blit(s.ax[0].bbox)

        # plot ax1
        s.fig.canvas.restore_region(s.ax1background)
        s.ax[1].draw_artist(s.plt_fft)
        s.fig.canvas.blit(s.ax[1].bbox)

        s.fig.canvas.flush_events()


if __name__ == '__main__':
    fp = fast_plot()

    k = 0
    for i in range(1000):
        fp.update_plot(i, np.sin(3.+k))
        k+=0.11