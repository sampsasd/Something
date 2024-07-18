import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames
import matplotlib.ticker as ticker
from functions import readMeas, gaussian
from scipy.optimize import curve_fit


def main():

    #240716

    hypoList = [10.8, 10.7, 10.8, 10.7, 10.7, 10.6, 10.5, 10.6, 10.6, 10.6, 11.5]
    oppoList = [0, 1.7, 2.8, 4.2, 5.5, 6.8, 7.9, 9, 9.8, 10.4, 10.7]

    angleList = []
    for i in range(len(hypoList)-1):
        angleList.append(np.arcsin(oppoList[i] / hypoList[i]) * (180 / np.pi))
    angleList.append(180 - np.arcsin(oppoList[-1] / hypoList[-1]) * (180 / np.pi))

    read = readMeas(['./AppsNshit/Data/240716zeroFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716firstFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716secondFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716thirdFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716fourthFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716fifthFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716sixthFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716seventhFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716eighthFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716ninthFromSpecular0625BLUE.csv', 
                     './AppsNshit/Data/240716tenthFromSpecular0625BLUE.csv'])
    
    powerDict = {}
    for i in range(len(read[0][1])):
        powerDict[i] = [[read[key][1][i] for key in read], [read[key][2][i] for key in read]]

    #popt, pcov = curve_fit(gaussian, angleList[:-1], powerDict[7][0][:-1], p0=[60, 0, 10, 0])
    #print(popt, pcov)
    #linAng = np.linspace(0, 90, 100)
    #line = gaussian(linAng, *popt)
    labels = ['10 mA', '15 mA', '20 mA', '25 mA', '30 mA']
    colors = ['tomato', 'gold', 'mediumseagreen', 'cornflowerblue', 'mediumorchid']
    for i in range(5):
        plt.scatter(angleList[:-1], powerDict[3 + i][0][:-1], c=colors[i], s=15, label=labels[i])
    #plt.plot(linAng, line)
    plt.title('Blue laser\n40 $\\mathrm{\\mu}$g / cm$^{2}$ coating')
    plt.xlabel('Angle from specular / deg')
    plt.ylabel('Power / $\\mathrm{\\mu}$W')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()