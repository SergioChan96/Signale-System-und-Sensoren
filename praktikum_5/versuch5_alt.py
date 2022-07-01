# -*- coding: utf-8 -*-






import redlab as rl
import numpy as np
from time import sleep
from matplotlib import pyplot as plt

BOARD_NUM = 0
CHANNEL = 0
RANG = 1
RANG_OUT = 101
VALUES = 1000

ADWert = rl.cbAIn(0,0,1)
print("------- einzelne Werte -------------------------")
print(f"16 Bit Value: {str(rl.cbAIn(0,0,1))}")
print(f"Voltage Value: {str(rl.cbVIn(0,0,1))}" )
# print("------- Messreihe -------------------------")
# print(f"Messreihe: {str(rl.cbAInScan(0,0,0,300,8000,1))}")
# print(f"Messreihe: {str(rl.cbVInScan(0,0,0,300,8000,1))}" )
# print("------- Ausgabe -------------------------")



def write_to_board():
    try:
        val = float(input("Spannungswert eingeben:\n"))
        rl.cbVOut(BOARD_NUM, CHANNEL, RANG_OUT, val)
    except Exception as e:
        print(e)
    
    input("Press any key")
    
def zeug():
    sinwave = [np.sin(np.pi * 4 * (i/300)) for i in range(300)]
    values = 300
    for i in range(10):
        if i %10 == 0: print(f"###############{i}")
        for x in range(len(sinwave)):
            # print(sinwave[x]+1)
            rl.cbVOut(BOARD_NUM, CHANNEL, RANG_OUT, sinwave[x]+1)
            #sleep(0.1)
        
data = rl.cbVInScan(0,0,0,VALUES,8000,1)
print(data)
freq = "test"
np.savetxt(f"sinus_{freq}.csv", [x / 1000000000000000000 for x in data], delimiter=",")
plt.plot(data)
plt.savefig(f'sinus_{freq}.png')
plt.show()
