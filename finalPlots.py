import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename, askopenfilenames
from FileHandler import ReadJson

#FINAL PLOTS FOR GRADU
#direct uv current sweep with and without filter
#   uv current sweep, filtered sweep, 
#   angle distribution with and without filter, combined conversion dist

#blue angle distribution
#blue specular peak height as function of coating thickness (relative?)
#blue Riemann sum as function of coating thickness

#Riemann sum of combined conversion dist as a function of coating thickness


def readCurrentSweepData():
    """Returns dict with angle key and [currentList, powerList, stdList]"""
    """Reads current in mA, power and std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
    fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
    for i in range(len(fileNameList)):
        currTemp = []
        measTemp = []
        stdTemp = []
        filesDict = {}
        with open(fileNameList[i], 'r') as file:
            rows = list(file)
            rows.pop(0)
            for row in rows:
                points = row.strip().split(', ')
                currTemp.append(points[1])
                measTemp.append(points[2])
                stdTemp.append(points[3])
                angle = int(points[0])
            if currTemp[0] != '-':
                filesDict[angle] = ([float(point) for point in currTemp], [float(point) for point in measTemp], [float(point) for point in stdTemp])
            else:
                filesDict[angle] = (currTemp, [float(point) for point in measTemp], [float(point) for point in stdTemp])
    return filesDict

def readParamsData():
    """Returns dict with angle key and wls fit params"""
    fileName = askopenfilename(initialdir='./AppsNshit/Data')
    dataDict = ReadJson(fileName)
    return dataDict

def readBlueData():
    """Returns [angleList, powerList, stdList]"""
    filename = askopenfilename(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
    with open(filename, 'r') as file:
        rows = list(file)
        rows.pop(0)
        angleTemp = []
        currnetTemp = []
        measTemp = []
        stdTemp = []
        for row in rows:
            points = row.strip().split(', ')
            angleTemp.append(int(points[0]))
            currnetTemp.append(float(points[1]))
            measTemp.append(float(points[2]))
            stdTemp.append(float(points[3]))
    refAngleList = []
    currentList = []
    measList = []
    stdList = []
    i = 1
    while i < len(measTemp):
        refAngleList.append(angleTemp[i])
        currentList.append(currnetTemp[i])
        measList.append(measTemp[i] - measTemp[i-1])
        stdList.append(stdTemp[i])
        i += 2
    return refAngleList, measList, stdList

def saveSum(sDensityList, sumList):
    """Saves Riemann sum as funnction of surface density to a csv"""
    pass

def readSum():
    """Returns thicknessList, sumList"""
    pass

#===============================================================================================0



def plotCurrentsweepData(filesDict, filter = None, errorbar = None):
    """Plots UV current sweep data with or without filter (filter should be given in watts)"""
    
    if filter is None:
        for angle in filesDict:
            plt.scatter(filesDict[angle][0], filesDict[angle][1], c='mediumorchid', marker='.', markersize=4, label=f'{angle}')
        plt.xlabel('Current / A')
        plt.ylabel('Power / W')
        plt.tight_layout()
        plt.show()

def thirtySixtyCombineUV(paramsDict30, paramsDict60):
    """Completes conversion distribution using
    measurements with 30 and 60 degree incident angle.\n
    Returns full angle distribution."""
    pass

def plotAngleDistUV(paramsDict, incAng = None):
    pass

def plotAngleDistBLUE(angleList, powerList, stdList = None):
    pass

def riemannSum(distData):
    """Returns Riemann sum of distribution"""
    pass

def plotSumVsThick(thicknessList, sumList):
    """Plots Riemann sum as function of coating thickness"""
    pass





#============================================================================================================

def main():
    pass

if __name__ == '__main__':
    main()