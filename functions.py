import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames
import matplotlib.ticker as ticker
from scipy import stats

def sphericalGaussian(x, a, d, w):
    return a * np.exp(w * (np.cos((np.pi*(x-d)/180)) - 1))

def gaussian(x, a, x0, sig, h):
    return a * np.exp(-(x - x0)**2 / (2 * sig**2)) + h

def doubleGaussian(x, a0, x0, sig0, a1, x1, sig1, h):
    return a0 * np.exp(-(x - x0)**2 / (2 * sig0**2)) + a1 * np.exp(-(x - x1)**2 / (2 * sig1**2)) + h

def GnL(x, a, x0, sig, b):
    return a * np.exp(-(x - x0)**2 / (2 * sig**2)) + b * np.cos(np.pi * (x - 40) / 180)

def dGnL(x, a0, x0, sig0, a1, x1, sig1, b):
    return a0 * np.exp(-(x - x0)**2 / (2 * sig0**2)) + a1 * np.exp(-(x - x1)**2 / (2 * sig1**2)) + b * np.cos(np.pi * (x - 40) / 180)

def readMeas(fileNameList:list):
    """Returns dict of current in mA, power and 2*std in uW. Keys are 0, 1, 2, ...\n
    Deletes first row of file and assumes ', ' separator"""
    filesDict = {}
    #fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
    for i in range(len(fileNameList)):
        currTemp = []
        measTemp = []
        stdTemp = []
        with open(fileNameList[i], 'r') as file:
            for row in file:
                points = row.strip().split(', ')
                currTemp.append(points[0])
                measTemp.append(points[1])
                stdTemp.append(points[2])
            currTemp.remove(currTemp[0])
            measTemp.remove(measTemp[0])
            stdTemp.remove(stdTemp[0])
            if currTemp[0] != '-':
                filesDict[i] = ([float(point)*1e3 for point in currTemp], [float(point)*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
            else:
                filesDict[i] = (currTemp, [float(point)*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
    return filesDict