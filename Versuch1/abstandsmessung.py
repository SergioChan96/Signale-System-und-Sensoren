# -*- coding: utf-8 -*-

import numpy as np
import os
from io import StringIO
from matplotlib import pyplot as plt

folder = "."
file_filter = "^*\.csv$"

protocol_dist = [10, 13, 16, 19, 22, 25, 28, 31, 34, 37, 40, 43, 46, 49, 52, 55, 58, 61, 64, 67, 70]
protocol_vals = [1.337, 1.181, 1.045, 0.951, 0.8728, 0.8005, 0.7592, 0.6956, 0.6758, 0.6541, 0.6368, 0.6182, 0.5988,
                 0.5985,
                 0.5793, 0.5415, 0.5986, 0.5577, 0.5794, 0.5608, 0.5602]


def read_data(file):
    with open(f"{folder}/{file}", 'r') as data:
        plaintext = data.read()

        plaintext = plaintext.replace(',', '.')

        content = np.genfromtxt(StringIO(plaintext), delimiter=';', dtype=None, skip_header=1000)
        values = [entry[1] for entry in content]
        return values


def calc_data(values):
    return (np.mean(values), np.std(values))


def plot_data(results):
    mean_vals = []
    std_vals = []

    for entry in results:
        mean_vals.append(entry[0])
        std_vals.append(entry[1])

    axt[0].plot(protocol_dist, protocol_vals, label="mean protocol")
    axt[0].plot(protocol_dist, mean_vals, label="mean mesured")
    axt[0].plot(protocol_dist, std_vals, label="std mesured")
    axt[0].legend()


def modelling(values):
    # print(f"{values=}")
    global steigung
    global b
    v_ = lambda v: np.log(v)

    distances = [v_(val) for val in protocol_dist]
    measured_distances = [v_(val) for val in values]
    zipped = list(zip(distances, measured_distances))
    axt[1].scatter(measured_distances, distances)
    avgX = np.average(measured_distances)
    avgY = np.average(distances)

    # print(avgX, avgY)
    d = [((distance - avgY) * (measured_distance - avgX), (distance - avgY) ** 2) for distance, measured_distance in
         zipped]

    steigung = np.sum([val[0] for val in d]) / np.sum([val[1] for val in
                                                       d])  # E = np.sum(np.array([distance - (avgX * measured_distance) for distance, measured_distance in zipped]))
    b = avgX - (steigung * avgY)

    # print(b)
    # print(steigung)

    axt[1].plot(steigung * np.array([distance for distance, _ in zipped]) + b, [distance for distance, _ in zipped],
                label="regression")


def schaetzwert(vals):
    factor = 1.09  # depends on number of measures
    x_ = np.mean(vals)
    # x_ = 30
    s = np.std(vals, ddof=1)
    sx = s / np.sqrt(len(vals))
    x1 = x_ + factor * sx
    x2 = x_ - factor * sx

    def fehlerfortpfalnzung(vals):
        x__ = factor * sx  # delta X
        y__ = (steigung * np.exp(b) * x_ ** (steigung - 1)) * x__  # delta y
        y = np.exp(b) * x_ ** steigung
        y1 = y + y__
        y2 = y - y__
        # print(f"{np.exp(b)} * {x_} ** {steigung} = {y}")
        # print(y1, y2)
        return (y, y__)

    return fehlerfortpfalnzung(vals)
    # def fehlerfortpfalnzung():
    #     print((x_/np.exp(b))**(1/steigung))
    # fehlerfortpfalnzung()


def gaussFehler(long, short):
    return np.sqrt((short[0] * long[1]) ** 2 + (long[0] * short[1]) ** 2)


def main():
    global axt
    fig, axt = plt.subplots(2)
    files = [file for file in os.listdir(folder) if "cm.csv" in file]
    files.sort()
    values = [read_data(file) for file in files]
    results = [calc_data(value) for value in values]
    # results = (mean, std) of values of csv files
    plot_data(results)
    modelling([res[0] for res in results])

    plt.savefig("./measurement.png")

    # paperfiles = [file for file in os.listdir(folder) if "paper_" in file]
    # paperfiles.sort()
    # papervalues = [read_data(file) for file in paperfiles]
    # longVals = papervalues[0]
    # shortVals = papervalues[1]
    # longY = schaetzwert(longVals)
    # shortY = schaetzwert(shortVals)
    # gauss = gaussFehler(longY, shortY)
    # print(longY[0]*shortY[0] + gauss)
    # print(longY[0]*shortY[0] - gauss)


if __name__ == "__main__": main()