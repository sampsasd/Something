import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfilenames, asksaveasfilename
from tkinter.ttk import *
from tkinter import Tk, IntVar
from scipy.optimize import curve_fit
from functions import line
from FileHandler import WriteJson, ReadJson
from statsmodels.api import WLS
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import statsmodels.regression.linear_model as srlm

class plotGUI:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title("Harry Plotter")
        self.master.configure(background='black')
        self.master.state('zoomed')
        self.angle = None
        self.currentList = []
        self.measList = []
        self.stdList = []
        self.filesDict = {}
        self.paramDict = {}
        self.filterCoeff = 0.05
        self.mColor = 'mediumorchid'

        self.frmStyle = Style()
        self.frmStyle.theme_use('classic')
        self.frmStyle.configure('my.TFrame', background='black')
        self.frm = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.frm.place(in_=self.master, anchor='center', relx=.5, rely=.5)

        self.titleframe = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.titleframe.place(in_=self.master, anchor='center', relx=.5, rely=.2)
        
        #===============================HARRY STYLES========================================================
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
        self.labStyle.configure(style='my.TLabel', font=('Helvetica', 15))
        self.butStyle.map('my.TLabel', 
                          background=[('!active', 'black'), ('pressed', 'red'), ('active', 'maroon')], 
                          foreground=[('!active', 'red'), ('pressed', 'black'), ('active', 'black')])

        #==========================TITLE========================================================================

        self.hp = Label(self.titleframe, text='Harry Plotter and the Physicist\'s Stones', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #==============================BUTTONS N STUFF===================================================================

        self.multiVar = IntVar(value=0)
        self.multiCheck = Checkbutton(self.frm, text='Plot multiple', style='my.TCheckbutton', variable=self.multiVar, onvalue=1, offvalue=0)
        self.multiCheck.grid(column=0, row=0, padx=10, pady=10)

        self.fileBut = Button(self.frm, text='File(s)', style='my.TButton', command=self.readMeas)
        self.fileBut.grid(column=0, row=1, padx=10, pady=10)

        self.clearDataBut = Button(self.frm, text='Clear data', style='my.TButton', command=self.clear)
        self.clearDataBut.configure(state='disabled')
        self.clearDataBut.grid(column=0, row=2)

        #self.destructionBut = Button(self.frm, text='Close', style='my.TButton', command=self.DESTRUCTION)
        #self.destructionBut.grid(column=0, row=100, padx=20, pady=20)

        self.colorLab = Label(self.frm, text='Color:', style='my.TLabel')
        self.colorLab.grid(column=1, row=0, padx=10, pady=10)
        self.colorEn = Entry(self.frm)
        self.colorEn.bind('<Return>', self.setColor)
        self.colorEn.grid(column=2, row=0)
        self.colorLabel = Label(self.frm, text=self.mColor, style='my.TLabel')
        self.colorLabel.grid(column=3, row=0, padx=10, pady=10)

        self.filterLab = Label(self.frm, text='Filter Coeff: ', style='my.TLabel')
        self.filterLab.grid(column=1, row=1, padx=10, pady=10)
        self.filterEn = Entry(self.frm)
        self.filterEn.bind('<Return>', self.setFilter)
        self.filterEn.grid(column=2, row=1)
        self.filterLabel = Label(self.frm, text=f'{self.filterCoeff}', style='my.TLabel')
        self.filterLabel.grid(column=3, row=1, padx=10, pady=10)

        self.filterVar = IntVar(value=0)
        self.filterCheck = Checkbutton(self.frm, text='Filter', variable=self.filterVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.filterCheck.grid(column=4, row=1, padx=10, pady=10)

        self.twinxVar = IntVar(value=0)
        self.twinxCheck = Checkbutton(self.frm, text='Twinx', style='my.TCheckbutton', variable=self.twinxVar, onvalue=1, offvalue=0)
        self.twinxCheck.grid(column=1, row=2, padx=10, pady=10)

        self.errorVar = IntVar(value=0)
        self.errorCheck = Checkbutton(self.frm, text='Errorbar', variable=self.errorVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.errorCheck.grid(column=2, row=2, padx=10, pady=10)

        self.scatterBut = Button(self.frm, text='Scatter', style='my.TButton', command=self.scatter)
        self.scatterBut.grid(column=5, row=0, padx=10, pady=10)

        self.appendBut = Button(self.frm, text='Append params', style='my.TButton', command=self.appendParams)
        self.appendBut.grid(column=5, row=1, padx=10, pady=10)

        self.saveParamsBut = Button(self.frm, text='Save Params', style='my.TButton', command=self.saveParams)
        self.saveParamsBut.grid(column=5, row=2, padx=10, pady=10)

        self.clearParamsBut = Button(self.frm, text='Clear Params', style='my.TButton', command=self.clearParams)
        self.clearParamsBut.grid(column=5, row=3, padx=10, pady=20)
        self.clearParamsBut.config(state='disabled')

    #==================================FUNC=================================================================

    def clearParams(self):
        self.paramDict.clear()
        self.clearParamsBut.config(state='disabled')

    def saveParams(self):
        fName = asksaveasfilename(initialdir='./AppsNshit/Data')
        WriteJson(fName, self.paramDict)
        self.paramDict.clear()
        self.clearParamsBut.config(state='disabled')

    def appendParams(self):
        """WITH WLS THE PARAMETERS ARE LIKE b + ax AND NOT ax + b"""
        if not self.multiVar.get():
            self.paramDict[self.angle] = ([self.popt[0], self.popt[1]], [[self.pcov[0][0], self.pcov[0][1]], [self.pcov[1][0], self.pcov[1][1]]])
            self.clearParamsBut.config(state='normal')
            print(self.paramDict)
        if self.multiVar.get():
            for ang in self.poptDict:
                self.paramDict[ang] = ([self.poptDict[ang][0][0], self.poptDict[ang][0][1]], 
                                       [[self.poptDict[ang][1][0][0], self.poptDict[ang][1][0][1]], 
                                        [self.poptDict[ang][1][1][0], self.poptDict[ang][1][1][1]]])
            print(self.paramDict)

    def scatter(self):
        """Scatters  Power / uW as a function of current / mA"""

        if not self.multiVar.get():
            if self.filterVar.get():
                try:
                    self.filterData()
                    plt.scatter(self.currentListFiltered, self.measListFiltered, marker='o', s=10, c=self.mColor)
                    #plt.plot(self.currentListFiltered, self.intervalLow, color='blue', ls=':')
                    #plt.plot(self.currentListFiltered, self.intervalUp, color='blue', ls=':')
                    if self.errorVar.get():
                        plt.errorbar(self.currentListFiltered, self.measListFiltered, yerr=self.stdListFiltered, fmt='none', capsize=4, c=self.mColor)
                    fitCurrent = np.linspace(0, 100e-3, 100)
                    plotFit = line(fitCurrent, self.popt[1], self.popt[0])
                    plt.plot(fitCurrent, plotFit, label=f'{self.popt[1]:.3e} * $I$ + {self.popt[0]:.3e}')
                    plt.xlabel('Current / A')
                    plt.ylabel('Power / W')
                    plt.legend()
                    plt.show()
                except Exception as e:
                    print(e)
            else:
                try:
                    plt.scatter(self.currentList, self.measList, marker='o', s=10, c=self.mColor)
                    if self.errorVar.get():
                        plt.errorbar(self.currentList, self.measList, yerr=self.stdList, fmt='none', capsize=4, c=self.mColor)
                    plt.xlabel('Current / A')
                    plt.ylabel('Power / W')
                    plt.show()
                except Exception as e:
                    print(e)

        if self.multiVar.get():
            if self.filterVar.get():
                try:
                    self.filterData()
                    if not self.errorVar.get():
                        for ang in self.filesDictFiltered:
                            plt.scatter(self.filesDictFiltered[ang][0], self.filesDictFiltered[ang][1], marker='o', s=10)
                            fitCurrent = np.linspace(0, 100e-3, 100)
                            plotFit = line(fitCurrent, self.poptDict[ang][0][1], self.poptDict[ang][0][0])
                            plt.plot(fitCurrent, plotFit, label=f'{self.poptDict[ang][0][1]:.3e} * $I$ + {self.poptDict[ang][0][0]:.3e}')
                    # if self.errorVar.get():
                    #     for key in self.filesDict:
                    #         plt.scatter(self.filesDict[key][0], self.filesDict[key][1], marker='o', s=10, c=self.mColor)
                    #         plt.errorbar(self.filesDict[key][0], self.filesDict[key][1], yerr=self.filesDict[key][2], fmt='none', capsize=4, c=self.mColor)
                    plt.xlabel('Current / A')
                    plt.ylabel('Power / W')
                    plt.legend()
                    plt.show()
                except Exception as e:
                    print(e)
            if not self.filterVar.get():
                try:
                    if not self.errorVar.get():
                        for ang in self.filesDict:
                            plt.scatter(self.filesDict[ang][0], self.filesDict[ang][1], marker='o', s=10)
                    if self.errorVar.get():
                         for key in self.filesDict:
                             plt.scatter(self.filesDict[key][0], self.filesDict[key][1], marker='o', s=10, c=self.mColor)
                             plt.errorbar(self.filesDict[key][0], self.filesDict[key][1], yerr=self.filesDict[key][2], fmt='none', capsize=4, c=self.mColor)
                    plt.xlabel('Current / A')
                    plt.ylabel('Power / W')
                    plt.legend()
                    plt.show()
                except Exception as e:
                    print(e)

    def setColor(self, event=None):
        """Pretty colors for scatterplot yes :)"""
        self.mColor = self.colorEn.get()
        self.colorLabel.config(text=self.mColor)
        self.colorEn.delete(0, 'end')

    def clear(self):
        self.currentList.clear()
        self.measList.clear()
        self.stdList.clear()
        self.filesDict.clear()
        self.clearDataBut.configure(state='disabled')

    def readMeas(self):
        """Reads current in mA, power and std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
        if not self.multiVar.get():
            fileName = askopenfilename(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
            with open(fileName, 'r') as file:
                rows = list(file)
                rows.pop(0)
                for row in rows:
                    points = row.strip().split(', ')
                    self.currentList.append(points[1])
                    self.measList.append(points[2])
                    self.stdList.append(points[3])
                if self.currentList[0] != '-':
                    self.currentList = [float(point) for point in self.currentList]
                self.measList = [float(point) for point in self.measList]
                self.stdList = [float(point) for point in self.stdList]
                self.angle = int(points[0])
            
            self.clearDataBut.configure(state='normal')
        if self.multiVar.get():
            fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
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
                        self.filesDict[angle] = ([float(point) for point in currTemp], [float(point) for point in measTemp], [float(point) for point in stdTemp])
                    else:
                        self.filesDict[angle] = (currTemp, [float(point) for point in measTemp], [float(point) for point in stdTemp])
            self.clearDataBut.configure(state='normal')

    def setFilter(self, event=None):
        self.filterCoeff = float(self.filterEn.get())
        self.filterLabel.config(text=f'{self.filterCoeff}')
        self.filterEn.delete(0, 'end')

    def filterData(self, event=None):

        if not self.multiVar.get():
            self.currentListFiltered = self.currentList.copy()
            self.measListFiltered = self.measList.copy()
            self.stdListFiltered = self.stdList.copy()

            while True:
                newIter = False
                weights = [1/(point**2) for point in self.stdListFiltered]
                xDataForWLS = sm.add_constant(self.currentListFiltered)
                wlsFit = WLS(self.measListFiltered, xDataForWLS, weights=weights).fit()
                self.popt = wlsFit.params
                self.pcov = wlsFit.cov_params()

                self.prstd, self.intervalLow, self.intervalUp = wls_prediction_std(wlsFit)

                #self.popt, self.pcov = curve_fit(line, self.currentListFiltered, self.measListFiltered)
                print(self.popt, self.pcov)
                self.fit = [line(self.currentListFiltered[i], self.popt[1], self.popt[0]) for i in range(len(self.currentListFiltered))]
                #ERRORS HERE U DUMB FUCK=============================================================================================================================================================================================
                i = 0
                while i < len(self.fit):
                    if self.measListFiltered[i] > self.fit[i] + self.filterCoeff * self.fit[i]:
                        self.currentListFiltered.remove(self.currentListFiltered[i])
                        self.measListFiltered.remove(self.measListFiltered[i])
                        self.stdListFiltered.remove(self.stdListFiltered[i])
                        self.fit.remove(self.fit[i])
                        newIter = True
                    else:
                        i += 1

                if not newIter:
                    break

        if self.multiVar.get():
            self.filesDictFiltered = {}
            self.poptDict = {}
            self.fitDict = {}
            
            for ang in self.filesDict:
                self.filesDictFiltered[ang] = (self.filesDict[ang][0].copy(), self.filesDict[ang][1].copy(), self.filesDict[ang][2].copy())
            
            for ang in self.filesDictFiltered:
                while True:
                    newIter = False
                    weights = [1/(point**2) for point in self.filesDictFiltered[ang][2]]
                    xDataForWLS = sm.add_constant(self.filesDictFiltered[ang][0])
                    wlsFit = WLS(self.filesDictFiltered[ang][1], xDataForWLS, weights=weights).fit()
                    self.poptDict[ang] = wlsFit.params, wlsFit.cov_params()

                    #self.prstd, self.intervalLow, self.intervalUp = wls_prediction_std(wlsFit)

                    #self.popt, self.pcov = curve_fit(line, self.currentListFiltered, self.measListFiltered)
        
                    self.fitDict[ang] = [line(self.filesDictFiltered[ang][0][i], self.poptDict[ang][0][1], self.poptDict[ang][0][0]) for i in range(len(self.filesDictFiltered[ang][0]))]
                    #ERRORS HERE U DUMB FUCK=============================================================================================================================================================================================
                    i = 0
                    while i < len(self.fitDict[ang]):
                        if self.filesDictFiltered[ang][1][i] > self.fitDict[ang][i] + self.filterCoeff * self.fitDict[ang][i]:
                            self.filesDictFiltered[ang][0].remove(self.filesDictFiltered[ang][0][i])
                            self.filesDictFiltered[ang][1].remove(self.filesDictFiltered[ang][1][i])
                            self.filesDictFiltered[ang][2].remove(self.filesDictFiltered[ang][2][i])
                            self.fitDict[ang].remove(self.fitDict[ang][i])
                            newIter = True
                        else:
                            i += 1

                    if not newIter:
                        print(self.poptDict)
                        break

    def DESTRUCTION(self):
        self.master.quit()

def main():
    root = Tk()
    plotGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()