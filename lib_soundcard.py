import soundcard as sc
import time

from scipy.io import wavfile as wav
from scipy.fftpack import fft
import numpy as np
import sin_fft

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

def loop_back():
    s_tinka = sc.get_speaker('Tinka')
    print(s_tinka)

    #m_tinka = sc.get_microphone("Tinka")
    m_tinka = sc.default_microphone()
    print(m_tinka)

    # 96000spr/s / 30f/s = 3200frames 
    spr = 96000
    frames = 3200

    fp = plt.fast_plot(frames, spr)

    with m_tinka.recorder(samplerate=spr, channels=[-1]) as mic, \
        s_tinka.player(samplerate=spr) as sp:
        for i in range(10000):
            
            # data.shape = (frames, channel)
            data = mic.record(numframes=int(frames))

            #sp.play(data)

            fp.update_plot(i, data)

            #print(f'{time.time():3.1f} {len(data)} {len(fft_out)}')

if __name__ == '__main__':
    loop_back()
    #fft_sin()

        

