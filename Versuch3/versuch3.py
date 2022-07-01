# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:04:24 2022

@author: Sergio Chan
@auhor: Eik Hoffmann
"""
import math

import numpy as np
from io import StringIO
from matplotlib import pyplot as plt
frequency = [100, 200, 300, 400, 500, 700, 850, 1000, 1200, 1500, 1700, 2000, 3000, 4000, 5000, 6000, 10000]
amplitudeInputSmall = [14.41, 22.27, 31.01, 54.6, 116, 54.07, 47.96, 45.35,  33.14, 34.88, 31.39, 35.82, 40.99, 30.52, 34.01, 13.95, 20.93]
amplitudeOutputSmall = [1559, 1490, 1507, 1490, 1490, 1507, 1490, 1490, 1490, 1490, 1490, 1490, 1490, 1490, 1490, 1519, 1519]
phasengangSmall = [3.701, 2.884, 2.204, 1.85, 1.769, 1.605, 1.306, 1.197, 1.034, 1.524, 1.306, 1.17, 1.143, 1.129, 1.163, 1.115, 1.053]
amplitudeInputLarge = [71.52, 174.3, 130.7, 99.33, 81.9, 64.47, 64.47, 73.19, 64.47, 67.96, 64.47, 67.96, 74.93, 50.54, 38.33, 33.1, 36.59]
amplitudeOutputLarge = [1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1519, 1477]
phasengangLarge = [4.917, 4.4, 3.366, 2.713, 2.251, 1.679, 1.326, 1.175, 1.01, 0.8314, 0.7285, 0.6461, 0.4952, 0.3991, 0.3579, 0.3030, 0.2378]
folder="."
mundharmonika = "sound_part1.csv"

def read_data(file):
    with open(f"{folder}/{file}", 'r') as data:
        plaintext = data.read()
        
        plaintext = plaintext.replace(",", ".")
        
        content = np.genfromtxt(StringIO(plaintext), delimiter=";", dtype=None, skip_header=1000)
        
        return (np.array([entry[0] for entry in content]), np.array([entry[1] for entry in content]))
    
    
def plot_data(values, splot):
    splot.plot(values[0], values[1])
    
    
def fourrier_transform(values):
    return np.fft.fft(values)

def toPhasenwinkel(phasenwinkel):
    results = []
    for i in range(len(phasenwinkel)):
        results.append(-phasenwinkel[i]*frequency[i]*360)
    return results

def calcDecibels(voltagesInput, voltagesOutput):
    #power_db = 20 * log10(amp / amp_ref);
    db = []
    for i in range(len(voltagesInput)):
        db.append(20*math.log10(voltagesInput[i]/voltagesOutput[i]))
    return db
    
def main():
    #aufgabe 1
    sound1 = read_data(mundharmonika)

    global axt
    #deltaT = abs(sound1[1:])
    #1.25ms
    fourrier_vals = fourrier_transform(sound1[0])
    plt.plot(sound1[0], sound1[1], 'b')
    plt.ylabel('Spannung in mV')
    plt.xlabel('Zeit in ms')
    plt.xlim(0, 3)
    plt.grid(True)
    plt.show()
    funcAmplitude = np.vectorize(lambda x: np.abs(x))
    frequenzcalc = np.vectorize(lambda x: round(x / (sound1[0][-1] / ((len(sound1)) * 1000) * len(sound1))))
    fourier = np.fft.fft(sound1[1])
    frequenzspektrum = np.array(funcAmplitude(fourier), dtype=int)
    frequenzen = np.array(range(1, len(fourier) + 1), dtype=int)
    frequenzen = frequenzcalc(frequenzen)
    plt.plot(frequenzen[:400], frequenzspektrum[:400], 'b')
    plt.title("Curve")
    print("Grundfrequenz: ", frequenzen[np.argmax(frequenzspektrum[:60])], "Hz")
    print("Stärkste Frequenz: ", frequenzen[np.argmax(frequenzspektrum)], "Hz")
    #dauer = np.max(sound1[0]) + np.min(sound1[0])
    #timeAxis = sound1[0]
    #delta_t = np.abs(timeAxis[1] - timeAxis[0])
    #print(f'frequenz \t\t ', np.argmax(sound1[1]) / dauer * delta_t)
    #spectrum = np.fft.fft(sound1[1])
    #freq = np.fft.fftfreq(len(spectrum))
    #plt.plot(freq, abs(spectrum))
    #plt.plot(spectrum)
    #freq = range(0, 10003, 1) / (Signalänge * deltaT)
    #axt[1].plot(freq)
    #plt.show()

    # aufgabe 2
    fig, spl = plt.subplots(2)
    spl[0].semilogx(calcDecibels(amplitudeInputSmall, amplitudeOutputSmall))
    spl[0].semilogx(calcDecibels(amplitudeInputLarge, amplitudeOutputLarge))
    spl[1].semilogx(toPhasenwinkel(phasengangSmall))
    spl[1].semilogx(toPhasenwinkel(phasengangLarge))
    plt.show()

if __name__ == "__main__": main()