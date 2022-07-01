# -*- coding: utf-8 -*-
import numpy as np
import pyaudio as ad
from matplotlib import pyplot as plt



FORMAT = ad.paInt16
SAMPLEFREQ = 44100
FRAMESIZE = 1024
NOFFRAMES = 220



def record(name):
    p = ad.PyAudio()
    stream = p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,
                input=True,frames_per_buffer=FRAMESIZE)



    data = stream.read(NOFFRAMES*FRAMESIZE)
    decoded = np.fromstring(data, 'Int16')

    np.save(f"./{name}", decoded)


    start = 10000 # cut the first n values off

    #trigger = decoded[start:start+SAMPLEFREQ]

    stream.stop_stream()
    stream.close()
    p.terminate()
    print(f"recording of '{name}'")
    
    fig, axs = plt.subplots(2)
    count = 0
    start = 0
    # start slicing if signal is greater than x
    for i in decoded[0:len(decoded)]:
        if i > 2000:
            start = count
            break
        count = count+1
    # sliced values
    sliced=np.array(decoded)[start:start+SAMPLEFREQ]
    # if less than SAMPLEFREQ values, append zeros
    if len(sliced) < SAMPLEFREQ:
        missing_num = SAMPLEFREQ - len(sliced)
        for i in range(missing_num):
            np.append(sliced,0)
    
    axs[0].plot(sliced)
    #axs[0].plot(trigger)
    axs[1].plot(transform(sliced))
    axs[0].set(ylabel="amp")
    axs[1].set(xlabel="freq")
    plt.show()
    
    
    
    
def windowing():
    
    
def transform(data):
    four = np.fft.fft(data)
    return abs(four[:int(len(four)/2+1)])
    
    
    
    
def main():
    record("links")

    
    
if __name__ == "__main__": main()



# https://www.cbcity.de/die-fft-mit-python-einfach-erklaert