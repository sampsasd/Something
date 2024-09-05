import pyvisa as visa
from tkinter import Tk, IntVar
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from time import sleep
import threading
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from FileHandler import ReadJson

class ap2GUI:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title('Angle Plotter 3')
        self.master.configure(background='black')
        self.master.state('zoomed')

        self.angleList = []
        self.powerList = []
        self.sigmaList = []
        self.dataDict = {}
        self.current = 50e-3
        self.incAng = '-'

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
        
        self.sbStyle = Style()
        self.sbStyle.theme_use('classic')
        self.sbStyle.configure(style='my.Vertical.TScrollbar', font=('Helvetica', 15))
        self.sbStyle.map('my.Vertical.TScrollbar', 
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

        #===================================FRAMES===================================================

        self.frm = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.frm.place(in_=self.master, anchor='center', relx=.5, rely=.6)

        self.titleframe = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.titleframe.place(in_=self.master, anchor='center', relx=.5, rely=.2)

        self.hp = Label(self.titleframe, text='Harry Plotter and the Prisoner of Optics Room', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #===============================BUTTONS N STUFF=====================================================

        self.plotBut = Button(self.frm, text='Plot', command=self.plotData, style='my.TButton')
        self.plotBut.grid(column=1, row=0, padx=5, pady=5)
        self.plotBut.config(state='disabled')

        self.errorVar = IntVar(value=0)
        self.errorCheck = Checkbutton(self.frm, text='Errorbars', style='my.TCheckbutton', variable=self.errorVar, onvalue=1, offvalue=0)
        self.errorCheck.grid(column=2, row=0, padx=5, pady=5)

        self.currLab = Label(self.frm, text='Current: ', style='my.TLabel')
        self.currLab.grid(column=0, row=1, padx=5, pady=5)
        self.currEn = Entry(self.frm, style='my.TEntry')
        self.currEn.bind('<Return>', self.setCurrent)
        self.currEn.grid(column=1, row=1, padx=5, pady=5)
        self.currLabel = Label(self.frm, text=f'{self.current} A', style='my.TLabel')
        self.currLabel.grid(column=2, row=1, padx=5, pady=5)

        self.incAngLab = Label(self.frm, text='Incident Angle: ', style='my.TLabel')
        self.incAngLab.grid(column=0, row=2, padx=5, pady=5)
        self.incAngEn = Entry(self.frm, style='my.TEntry')
        self.incAngEn.bind('<Return>', self.setIncAng)
        self.incAngEn.grid(column=1, row=2, padx=5, pady=5)
        self.incAngLabel = Label(self.frm, text=f'{self.incAng}', style='my.TLabel')
        self.incAngLabel.grid(column=2, row=2, padx=5, pady=5)

        self.filesBut = Button(self.frm, text='Select File', command=self.readData, style='my.TButton')
        self.filesBut.grid(column=1, row=3, padx=5, pady=5)

        self.clearBut = Button(self.frm, text='Clear Data', command=self.clearData, style='my.TButton')
        self.clearBut.grid(column=1, row=4, padx=20, pady=20)
        self.clearBut.config(state='disabled')
        
        #=======================================FUNCTIONS======================================================

    def setIncAng(self, event=None):
        self.incAng = int(self.incAngEn.get())
        self.incAngEn.delete(0, 'end')
        self.incAngLabel.config(text=f'{self.incAng} deg')

    def interpolateData(self):
        """Takes fit parameters and interpolates power and 2 sigma error for given current"""
        for angle in self.dataDict:
            self.angleList.append(int(angle))
            self.powerList.append(self.dataDict[angle][0][1] * self.current)
            self.sigmaList.append(2 * np.sqrt(self.dataDict[angle][1][1][1]) * self.current + 2 * np.sqrt(self.dataDict[angle][1][0][0]))
        print(self.angleList, self.powerList, self.sigmaList)

    def setCurrent(self, event=None):
        self.current = float(self.currEn.get())
        self.currLabel.config(text=f'{self.current} A')
        self.currEn.delete(0, 'end')

        self.angleList.clear()
        self.powerList.clear()
        self.sigmaList.clear()
        self.interpolateData()

    def readData(self):
        """Returns self.filesDict"""
        #REMEMBER TO FIX SAVE DATA IN CURRENT SWEEP TO ANGLE, CURRENT, POWER, STD
        try:
            fileName = askopenfilename(initialdir='./AppsNshit/Data')
            self.dataDict = ReadJson(fileName)
            
            self.plotBut.config(state='normal')
            self.clearBut.config(state='normal')
            self.filesBut.config(state='disabled')

            self.interpolateData()
        except Exception as e:
            print(e)
    
    def plotData(self):
        plt.scatter(self.angleList, self.powerList, s=10, c='mediumorchid')
        if self.errorVar.get():
            plt.errorbar(self.angleList, self.powerList, yerr=self.sigmaList, fmt='none', capsize=4, c='mediumorchid')
        if self.incAng != '-':
            plt.vlines(self.incAng, 0, (max(self.powerList)+0.1*max(self.powerList)), colors='black', linewidths=1, linestyles=':', label='Incident angle')
        plt.xticks(np.arange(-90, 91, 10))
        plt.xlabel('Angle from surface normal / deg')
        plt.ylabel('Power / W')
        plt.legend(loc=0)

        plt.tight_layout()
        plt.show()

    def clearData(self):
        self.dataDict.clear()
    
        self.clearBut.config(state='disabled')
        self.plotBut.config(state='disabled')
        self.filesBut.config(state='normal')





def main():
    root = Tk()
    ap2GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()