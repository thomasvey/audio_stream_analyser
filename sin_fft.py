import numpy as np
from scipy.fftpack import fft
import pylab as plt


def sine_wave(  freq        = 100,
                samplerate  = 48000,
                phase       = 0,
                frames      = 1):
    """
    Generate sine wave signal with the following parameters
    Parameters:
        freq : frequency of sine wave in Hertz
        overSR : oversampling rate (integer)
        phase : desired phase shift in radians
        nCyl : number of cycles of sine wave to generate
    Returns:
        (xt,sig) : time base (t) and the signal g(t) as tuple
    """

    xt = np.linspace(start= 0, 
                     stop = 2*np.pi*frames,
                     num=samplerate*frames)
    
    # w = 2pi/T = 2pi*f
    # sin(w * t)
    # sin(2pi* f * t)
    # sin(2pi* f / s*t)
    
    sig = np.sin(xt * freq + phase)
    
    return (xt,sig)

def plot(xt, sig, samplerate=48000):
    fig1, ax = plt.subplots(nrows=2, ncols=1)

    print(f'xlen {len(xt)} slen{len(sig)}')
    ax[0].plot(xt, sig)                         #TODO: time is wrong
    ax[0].set_title('Sine wave')
    ax[0].set_xlabel('Time (s)')
    ax[0].set_ylabel('Amplitude')

    sig_fft=np.abs(fft(sig,samplerate))         #TODO: there is always a frequenz present about 100K?? 

    # m = max(sig_fft)
    # print(f'max: {m} | len {len(sig_fft)}')
    # for i, v in enumerate(sig_fft):
    #     if(v > m-20 or i > n_FFT-10):
    #         print(f'{i} : {v:.2f}')

    ax[1].plot(np.arange(samplerate), sig_fft)      
    ax[1].set_title('Double Sided FFT - without FFTShift')
    ax[1].set_xlabel(f'Sample points (N-point DFT)')       
    ax[1].set_xscale('log') 
    ax[1].set_ylabel('DFT Values')

    fig1.set_size_inches(15,15)
    fig1.show()

if __name__ == '__main__':
    xt,sig0 = sine_wave(freq = 20)
    xt,sig1 = sine_wave(freq = 100)
    xt,sig2 = sine_wave(freq = 130)
    xt,sig3 = sine_wave(freq = 1000)
    xt,sig4 = sine_wave(freq = 16000)

    sig = sig0 + sig1 + sig2 + sig3 + sig4

    plot(xt, sig)

    input()