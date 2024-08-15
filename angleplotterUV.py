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
        self.dataDict = {}

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
        self.plotBut.grid(column=0, row=0, padx=5, pady=5)
        self.plotBut.config(state='disabled')

        self.filesBut = Button(self.frm, text='Select Files', command=self.readData, style='my.TButton')
        self.filesBut.grid(column=0, row=1, padx=5, pady=5)





        
        self.shitFrame = Frame(self.frm, style='my.TFrame')
        self.shitFrame.grid(column=0, row=2, padx=5, pady=5)
        

        self.dataCanvas = tk.Canvas(self.shitFrame, borderwidth=0, width=200, height=200, background='black')
        self.dataCanvas.pack(side='left', fill='both', expand=True)
        
        self.scroller = Scrollbar(self.shitFrame, orient='vertical', command=self.dataCanvas.yview, style='my.Vertical.TScrollbar')
        self.scroller.pack(side='right', fill='y')
        
        self.dataFrame = Frame(self.dataCanvas, style='my.TFrame')
        #self.dataFrame.bind('<Configure>', self.on_frame_configure)
        self.dataCanvas.create_window((2, 2), window=self.dataFrame, anchor='nw')

        
        
        



        self.clearBut = Button(self.frm, text='Clear Data', command=self.clearData, style='my.TButton')
        self.clearBut.grid(column=0, row=4, padx=20, pady=20)
        self.clearBut.config(state='disabled')
        
        #=======================================FUNCTIONS======================================================

    def on_frame_configure(self):
        self.dataCanvas.configure(scrollregion=self.dataCanvas.bbox())

    def readData(self):
        """Saves (angle, current, power, std) with int keys into self.filesDict"""
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
                    angTemp.append(points[0])
                    currTemp.append(points[1])
                    measTemp.append(points[2])
                    stdTemp.append(points[3])
                angTemp.remove(angTemp[0])
                currTemp.remove(currTemp[0])
                measTemp.remove(measTemp[0])
                stdTemp.remove(stdTemp[0])
                
                self.filesDict[i] = ([int(point) for point in angTemp], [float(point)*1e3 for point in currTemp], [(float(point)-float(measTemp[0]))*1e6 for point in measTemp], [2*float(point)*1e6 for point in stdTemp])
        
        #No comment
        self.dataDict = {}
        for key in self.filesDict:
            for current in self.filesDict[key][1]:
                if current in self.dataDict:
                    self.dataDict[current][0].append(self.filesDict[key][0])
                    self.dataDict[current][1].append(self.filesDict[key][2])
                    self.dataDict[current][2].append(self.filesDict[key][3])
                else:
                    self.dataDict[current] = [[self.filesDict[key][0]], [self.filesDict[key][2]], self.filesDict[key][3]]
        
        self.checkDict = {}
        for key in self.dataDict:
            tempVar = IntVar(value=1)
            tempCheck = Checkbutton(self.dataFrame, text=f'{key} mA', variable=tempVar, onvalue=1, offvalue=0, style='my.TCheckbutton')
            tempCheck.pack(side='top', fill='x')
            self.checkDict[key] = [tempVar, tempCheck]
        
        self.plotBut.config(state='normal')
        self.clearBut.config(state='normal')
    
    def plotData(self):
        pass

    def clearData(self):
        self.dataDict.clear()
        for key in self.checkDict:
            self.checkDict[key][1].destroy()
        self.checkDict.clear()
        self.clearBut.config(state='disabled')
        self.plotBut.config(state='disabled')





def main():
    root = Tk()
    ap2GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()