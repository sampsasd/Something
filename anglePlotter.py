import pyvisa as visa
from tkinter import Tk, IntVar
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from time import sleep
import threading
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from functions import gaussian, GnL

class apGUI:
    def __init__(self, master) -> None:

        self.master = master
        self.master.title('Angle Plotter')
        self.master.geometry('300x600')
        self.master.attributes('-fullscreen', True)
        self.master.configure(background='black')

        self.angleList = [-20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 100, 110, 120]
        self.currentList = [0, 0.001, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
        self.measList = []
        self.stdList = []
        self.filesDict = {}

        #==============================STYLES================================================
        self.frmStyle = Style()
        self.frmStyle.theme_use('classic')
        self.frmStyle.configure('my.TFrame', background='black')

        self.butStyle = Style()
        self.butStyle.theme_use('classic')
        self.butStyle.configure(style='my.TButton', font=('Helvetica', 15))
        self.butStyle.map('my.TButton', 
                          background=[('!active', 'black'), ('pressed', 'red'), ('active', 'maroon')], 
                          foreground=[('!active', 'red'), ('pressed', 'black'), ('active', 'black')])

        self.chButStyle = Style()
        self.chButStyle.theme_use('classic')
        self.chButStyle.configure(style='my.TCheckbutton', font=('Helvetica', 15))
        self.butStyle.map('my.TCheckbutton', 
                          background=[('!active', 'black'), ('pressed', 'red'), ('active', 'maroon')], 
                          foreground=[('!active', 'red'), ('pressed', 'black'), ('active', 'black')])

        self.labStyle = Style()
        self.labStyle.theme_use('classic')
        self.labStyle.configure(style='my.TLabel', font=('Helvetica', 18))
        self.butStyle.map('my.TLabel', 
                          background=[('!active', 'black'), ('pressed', 'red'), ('active', 'maroon')], 
                          foreground=[('!active', 'red'), ('pressed', 'black'), ('active', 'black')])

        #==============================================================================================
        self.frm = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.frm.place(in_=self.master, anchor='center', relx=.5, rely=.6)

        self.titleframe = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.titleframe.place(in_=self.master, anchor='center', relx=.5, rely=.2)

        self.hp = Label(self.titleframe, text='Harry Plotter and the Chamber of Darkness', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #=============================BUTTONS==================================================

        self.fileBut = Button(self.frm, text='Files', style='my.TButton', command=self.readMeas)
        self.fileBut.grid(column=0, row=4, padx=5, pady=5)

        self.clearDataBut = Button(self.frm, text='Clear data', style='my.TButton', command=self.clear)
        self.clearDataBut.configure(state='disabled')
        self.clearDataBut.grid(column=0, row=5, padx=5, pady=5)

        self.scatterBut = Button(self.frm, text='Scatter', style='my.TButton', command=self.scatter)
        self.scatterBut.grid(column=0, row=0, padx=20, pady=20)

        self.errorVar = IntVar(value=0)
        self.errorCheck = Checkbutton(self.frm, text='Errorbar', variable=self.errorVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.errorCheck.grid(column=0, row=1, padx=5, pady=5)

        self.fitGVar = IntVar(value=0)
        self.fitGCheck = Checkbutton(self.frm, text='Fit Gaussian', variable=self.fitGVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.fitGCheck.grid(column=0, row=2, padx=5, pady=5)

        self.fitGVar2 = IntVar(value=0)
        self.fitGCheck2 = Checkbutton(self.frm, text='Fit Gaussian (Exc. Specular)', variable=self.fitGVar2, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.fitGCheck2.grid(column=0, row=3, padx=5, pady=5)

        self.destructionBut = Button(self.frm, text='Close', style='my.TButton', command=self.master.quit)
        self.destructionBut.grid(column=0, row=100, padx=30, pady=30)

        

    def scatter(self):
        """Scatters  Power / uW as a function of angle from specular / deg"""

        self.angleList = []
        self.measDict = {}
        self.stdDict = {}
        #Makes a list of angles
        for key in self.filesDict:
            self.angleList.append(key)
        #Makes dict keys of different laser currents with power(angle) and their 2sig std
        for i in range(len(self.filesDict[self.angleList[0]][0])):
            self.measDict[self.filesDict[self.angleList[0]][0][i]] = [self.filesDict[key][1][i] for key in self.filesDict]
            self.stdDict[self.filesDict[self.angleList[0]][0][i]] = [self.filesDict[key][2][i] for key in self.filesDict]
        try:
            if not self.errorVar.get():
                if not self.fitGVar.get() and not self.fitGVar2.get():
                    for key in self.measDict:
                        plt.scatter(self.angleList, self.measDict[key], color='mediumorchid')
                        plt.xlabel('Angle from specular / deg')
                        plt.ylabel('Power / $\\mathrm{\\mu}$W')
                        plt.show()
                if self.fitGVar.get():
                    self.fitDict = {}
                    for key in self.measDict:
                        try:
                            popt, pcov = curve_fit(GnL, self.angleList, self.measDict[key], p0=[max(self.measDict[key]), 0, 10, (max(self.measDict[key])*0.01)])
                            angs = np.linspace(-20, 120, 1000)
                            fit = GnL(angs, *popt)
                            self.fitDict[key] = [angs, fit, popt, pcov]
                            print(popt, '\n', pcov)
                        except Exception as e:
                            print(e)
                            continue
                    for key in self.measDict:
                        plt.scatter(self.angleList, self.measDict[key], s=10)
                        plt.plot(self.fitDict[key][0], self.fitDict[key][1])
                    plt.xlabel('Angle from specular / deg')
                    plt.ylabel('Power / $\\mathrm{\\mu}$W')
                    plt.show()
                if self.fitGVar2.get():
                    self.fitDict2 = {}
                    self.measDict2 = {}
                    self.angleList2 = self.angleList.copy()
                    self.angleList2.remove(self.angleList2[0])
                    for key in self.measDict:
                        self.measDict2[key] = self.measDict[key].copy()
                        self.measDict2[key].remove(self.measDict2[key][0])
                        try:
                            popt, pcov = curve_fit(GnL, self.angleList2, self.measDict2[key], p0=[(max(self.measDict2[key])+(max(self.measDict2[key])*0.4)), 0, 10, (max(self.measDict2[key])*0.01)])
                            angs = np.linspace(-20, 120, 1000)
                            fit = GnL(angs, *popt)
                            self.fitDict2[key] = [angs, fit, popt, pcov]
                            print(popt, '\n', pcov)
                        except Exception as e:
                            print(e)
                            continue
                    #for key in self.measDict:
                    plt.scatter(self.angleList, self.measDict[15], color='mediumorchid')
                    plt.plot(self.fitDict2[15][0], self.fitDict2[15][1])
                    plt.xlabel('Angle from specular / deg')
                    plt.ylabel('Power / $\\mathrm{\\mu}$W')
                    plt.show()
                    
            elif self.errorVar.get():
                for key in self.filesDict:
                    plt.scatter(self.filesDict[key][0], self.filesDict[key][1], marker='o', s=10, c=self.mColor)
                    plt.errorbar(self.filesDict[key][0], self.filesDict[key][1], yerr=self.filesDict[key][2], fmt='none', capsize=4, c=self.mColor)
            plt.xlabel('Angle from specular / deg')
            plt.ylabel('Power / $\\mathrm{\\mu}$W')
            #plt.show()
        except Exception as e:
            print(e)

    def readMeas(self):
        """Reads current in mA, power and 2*std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
        fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
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
                nameAngles = [('_0deg', 0), ('_10deg', 10), ('_20deg', 20), ('_30deg', 30), 
                              ('_40deg', 40), ('_50deg', 50), ('_60deg', 60), ('_70deg', 70), 
                              ('_100deg', 100), ('_110deg', 110), ('_120deg', 120), ('neg10deg', -10), 
                              ('neg20deg', -20)]
                for tup in nameAngles:
                    if tup[0] in fileNameList[i]:
                        self.filesDict[tup[1]] = ([float(point)*1e3 for point in currTemp], [(float(point)-float(measTemp[0]))*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
                
        self.clearDataBut.configure(state='normal')

    def clear(self):
        #self.angleList.clear()
        self.measList.clear()
        self.stdList.clear()
        self.filesDict.clear()
        self.clearDataBut.configure(state='disabled')

def main():
    root = Tk()
    apGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()