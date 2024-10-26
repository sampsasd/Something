import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter.filedialog import askopenfilename, askopenfilenames
from FileHandler import ReadJson
from statsmodels.api import WLS
import statsmodels.api as sm
from functions import line, fresnelAvg
from scipy.integrate import simpson
from time import sleep
import matplotlib as mpl

#FINAL PLOTS FOR GRADU
#direct uv current sweep with and without filter
#   uv current sweep, filtered sweep, 
#   angle distribution with and without filter, combined conversion dist

#blue angle distribution
#blue specular peak height as function of coating thickness (relative?)
#blue Riemann sum as function of coating thickness

#Riemann sum of combined conversion dist as a function of coating thickness
#
#Section of the solid angle distribution at the plane of incident light beam

settings = {'plotCurrentSweep': 0, 
            'plotBlueDist': 0, 
            'plotBlueDistMulti': 0, 
            'plotSpecThic': 0,
            'plotSpecThicUV': 0,
            'plotIntegrDiff': 0, 
            'plotUVDist': 0, 
            'plotUVDistMulti': 0,
            'plotUVSimps': 0, 
            'plotFresnel': 1,
            'extra': 0}

samples = {'noSample': 0, 
           '_0725_': 5.0, 
           '_0618_': 10.4, 
           '_0724_': 20.2, 
           '_0701_': 29.7, 
           '_0625_': 41.4, 
           '_0920_': 88.1, 
           '_1002_': 155.8}

samples2 = {'noSample': 'A', 
           '_0725_': 'B', 
           '_0618_': 'C', 
           '_0724_': 'D', 
           '_0701_': 'E', 
           '_0625_': 'F', 
           '_0920_': 'G', 
           '_1002_': 'H'}


def readCurrentSweepData():
    """Returns dict with angle key and [currentList, powerList, stdList]"""
    """Reads current in mA, power and std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
    fileNameList = askopenfilenames(initialdir='./AppsNshit/DataPrganized', filetypes=(('csv files', 'csv'), ))
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

def readParamsData(alpha=False):
    """Returns list of dicts with angle key and wls fit params"""
    fileNameList = askopenfilenames(initialdir='./AppsNshit/DataOrganized')
    dataDictList = []
    for file in fileNameList:
        for key in samples:
            if key in file:
                thick = samples[key]
        for key in samples2:
            if key in file:
                samp = samples2[key]
        if alpha:
            al = int(file[-2:])
            dataDictList.append((ReadJson(file), thick, samp, al))
        else:
            dataDictList.append((ReadJson(file), thick, samp))
    return dataDictList

def readBlueData():
    """Returns list of [angleList, powerList, stdList] elements"""
    dataListList = []
    filename = askopenfilenames(initialdir='./AppsNshit/DataOrganized', filetypes=(('csv files', 'csv'), ))
    for name in filename:
        for key in samples:
            if key in name:
                thic = samples[key]
                samp = samples2[key]
        with open(name, 'r') as file:
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
        dataListList.append([refAngleList, measList, stdList, thic, samp])
    return dataListList

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
    solidAngleApprox = 0.0071
    print(solidAngleApprox)

    return [point / solidAngleApprox for point in powerList]

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
        fig, (ax1, ax2) = plt.subplots(1, 2)
        fig.set_size_inches((10, 6))
        #ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
        #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
        for angle in filesDictFiltered:
            ax1.scatter(filesDict[angle][0], filesDict[angle][1], marker='o', s=8, label=f'$\\beta$={angle}'+'$^{\circ}$')
            ax2.scatter(filesDictFiltered[angle][0], filesDictFiltered[angle][1], marker='o', s=8)
            fit = line(currentLin, poptDict[angle][0][1], poptDict[angle][0][0])
            ax2.plot(currentLin, fit)

    ax1.set_xlabel('Current / A')
    ax1.set_ylabel('Power / W')
    ax1.legend()
    ax2.set_xlabel('Current / A')
    ax2.set_ylabel('Power / W')
    #ax2.legend()
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
            asd = readParamsData()[0]
            paramsDict = asd[0]
            alpha = asd[1]
            angleList = interpolateData(paramsDict, 50e-3)[0]
            powerList = interpolateData(paramsDict, 50e-3)[1]
            stdList = interpolateData(paramsDict, 50e-3)[2]
            
            j = angleList.index(50)
            k = angleList.index(70)
            angleList.remove(50)
            angleList.remove(70)
            powerList.remove(powerList[j])
            powerList.remove(powerList[k])

            paramsDict2 = readParamsData()[0][0]
            angleList2 = interpolateData(paramsDict2, 50e-3)[0]
            powerList2 = interpolateData(paramsDict2, 50e-3)[1]
            stdList2 = interpolateData(paramsDict2, 50e-3)[2]

            powerListSA = powerPerSolidAngle(powerList)
            stdListSA = powerPerSolidAngle(stdList)

            powerListSA2 = powerPerSolidAngle(powerList2)

            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.set_size_inches((11, 6))
            ax1.scatter(angleList, powerListSA, marker='o', s=8, c='darkorchid', label=f'$\\alpha$ = {alpha}$^\circ$')
            ax2.scatter(angleList2, powerListSA2, marker='o', s=8, c='blue', label=f'$\\alpha$ = {alpha}$^\circ$')
            ax1.xaxis.set_major_locator(ticker.MultipleLocator(base=15))
            ax2.xaxis.set_major_locator(ticker.MultipleLocator(base=15))
            #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1e'))
            ax1.set_xlim(-90, 90)
            ax2.set_xlim(-90, 90)
            ax1.set_xlabel('$\\beta$ / deg')
            ax1.set_ylabel('Radiant intensity / W$\cdot$sr$^{-1}$')
            ax2.set_xlabel('$\\beta$ / deg')
            ax2.set_ylabel('Radiant intensity / W$\cdot$sr$^{-1}$')
            ax1.legend()
            ax2.legend()
        elif multi:
            paramsDictList = readParamsData(alpha=True)
            angleLists = []
            powerLists = []
            stdLists = []
            thickList = []
            sampList = []
            alphaList = []
            for tup in paramsDictList:
                alphaList.append(tup[3])
                thickList.append(tup[1])
                sampList.append(tup[2])
                angleList = interpolateData(tup[0], 50e-3)[0]
                powerList = powerPerSolidAngle(interpolateData(tup[0], 50e-3)[1])
                stdList = powerPerSolidAngle(interpolateData(tup[0], 50e-3)[2])

                angleList, powerList, stdList = zip(*sorted(zip(angleList, powerList, stdList)))

                angleLists.append(interpolateData(tup[0], 50e-3)[0])
                powerLists.append(powerPerSolidAngle(interpolateData(tup[0], 50e-3)[1]))
                stdLists.append(powerPerSolidAngle(interpolateData(tup[0], 50e-3)[2]))

            
            sampList, thickList, alphaList, angleLists, powerLists, stdLists = zip(*sorted(zip(sampList, thickList, alphaList, angleLists, powerLists, stdLists)))
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            tcolors = mpl.colormaps['jet'](np.linspace(0.1, 1, 8))#[0.3, 0.43, 0.56, 0.7, 1]
            for i in range(len(angleLists)):
                ax.scatter(angleLists[i], powerLists[i], marker='o', s=16, c=tcolors[i], label='Sample: ' + f'{sampList[i]}')
                #ax.plot(angleLists[i], powerLists[i]) #, label=f'{thickList[i]}' + ' $\mathrm{\mu}$g$\cdot$cm$^{-2}$'
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            plt.xlabel('$\\beta$ / deg')
            plt.ylabel('Radiant intensity / W$\cdot$sr$^{-1}$')
            plt.legend()

        plt.xlim(-90, 90)
        plt.ticklabel_format(axis='y', scilimits=(yAxisExp, yAxisExp))
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(e)

def plotAngleDistBLUE(yAxisExp=-5, multi=False):
    
    try:
        if not multi:
            data = readBlueData()[0]
            alpha = -data[0][data[1].index(max(data[1]))]
            angleList = data[0]
            #j = angleList.index(70)
            #angleList.remove(70)
            powerList = data[1]
            #powerList.remove(powerList[j])
            stdList = data[2]

            powerListSA = powerPerSolidAngle(powerList)
            stdListSA = powerPerSolidAngle(stdList)

            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            ax.scatter(angleList, powerListSA, marker='o', s=20, label=f'$\\alpha$ = {alpha}$^\circ$')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
        
        elif multi:
            angleLists = []
            powerLists = []
            stdLists = []
            thickList = []

            datalists = readBlueData()

            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))

            specList = []
            sumList = []
            sumNoSpecList = []
            datalists = sorted(datalists, key=lambda x: x[3])
            for dataset in datalists:
                alpha = -dataset[0][dataset[1].index(max(dataset[1]))]
                thickList.append(dataset[3])
                angleList = dataset[0]
                powerList = powerPerSolidAngle(dataset[1])
                stdList = powerPerSolidAngle(dataset[2])

                angleLists.append(angleList)
                powerLists.append(powerList)
                stdLists.append(stdList)

                angleList, powerList, stdList = zip(*sorted(zip(angleList, powerList, stdList)))

                #ax.scatter(angleList, powerList, s=15)
                ax.scatter(angleList, powerList, marker='o', s=16, label='Sample: ' + f'{dataset[4]}')
                plt.plot(angleList, powerList)
                specList.append(max(dataset[1]))
                sumList.append(riemannSum(dataset[1]))
                sumNoSpecList.append(riemannSum(dataset[1], excludeSpecular=True))
            print(specList, '\n', sumList, '\n', sumNoSpecList, '\n')
            specList, sumList, sumNoSpecList = zip(*sorted(zip(specList, sumList, sumNoSpecList)))
            print('\n', specList, '\n', sumList, '\n', sumNoSpecList)

        plt.xlim((-90, 90))
        plt.ticklabel_format(axis='y', scilimits=(yAxisExp, yAxisExp))
        plt.xlabel('$\\beta$ / deg')
        plt.ylabel('Radiant intensity / W$\cdot$sr$^{-1}$')
        plt.legend()
        plt.tight_layout()
        plt.show()
        if multi:
            return specList
    except Exception as e:
        print(e)



def simps(angleListList, dataListList):
    simpList = []
    for i in range(len(dataListList)):
        anglelis = angleListList[i]
        datalis = dataListList[i]
        anglelis, datalis = zip(*sorted(zip(anglelis, datalis)))
        simp = simpson(datalis, x=anglelis)
        simpList.append(simp)
        print(anglelis, datalis)
    #simpList.sort()
    print(simpList)
    return simpList

def plotSimps(thiccList, simpList):
    
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches((10, 6))
    ax.scatter(thiccList, simpList)
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10e-6))
    #plt.xlim((-90, 90))
    #plt.ticklabel_format(axis='y', scilimits=(0, 0))
    plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
    plt.ylabel('Integrated conversion distribution')
    plt.tight_layout()
    plt.show()


def riemannSum(powerList, excludeSpecular=False):
    """Returns Riemann sum of distribution"""
    if excludeSpecular:
        powerList.remove(max(powerList))
    sumsum = sum(powerList)
    return sumsum

def plotSumVsThick(thicknessList, sumList):
    """Plots Riemann sum as function of coating thickness"""
    pass





#============================================================================================================


def main():
    try:
        thiccList = [0, 4.96, 10.035, 20.18, 29.74, 41.42, 88.06, 155.8]
        #UV STUFF==============================================

        #Current sweep
        if settings['plotCurrentSweep']:
            filesDict = readCurrentSweepData()
            #plotCurrentsweepData(filesDict=filesDict)
            plotCurrentsweepData(filesDict=filesDict, filter=5e-10)

        #Angle dist
        if settings['plotBlueDist']:
            plotAngleDistBLUE()
        
        if settings['plotBlueDistMulti']:
            asd = plotAngleDistBLUE(yAxisExp=-3, multi=True)
            qwe = thiccList[::-1]
            if len(asd) == 8:
                plt.scatter(qwe, asd)
                plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
                plt.ylabel('Specular reflection power / W')
                plt.tight_layout()
                plt.show()

        if settings['plotUVDist']:
            plotAngleDistUV()
        
        if settings['plotUVDistMulti']:
            plotAngleDistUV(multi=True)

        #SIMPS
        if settings['plotUVSimps']:
            #thiccList = [0, 4.96, 10.035, 20.18, 29.74, 41.42, 88.06, 155.8]
            plist = readParamsData()
            anglelistlist = [interpolateData(l[0], 50e-3)[0] for l in plist]
            datalistlist = [interpolateData(l[0], 50e-3)[1] for l in plist]
            thiccList = [l[1] for l in plist]
            for i in range(len(anglelistlist)):
                if thiccList[i] == 0:
                    j = anglelistlist[i].index(-45)
                    anglelistlist[i].remove(-45)
                    datalistlist[i].remove(datalistlist[i][j])
                else:
                    j = anglelistlist[i].index(-60)
                    anglelistlist[i].remove(-60)
                    datalistlist[i].remove(datalistlist[i][j])
            simpList = simps(anglelistlist, datalistlist)

            plotSimps(thiccList, simpList)
        
        if settings['plotSpecThic']:
            dataLists30 = readBlueData()
            dataLists60 = readBlueData()
            thickList30 = []
            specList30 = []
            specList60 = []
            thickList60 = []
            for l in dataLists30:
                thickList30.append(l[3])
                specList30.append(max(l[1]))
            for l in dataLists60:
                thickList60.append(l[3])
                specList60.append(max(l[1]))
            specList30New = [point / max(specList30) for point in specList30]
            specList60New = [point / max(specList60) for point in specList60]
            thickList30, specList30New = zip(*sorted(zip(thickList30, specList30New)))
            thickList60, specList60New = zip(*sorted(zip(thickList60, specList60New)))
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            ax.scatter(thickList30, specList30New, marker='o', s=8, label='$\\alpha=30^{\circ}$')
            ax.scatter(thickList60, specList60New, marker='o', s=8, label='$\\alpha=60^{\circ}$')
            ax.plot(thickList30, specList30New)
            ax.plot(thickList60, specList60New)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            #plt.xlim((-90, 90))
            #plt.ticklabel_format(axis='y', scilimits=(0, 0))
            plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
            plt.ylabel('Relative specular reflection')
            plt.legend()
            plt.tight_layout()
            plt.show()

        if settings['plotSpecThicUV']:
            dataLists30 = readParamsData()
            thickList30 = []
            specList30 = []
            for l in dataLists30:
                thickList30.append(l[1])
                specList30.append(max(l[0][1]))
            specList30New = [point / max(specList30) for point in specList30]
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((9, 6))
            ax.scatter(thickList30, specList30New)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            #plt.xlim((-90, 90))
            #plt.ticklabel_format(axis='y', scilimits=(0, 0))
            plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
            plt.ylabel('Relative specular reflection')
            plt.tight_layout()
            plt.show()
        
        if settings['plotIntegrDiff']:
            dataLists30 = readBlueData()
            #dataLists60 = readBlueData()

            thickList30 = []
            dataList30 = []
            anglelistlist = []
            datalistlist = []
            incAngList = []
            for l in dataLists30:
                thickList30.append(l[3])
                ll = l[1]
                i = l[1].index(max(l[1]))
                ll.remove(max(ll))
                al = l[0]
                incAngList.append(-al[i])
                al.remove(al[i])
                # if l[3] == 0:
                #     al = l[0]
                #     al.remove(-45)
                # else:
                #     al = l[0]
                #     al.remove(-60)
                anglelistlist.append(al)
                datalistlist.append(ll)
                
            dataList30 = simps(anglelistlist, datalistlist)

            thickList60 = []
            dataList60 = []
            anglelistlist = []
            datalistlist = []
            incAngList = []
            # for l in dataLists60:
            #     thickList60.append(l[3])
            #     ll = l[1]
            #     i = l[1].index(max(l[1]))
            #     ll.remove(max(ll))
            #     al = l[0]
            #     incAngList.append(-al[i])
            #     al.remove(al[i])
            #     # if l[3] == 0:
            #     #     al = l[0]
            #     #     al.remove(-45)
            #     # else:
            #     #     al = l[0]
            #     #     al.remove(-60)
            #     anglelistlist.append(al)
            #     datalistlist.append(ll)
                
            # dataList60 = simps(anglelistlist, datalistlist)
            
            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            ax.scatter(thickList30, dataList30)
            #ax.scatter(thickList60, dataList60, label='$\\alpha=60^{\circ}$')
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            #plt.xlim((-90, 90))
            plt.ticklabel_format(axis='y', scilimits=(-4, -4))
            #plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
            plt.xlabel('Sample surface density / $\mathrm{\mu}$g$\cdot$cm$^{-2}$')
            plt.ylabel('Integrated diffuse reflection')
            #plt.legend()
            plt.tight_layout()
            plt.show()


        if settings['plotFresnel']:
            ang = np.linspace(0, 90, 100)
            func = [fresnelAvg(point, 1.000273, 1.62) for point in ang]

            fig, ax = plt.subplots(1, 1)
            fig.set_size_inches((10, 6))
            ax.xaxis.set_major_locator(ticker.MultipleLocator(base=10))
            plt.plot(ang, func)
            ax.set_xlabel('$\\alpha$ / deg')
            ax.set_ylabel('$R_{\mathrm{eff}}$')
            plt.xlim((-5, 95))
            plt.tight_layout()
            plt.show()

        
        if settings['extra']:
            
            paramsDictList = readParamsData() #noFilter
            paramsDictList2 = readParamsData() #filter
            blueDict = readBlueData()
            angleLists = []
            powerLists = []
            stdLists = []
            i = 0
            for dic in paramsDictList:
                np.savetxt(f'filesUVnoFilter{i}.csv', [p for p in zip(interpolateData(dic, 50e-3)[0], powerPerSolidAngle(interpolateData(dic, 50e-3)[1]))], delimiter=',')
                i += 1
            i = 0
            for dic in paramsDictList2:
                np.savetxt(f'filesUVilter{i}.csv', [p for p in zip(interpolateData(dic, 50e-3)[0], powerPerSolidAngle(interpolateData(dic, 50e-3)[1]))], delimiter=',')
                i += 1
            i = 0
            for l in blueDict:
                np.savetxt(f'filesBLUEfilter{i}.csv', [p for p in zip(l[0], powerPerSolidAngle(l[1]))], delimiter=',')
                i += 1

    except Exception as e:
        print(e)



if __name__ == '__main__':
    main()