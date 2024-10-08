import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter.filedialog import askopenfilename, askopenfilenames
from FileHandler import ReadJson
from statsmodels.api import WLS
import statsmodels.api as sm
from functions import line
from scipy.integrate import simpson

#FINAL PLOTS FOR GRADU
#direct uv current sweep with and without filter
#   uv current sweep, filtered sweep, 
#   angle distribution with and without filter, combined conversion dist

#blue angle distribution
#blue specular peak height as function of coating thickness (relative?)
#blue Riemann sum as function of coating thickness

#Riemann sum of combined conversion dist as a function of coating thickness

settings = {'plotCurrentSweep': 0, 
            'plotBlueDist': 0, 
            'plotUVDist': 0,
            'plotUVSimps': 0}


def readCurrentSweepData():
    """Returns dict with angle key and [currentList, powerList, stdList]"""
    """Reads current in mA, power and std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
    fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
    filesDict = {}
    for i in range(len(fileNameList)):
        currTemp = []
        measTemp = []
        stdTemp = []
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
    """Returns list of dicts with angle key and wls fit params"""
    fileNameList = askopenfilenames(initialdir='./AppsNshit/Data')
    dataDictList = []
    for file in fileNameList:
        dataDictList.append(ReadJson(file))
    return dataDictList

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

def powerPerSolidAngle(powerList):
    
    sensorArea = np.pi * (9.5e-3 / 2)**2
    distToSensor = 10e-2
    solidAngle = sensorArea / (distToSensor**2)
    print(solidAngle)

    return [point / solidAngle for point in powerList]

def filterData(filesDict, filter):
    """Filters current sweep data based on datapoint distance of weighted least squares fit.
    \nWLS FIT IS B+AX NOT AX+B"""

    filesDictFiltered = {}
    poptDict = {}
    fitDict = {}
    
    for ang in filesDict:
        filesDictFiltered[ang] = (filesDict[ang][0].copy(), filesDict[ang][1].copy(), filesDict[ang][2].copy())
    
    for ang in filesDictFiltered:
        while True:
            newIter = False
            weights = [1/(point**2) for point in filesDictFiltered[ang][2]]
            xDataForWLS = sm.add_constant(filesDictFiltered[ang][0])
            wlsFit = WLS(filesDictFiltered[ang][1], xDataForWLS, weights=weights).fit()
            poptDict[ang] = wlsFit.params, wlsFit.cov_params()

            #prstd, intervalLow, intervalUp = wls_prediction_std(wlsFit)

            #popt, pcov = curve_fit(line, currentListFiltered, measListFiltered)

            fitDict[ang] = [line(filesDictFiltered[ang][0][i], poptDict[ang][0][1], poptDict[ang][0][0]) for i in range(len(filesDictFiltered[ang][0]))]
            #ERRORS HERE U DUMB FUCK=============================================================================================================================================================================================
            i = 0
            while i < len(fitDict[ang]):
                if filesDictFiltered[ang][1][i] > fitDict[ang][i] + filter and fitDict[ang][i] > 0:
                    filesDictFiltered[ang][0].remove(filesDictFiltered[ang][0][i])
                    filesDictFiltered[ang][1].remove(filesDictFiltered[ang][1][i])
                    filesDictFiltered[ang][2].remove(filesDictFiltered[ang][2][i])
                    fitDict[ang].remove(fitDict[ang][i])
                    newIter = True
                elif filesDictFiltered[ang][1][i] < fitDict[ang][i] - filter and fitDict[ang][i] > 0:
                    filesDictFiltered[ang][0].remove(filesDictFiltered[ang][0][i])
                    filesDictFiltered[ang][1].remove(filesDictFiltered[ang][1][i])
                    filesDictFiltered[ang][2].remove(filesDictFiltered[ang][2][i])
                    fitDict[ang].remove(fitDict[ang][i])
                    newIter = True
                elif filesDictFiltered[ang][1][i] < fitDict[ang][i] - filter and fitDict[ang][i] < 0:
                    filesDictFiltered[ang][0].remove(filesDictFiltered[ang][0][i])
                    filesDictFiltered[ang][1].remove(filesDictFiltered[ang][1][i])
                    filesDictFiltered[ang][2].remove(filesDictFiltered[ang][2][i])
                    fitDict[ang].remove(fitDict[ang][i])
                    newIter = True
                elif filesDictFiltered[ang][1][i] > fitDict[ang][i] + filter and fitDict[ang][i] < 0:
                    filesDictFiltered[ang][0].remove(filesDictFiltered[ang][0][i])
                    filesDictFiltered[ang][1].remove(filesDictFiltered[ang][1][i])
                    filesDictFiltered[ang][2].remove(filesDictFiltered[ang][2][i])
                    fitDict[ang].remove(fitDict[ang][i])
                    newIter = True
                else:
                    i += 1

            if not newIter:
                #print(poptDict)
                break
    return filesDictFiltered, poptDict

def interpolateData(paramsDict, current):
        """Takes fit parameters and interpolates power and 2 sigma error for given current"""
        angleList = []
        powerList = []
        sigmaList = []
        for angle in paramsDict:
            angleList.append(int(angle))
            powerList.append(paramsDict[angle][0][1] * current)
            sigmaList.append(2 * np.sqrt(paramsDict[angle][1][1][1]) * current + 2 * np.sqrt(paramsDict[angle][1][0][0]))
        return angleList, powerList, sigmaList

#MAYBE CHANGE UNITS IN PLOTS
def plotCurrentsweepData(filesDict, filter = None, errorbar = None):
    """Plots UV current sweep data with or without filter (filter should be given in watts)"""
    
    if filter is None:

        for angle in filesDict:
            plt.scatter(filesDict[angle][0], filesDict[angle][1], marker='o', s=8, label=f'{angle}'+'$^{\mathrm{\circ}}$')

    elif filter is not None:

        filesDictFiltered = filterData(filesDict=filesDict, filter=filter)[0]
        poptDict = filterData(filesDict=filesDict, filter=filter)[1]
        currentLin = np.linspace(0, 100e-3, 100)
        
        for angle in filesDictFiltered:
            plt.scatter(filesDictFiltered[angle][0], filesDictFiltered[angle][1], marker='o', s=8, label=f'{angle}')
            fit = line(currentLin, poptDict[angle][0][1], poptDict[angle][0][0])
            plt.plot(currentLin, fit)

    plt.xlabel('Current / A')
    plt.ylabel('Power / W')
    plt.legend()
    plt.tight_layout()
    plt.show()


def thirtySixtyCombineUV(paramsDict30, paramsDict60):
    """Completes conversion distribution using
    measurements with 30 and 60 degree incident angle.\n
    Returns full angle distribution."""
    pass

def plotAngleDistUV(yAxisExp=-7, incAng = None, multi=False):
    """Plots angle distribution for uv and marks incident angle to plot if specified"""
    try:
        if not multi:
            paramsDict = readParamsData()[0]
            angleList = interpolateData(paramsDict, 50e-3)[0]
            powerList = interpolateData(paramsDict, 50e-3)[1]
            stdList = interpolateData(paramsDict, 50e-3)[2]

            powerListSA = powerPerSolidAngle(powerList)
            stdListSA = powerPerSolidAngle(stdList)

            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((9, 6))
            ax.scatter(angleList, powerListSA)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))

        plt.xlim(-90, 90)
        plt.ticklabel_format(axis='y', scilimits=(yAxisExp, yAxisExp))
        plt.xlabel('$\\beta$ / deg')
        plt.ylabel('$I$ / W$\cdot$sr$^{-1}$')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(e)

def plotAngleDistBLUE(yAxisExp=-5, multi=False):
    
    try:
        if not multi:
            data = readBlueData()
            angleList = data[0]
            powerList = data[1]
            stdList = data[2]

            powerListSA = powerPerSolidAngle(powerList)
            stdListSA = powerPerSolidAngle(stdList)

            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((9, 6))
            ax.scatter(angleList, powerListSA)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
        
        plt.xlim((-90, 90))
        plt.ticklabel_format(axis='y', scilimits=(yAxisExp, yAxisExp))
        plt.xlabel('$\\beta$ / deg')
        plt.ylabel('$I$ / W$\cdot$sr$^{-1}$')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(e)

def simps(angleListList, dataListList):
    simpList = []
    for i in range(len(dataListList)):
        simp = simpson(dataListList[i], x=angleListList[i])
        simpList.append(simp)
    print(simpList)
    return simpList

def riemannSum(distData):
    """Returns Riemann sum of distribution"""
    pass

def plotSumVsThick(thicknessList, sumList):
    """Plots Riemann sum as function of coating thickness"""
    pass





#============================================================================================================


def main():
    #UV STUFF==============================================

    #Current sweep
    if settings['plotCurrentSweep']:
        filesDict = readCurrentSweepData()
        plotCurrentsweepData(filesDict=filesDict)
        plotCurrentsweepData(filesDict=filesDict, filter=1e-9)

    #Angle dist
    if settings['plotBlueDist']:
        plotAngleDistBLUE()

    if settings['plotUVDist']:
        plotAngleDistUV()

    #SIMPS
    if settings['plotUVSimps']:
        plist = readParamsData()
        anglelistlist = [interpolateData(l, 50e-3)[0] for l in plist]
        datalistlist = [interpolateData(l, 50e-3)[1] for l in plist]
        simps(anglelistlist, datalistlist)



if __name__ == '__main__':
    main()