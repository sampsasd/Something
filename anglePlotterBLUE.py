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

class ap4GUI:
    def __init__(self, master) -> None:

        self.master = master
        self.master.title('Angle Plotter 4')
        self.master.geometry('300x600')
        self.master.state('zoomed')
        self.master.configure(background='black')

        self.refAngleList = []
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

        #=======================================FRAMES=======================================================
        self.frm = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.frm.place(in_=self.master, anchor='center', relx=.5, rely=.6)

        self.titleframe = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.titleframe.place(in_=self.master, anchor='center', relx=.5, rely=.2)

        self.hp = Label(self.titleframe, text='Harry Plotter and the Goblet of TPB', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #=============================BUTTONS==================================================

        self.scatterBut = Button(self.frm, text='Scatter', style='my.TButton', command=self.scatter)
        self.scatterBut.grid(column=0, row=0, padx=20, pady=20)

        self.multiVar = IntVar(value=0)
        self.multiCheck = Checkbutton(self.frm, text='Plot multiple', variable=self.multiVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.multiCheck.grid(column=0, row=1, padx=5, pady=5)

        self.errorVar = IntVar(value=0)
        self.errorCheck = Checkbutton(self.frm, text='Errorbar', variable=self.errorVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        self.errorCheck.grid(column=0, row=2, padx=5, pady=5)

        # self.fitGVar = IntVar(value=0)
        # self.fitGCheck = Checkbutton(self.frm, text='Fit spherical Gaussian', variable=self.fitGVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
        # self.fitGCheck.grid(column=0, row=3, padx=5, pady=5)

        # self.fitGVar3 = IntVar(value=0)
        # self.fitGCheck3 = Checkbutton(self.frm, text='Fit Gaussian', variable=self.fitGVar3, onvalue=1, offvalue=0, style='my.TCheckbutton')
        # self.fitGCheck3.grid(column=1, row=3, padx=5, pady=5)

        # self.fitGVar2 = IntVar(value=0)
        # self.fitGCheck2 = Checkbutton(self.frm, text='Fit Gauss + Lambert (Exc. Specular)', variable=self.fitGVar2, onvalue=1, offvalue=0, style='my.TCheckbutton')
        # self.fitGCheck2.grid(column=0, row=4, padx=5, pady=5)

        self.fileBut = Button(self.frm, text='Files', style='my.TButton', command=self.readData)
        self.fileBut.grid(column=0, row=3, padx=5, pady=5)

        self.clearDataBut = Button(self.frm, text='Clear data', style='my.TButton', command=self.clear)
        self.clearDataBut.configure(state='disabled')
        self.clearDataBut.grid(column=0, row=4, padx=5, pady=5)
    
    def scatter(self):
        pass

    def readData(self):
        """Reads data from csv (angle, current, power, std) and saves to class datalist attributes"""

        if not self.multiVar.get():
            filename = askopenfilename(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
            with open(filename, 'r') as file:
                for row in file:
                    points = row.strip().split(', ')
                    self.refAngleList.append(points[0])
                    self.currentList.append(points[1])
                    self.measList.append(points[2])
                    self.stdList.append(points[3])

    def clear(self):
        pass


def main():
    root = Tk()
    gui = ap4GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()