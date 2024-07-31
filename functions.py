import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames
import matplotlib.ticker as ticker

def gaussian(x, a, x0, sig, h):
    return a * np.exp(-(x - x0)**2 / (2 * sig**2)) + h

def GnL(x, a, x0, sig, b):
    return a * np.exp(-(x - x0)**2 / (2 * sig**2)) + b * np.cos(np.pi * (x - 40) / 180)

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