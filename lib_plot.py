import time
from matplotlib import pyplot as plt
from scipy.fftpack import fft
import numpy as np
import matplotlib.cm as cm

class fast_plot():

    sub_sampling = 10
    frame_ss = 3200/sub_sampling
    
    def __init__(s, spr=96000, frame = 3200, disp_win=1, audio_ch=1) -> None:

        # some math and create buff
        s.frame_ss = int(frame / s.sub_sampling)
        t_frame = 1/(spr/frame) 
        s.num_fames = (spr * disp_win) / frame

        # Waveform
        s.wave_buffer = np.zeros([int(s.frame_ss*s.num_fames),audio_ch], dtype=int)
        print(np.shape(s.wave_buffer))
        
        s.xt = np.linspace( start = 0, 
                            stop  = int(t_frame*s.num_fames),
                            num   = int(s.frame_ss*s.num_fames))

        s.fig, s.ax = plt.subplots(nrows=2, ncols=1)
        s.fig.set_size_inches(15,15)
        s.text = s.fig.text(0.7,0.8, "")

        s.waveform, = s.ax[0].plot([], lw=3)
        s.ax[0].set_title('Waveform')
        s.ax[0].set_xlabel('Time (s)')
        s.ax[0].set_ylabel('Amplitude')
        s.ax[0].set_ylim([-1.1, 1.1])
        s.ax[0].set_xlim(0, int(t_frame*s.num_fames))


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
        
    def update_plot(s, i, data, spr=96000, frame=3200):

        t0 = time.time()
        # show fps
        tx = 'Mean Frame Rate:\n {fps:.3f}FPS'.format(fps= ((i+1) / (time.time() - s.t_start)) ) 
        s.text.set_text(tx)
        
        # fill ring buffer
        s.wave_buffer = s.wave_buffer[s.frame_ss:]
        s.wave_buffer = np.append(s.wave_buffer, data[::s.sub_sampling])

        # display waveform
        s.waveform.set_data(s.xt, s.wave_buffer)

        # plot ax0 -- wafeform
        s.fig.canvas.restore_region(s.ax0background)
        s.ax[0].draw_artist(s.text)
        s.ax[0].draw_artist(s.waveform)
        s.fig.canvas.blit(s.ax[0].bbox)
        
        t1 = time.time()
        
        # display fft
        data = data.reshape(-1)
        sig_fft = np.abs(fft(data, spr))
        sig_fft = sig_fft[:s.nyquist_shannon]
        s.plt_fft.set_data(s.xt_fft, sig_fft)

        # plot ax1 - fft
        s.fig.canvas.restore_region(s.ax1background)
        s.ax[1].draw_artist(s.plt_fft)
        s.fig.canvas.blit(s.ax[1].bbox)

        t2 = time.time()
        
        s.fig.canvas.flush_events()
        
        t3 = time.time()
        
        e1 = t1 - t0
        e2 = t2 - t1
        e3 = t3 - t2
        print(f'wave {e1:.4f} \t fft {e2:.4f} \t show {e2:.4f}',end='')


if __name__ == '__main__':
    fp = fast_plot()

    k = 0
    for i in range(1000):
        fp.update_plot(i, np.sin(3.+k))
        k+=0.11