import pyvisa as visa
from tkinter import Tk, IntVar
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from time import sleep
import threading
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

class apGUI:
    def __init__(self, master) -> None:

        self.master = master
        self.master.title('Angle Plotter')
        self.master.attributes('-fullscreen', True)
        self.master.configure(background='black')

        self.angleList = [0, 10, 20, 30, 40, 50, 60, 70, 80]
        self.currentList = []
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

        self.hp = Label(self.titleframe, text='Harry Plotter and the Chamber of Optics', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #=============================BUTTONS==================================================

        self.multiVar = IntVar(value=0)
        self.multiCheck = Checkbutton(self.frm, text='Plot multiple', style='my.TCheckbutton', variable=self.multiVar, onvalue=1, offvalue=0)
        self.multiCheck.grid(column=0, row=2, padx=5, pady=5)

        self.fileBut = Button(self.frm, text='File(s)', style='my.TButton', command=self.readMeas)
        self.fileBut.grid(column=0, row=3, padx=5, pady=5)

        self.clearDataBut = Button(self.frm, text='Clear data', style='my.TButton', command=self.clear)
        self.clearDataBut.configure(state='disabled')
        self.clearDataBut.grid(column=0, row=4, padx=5, pady=5)

        self.scatterBut = Button(self.frm, text='Scatter', style='my.TButton', command=self.scatter)
        self.scatterBut.grid(column=0, row=0, padx=20, pady=20)

        self.errorVar = IntVar(value=0)
        self.errorCheck = Checkbutton(self.frm, text='Errorbar', variable=self.errorVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.errorCheck.grid(column=0, row=1, padx=5, pady=5)



        self.destructionBut = Button(self.frm, text='Close', style='my.TButton', command=self.master.quit)
        self.destructionBut.grid(column=0, row=100, padx=30, pady=30)

        

    def scatter(self):
        """Scatters  Power / uW as a function of current / mA"""

        if not self.multiVar.get():
            try:
                plt.scatter(self.angleList, self.measList, marker='o', s=10, c='mediumorchid')
                if self.errorVar.get():
                    plt.errorbar(self.angleList, self.measList, yerr=self.stdList, fmt='none', capsize=4, c='mediumorchid')
                plt.xlabel('Angle from specular / deg')
                plt.ylabel('Power / $\\mathrm{\\mu}$W')
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
                plt.xlabel('Angle from specular / deg')
                plt.ylabel('Power / $\\mathrm{\\mu}$W')
                plt.show()
            except Exception as e:
                print(e)

    

    def readMeas(self):
        """Reads current in mA, power and 2*std in uW.\n
        Deletes first row of file and assumes ', ' separator"""
        
        if not self.multiVar.get():
            fileName = askopenfilename(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
            with open(fileName, 'r') as file:
                for row in file:
                    points = row.strip().split(', ')
                    self.currentList.append(points[0])
                    self.measList.append(points[1])
                    self.stdList.append(points[2])
                self.currentList.remove(self.currentList[0])
                self.measList.remove(self.measList[0])
                self.stdList.remove(self.stdList[0])
                if self.currentList[0] != '-':
                    self.currentList = [float(point)*1e3 for point in self.currentList]
                self.measList = [float(point)*1e6 for point in self.measList]
                self.stdList = [2*float(point)*1e6 for point in self.stdList]
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
                        self.filesDict[i] = ([float(point)*1e3 for point in currTemp], [float(point)*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
                    else:
                        self.filesDict[i] = (currTemp, [float(point)*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
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