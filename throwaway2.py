import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames
import matplotlib.ticker as ticker
from throwaway1 import readMeas

#240716

hypoList = [10.8, 10.7, 10.8, 10.7, 10.7, 10.6, 10.5, 10.6, 10.6, 10.6, 11.5]
oppoList = [0, 1.7, 2.8, 4.2, 5.5, 6.8, 7.9, 9, 9.8, 10.4, 10.7]

angleList = []
for i in range(len(hypoList)-1):
    angleList.append(np.arcsin(oppoList[i] / hypoList[i]) * (180 / np.pi))
angleList.append(180 - np.arcsin(oppoList[-1] / hypoList[-1]) * (180 / np.pi))



def main():
    print(angleList)

if __name__ == '__main__':
    main()