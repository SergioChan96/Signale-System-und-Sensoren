import pyaudio
import numpy as np

FORMAT=pyaudio.paInt16
SAMPLEFREQ=44100
FRAMESIZE=1024
NOFFRAMES=220

FILENAME='tief'
DEIN_NAME='Sergio'
RUN='5'


p=pyaudio.PyAudio()

def record():
    print('running')

    stream=p.open(format=FORMAT,channels=1,rate=SAMPLEFREQ,input=True,frames_per_buffer=FRAMESIZE)
    data=stream.read(NOFFRAMES*FRAMESIZE)
    decoded=np.fromstring(data, 'int16') / (2**10)/2

    # np.save(f'./records/{FILENAME}_{RUN}_{DEIN_NAME}.npy', decoded)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('done')

    start = np.argmax(np.abs(decoded) > 0.05 ) - 1024

    end = start + SAMPLEFREQ

    triggered = decoded[start:end]
    concat = np.concatenate((triggered, [0]*(SAMPLEFREQ - end - start)))

    np.save(f'./records/{FILENAME}_{RUN}_{DEIN_NAME}.npy', concat)


def main():
    record()


if __name__ == "__main__": main()