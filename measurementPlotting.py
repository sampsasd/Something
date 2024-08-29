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

    #==================================FUNC=================================================================

    def clearParams(self):
        self.paramDict.clear()

    def saveParams(self):
        fName = asksaveasfilename(initialdir='./AppsNshit/Data')
        WriteJson(fName, self.paramDict)

    def appendParams(self):
        self.paramDict[self.angle] = ([self.popt[0], self.popt[1]], [[self.pcov[0][0], self.pcov[0][1]], [self.pcov[1][0], self.pcov[1][1]]])
        print(self.paramDict)

    def scatter(self):
        """Scatters  Power / uW as a function of current / mA"""

        if not self.multiVar.get():
            if self.filterVar.get():
                try:
                    self.filterData()
                    plt.scatter(self.currentListFiltered, self.measListFiltered, marker='o', s=10, c=self.mColor)
                    if self.errorVar.get():
                        plt.errorbar(self.currentListFiltered, self.measListFiltered, yerr=self.stdListFiltered, fmt='none', capsize=4, c=self.mColor)
                    plt.plot(self.currentListFiltered, self.fit, label=f'{self.popt[0]:.3e} * $I$ + {self.popt[1]:.3e}')
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
            try:
                if not self.errorVar.get():
                    for key in self.filesDict:
                        plt.scatter(self.filesDict[key][0], self.filesDict[key][1], marker='o', s=10, c=self.mColor)
                if self.errorVar.get():
                    for key in self.filesDict:
                        plt.scatter(self.filesDict[key][0], self.filesDict[key][1], marker='o', s=10, c=self.mColor)
                        plt.errorbar(self.filesDict[key][0], self.filesDict[key][1], yerr=self.filesDict[key][2], fmt='none', capsize=4, c=self.mColor)
                plt.xlabel('Current / A')
                plt.ylabel('Power / W')
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
        """Reads current in mA, power and 2*std in uW.\n
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
                self.stdList = [2*float(point) for point in self.stdList]
                self.angle = int(points[0])
            
            self.clearDataBut.configure(state='normal')
        if self.multiVar.get():
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
                    if currTemp[0] != '-':
                        self.filesDict[i] = ([float(point) for point in currTemp], [float(point) for point in measTemp], [2*float(point) for point in stdTemp])
                    else:
                        self.filesDict[i] = (currTemp, [float(point) for point in measTemp], [2*float(point) for point in stdTemp])
            self.clearDataBut.configure(state='normal')

    def setFilter(self, event=None):
        self.filterCoeff = float(self.filterEn.get())
        self.filterLabel.config(text=f'{self.filterCoeff}')
        self.filterEn.delete(0, 'end')

    def filterData(self, event=None):

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

        # for i in range(len(self.currentList)):
        #     if i == 0:
        #         self.currentListFiltered.append(self.currentList[i])
        #         self.measListFiltered.append(self.measList[i])
        #         self.stdListFiltered.append(self.stdList[i])
        #     elif self.measList[i] > self.measList[i-1] + self.filterCoeff * self.measList[i-1]:
        #         continue
        #     else:
        #         self.currentListFiltered.append(self.currentList[i])
        #         self.measListFiltered.append(self.measList[i])
        #         self.stdListFiltered.append(self.stdList[i])

    def DESTRUCTION(self):
        self.master.quit()

def main():
    root = Tk()
    plotGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()