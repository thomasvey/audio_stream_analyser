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
    mics = sc.all_microphones(include_loopback=True)
    for m in mics:
        print(m)
    print('-'*30)

def loop_back():

    mic_name = "Speaker"
    mic_name = "Monitor of LE-Tinka"
    #m_tinka = sc.get_microphone(mic_name, include_loopback=True)
    
    m_tinka = sc.default_microphone()
    print(m_tinka)

    #s_tinka = sc.get_speaker('Tinka')
    #print(s_tinka)

    # 96000spr/s / 30f/s = 3200frames 
    fps = 30        # plot frame rate
    spr = 48000     # Messpunktabstand
    frame = int(spr/fps) # Messpunktfreihe
    disp_win = 5    # anzuzeigendes Zeitfenster in s
    
    fp = plt.fast_plot(spr, frame, disp_win)

    with m_tinka.recorder(samplerate=spr, channels=[-1]) as mic: #, \
        #s_tinka.player(samplerate=spr) as sp:
    
        print(1/fps)
        for i in range(10000):
            t0 = time.time()    
            # data.shape = (frames, channel)
            data = mic.record(numframes=int(frame))
            
            t1 = time.time()
            #time.sleep(0.03)
            #sp.play(data)

            fp.update_plot(i, data, spr, frame)
            t2 = time.time()            
            #print(f'{time.time():3.1f} {len(data)} {len(fft_out)}')
            
            e0 = t2 - t0
            e1 = t1 - t0
            e2 = t2 - t1
            if(e1 < 0.0001):
                print("Warning: Programm to slow")
            
            print(f'\t| total {e0:.4f}\t rec{e1:.4f} \t plot {e2:.4f}')

if __name__ == '__main__':
    #print_mic()
    loop_back()
    #fft_sin()

        

