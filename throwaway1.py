import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames
import matplotlib.ticker as ticker

detectorArea = np.pi*(9.5e-3/2)**2
print(detectorArea)

def readMeas(fileNameList:list):
    """Reads current in mA, power and 2*std in uW.\n
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

#=============================================================================================

read1 = readMeas(('./AppsNshit/Data/240711directBLUE.csv', './AppsNshit/Data/240711specularNoSampleBLUE.csv'))

sReflectivity = []
for i in range(len(read1[0][0])):
    asd = read1[1][1][i] / read1[0][1][i]
    sReflectivity.append(asd)
power1 = [point / 1000 for point in read1[0][1]]

ax = plt.subplot()
ax.plot(power1, sReflectivity)
ax.set_xlabel('Power / mW')
ax.set_ylabel('Reflectivity (specular)')
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.05))
ax.grid(linestyle=':')
plt.tight_layout()
plt.show()

#=========================================================================================

read2 = readMeas(['./AppsNshit/Data/240711directUV.csv', './AppsNshit/Data/240711specularNoSampleUV2.csv'])

sReflectivity2 = []
for i in range(len(read2[0][0])):
    asd = read2[1][1][i] / read2[0][1][i]
    sReflectivity2.append(asd)
power2 = read2[0][1]

ax = plt.subplot()
ax.plot(power2, sReflectivity2)
ax.set_xlabel('Power / $\\mathrm{\\mu}$W')
ax.set_ylabel('Reflectivity (specular)')
ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.01))
ax.grid(linestyle=':')
plt.tight_layout()
plt.show()

#=============================================================================================

read3 = readMeas(['./AppsNshit/Data/240711converted0625UV2.csv', './AppsNshit/Data/240711specularConverted0625UV2.csv'])

diffConv40ug = [(point / detectorArea) * 2 * np.pi * (57e-3)**2 for point in read3[0][1]]

convP = []
for i in range(len(read2[1][0])):
    asd = diffConv40ug[i] / read2[0][1][i]
    convP.append(asd)

#convP2 = []
#for i in range(len(read2[1][0])):
#    asd = diffConv40ug[i] / read2[0][1][i]
#    convP.append(asd)

ax = plt.subplot()
ax.plot(power2, convP)
ax.set_xlabel('UV power / $\\mathrm{\\mu}$W')
ax.set_ylabel('Conversion rate')
#ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.01))
ax.grid(linestyle=':')
plt.tight_layout()
plt.show()

convPatSpec = [(point / (2 * np.pi * (45e-3)**2)) * detectorArea for point in convP]
correctedRef = []
for i in range(len(convPatSpec)):
    correctedRef.append(read3[1][1][i] - convPatSpec[i])

specreflUV = []
for i in range(len(correctedRef)):
    specreflUV.append(correctedRef[i] / power2[i])

#ax = plt.subplot()
#ax.plot(power2, specreflUV)
#ax.set_xlabel('Power / $\\mathrm{\\mu}$W')
#ax.set_ylabel('Reflectivity')
#ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.01))
#ax.grid(linestyle=':')
#plt.tight_layout()
#plt.show()

#====================================================================================

read4 = readMeas(['./AppsNshit/Data/240711specular0625BLUE.csv', './AppsNshit/Data/240711diffuse0625BLUE.csv'])

sReflectivity40ug = []
for i in range(len(read4[0][1])):
    asd = read4[0][1][i] / read1[0][1][i]
    sReflectivity40ug.append(asd)

ax = plt.subplot()
ax.plot(power1[1:], sReflectivity40ug[1:])
ax.set_xlabel('Power / mW')
ax.set_ylabel('Reflectivity (specular)')
#ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
ax.grid(linestyle=':')
plt.tight_layout()
plt.show()


dReflectivity40ug = []
for i in range(len(read4[1][1])):
    asd = read4[1][1][i] / read1[0][1][i]
    dReflectivity40ug.append(asd)

ax = plt.subplot()
ax.plot(power1[6:], dReflectivity40ug[6:])
ax.set_xlabel('Power / mW')
ax.set_ylabel('Reflectivity (diffuse)')
#ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
ax.grid(linestyle=':')
plt.tight_layout()
plt.show()