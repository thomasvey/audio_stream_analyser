import soundcard as sc
import time

from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np

import lib_plot as plt

def print_speaker():
    # get a list of all speakers:
    speakers = sc.all_speakers()
    for s in speakers:
        print(s)
    print('-'*30)

def print_mic():
    #get a list of all microphones:
    mics = sc.all_microphones()
    for m in mics:
        print(m)
    print('-'*30)

def generate_sin(sample_rate, freq=100):
    start_time = 0
    end_time = 1
    time = np.arange(start_time, end_time, 1/sample_rate)
    theta = 0
    amplitude = 1
    return amplitude * np.sin(2 * np.pi * freq * time + theta)
    
def fft_sin():
    sample_rate = 4096

    fp = plt.fast_plot(sample_rate)
    for i in range(10000):
        data = generate_sin(sample_rate, freq=i)
        fft_out = fft(data)
        fp.update_plot(i, np.abs(fft_out))

def loop_back():
    s_tinka = sc.get_speaker('Tinka')
    print(s_tinka)

    #m_tinka = sc.get_microphone("Tinka")
    m_tinka = sc.default_microphone()
    print(m_tinka)

    frames = 4096

    fp = plt.fast_plot(frames)
    with m_tinka.recorder(samplerate=48000) as mic, \
        s_tinka.player(samplerate=48000) as sp:
        for i in range(10000):
            data = mic.record(numframes=int(frames/2))
            sp.play(data)

            fft_out = fft(data)
            fp.update_plot(i, np.abs(fft_out))
            print(f'{time.time():3.1f} {len(data)} {len(fft_out)}')

if __name__ == '__main__':
    #loop_back()
    fft_sin()

        

