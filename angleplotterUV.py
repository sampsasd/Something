import pyvisa as visa
from tkinter import Tk, IntVar
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename, askopenfilenames
from time import sleep
import threading
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

class ap2GUI:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title('Angle Plotter 2')
        self.master.configure(background='black')
        self.master.state('zoomed')

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

        #===================================FRAMES===================================================

        self.frm = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.frm.place(in_=self.master, anchor='center', relx=.5, rely=.6)

        self.titleframe = Frame(self.master, style='my.TFrame', padding='0.5i')
        self.titleframe.place(in_=self.master, anchor='center', relx=.5, rely=.2)

        self.hp = Label(self.titleframe, text='Harry Plotter and the Prisoner of Optics Room', style='my.TLabel')
        self.hp.grid(column=0, row=0)

        #===============================BUTTONS N STUFF=====================================================

        self.plotBut = Button(self.frm, text='Plot', style='my.TButton')
        self.plotBut.grid(column=0, row=0, padx=5, pady=5)

        self.filesBut = Button(self.frm, text='Select Files', command=self.readData, style='my.TButton')
        self.filesBut.grid(column=0, row=1, padx=5, pady=5)

        #=======================================FUNCTIONS======================================================

    def readData(self):
        #REMEMBER TO FIX SAVE DATA IN CURRENT SWEEP TO ANGLE, CURRENT, POWER, STD
        fileNameList = askopenfilenames(initialdir='./AppsNshit/Data', filetypes=(('csv files', 'csv'), ))
        for i in range(len(fileNameList)):
            angTemp = []
            currTemp = []
            measTemp = []
            stdTemp = []
            with open(fileNameList[i], 'r') as file:
                for row in file:
                    points = row.strip(). split(', ')
                    #HERE HERE 






def main():
    root = Tk()
    ap2GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()