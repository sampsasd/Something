import pyvisa as visa
from tkinter import Tk
from tkinter.ttk import *
from tkinter import simpledialog, filedialog
from time import sleep
import threading
import tkinter as tk
import numpy as np

class laserGUI:
    def __init__(self, master) -> None:
        
        self.master = master
        self.master.title('Laser Current Sweep')
        self.master.configure(background='black')

        self.darkmode = Style()
        self.darkmode.theme_use('alt')
        self.darkmode.configure(style='my.TFrame', background='black')
        self.frm = Frame(self.master, padding='1i', style='my.TFrame')
        self.frm.grid()

        #=================================STYLES===============================================

        self.butStyle = Style()
        self.butStyle.theme_use('alt')
        self.butStyle.configure(style='my.TButton', font=('Helvetica', 18), background='black', foreground='red')
        self.butStyle.map('TButton', background=[('active', 'red')], foreground=[('active', 'black')])
        self.enStyle = Style()
        self.enStyle.theme_use('alt')
        self.enStyle.configure("my.TEntry", background='black', foreground='black')
        self.labStyle = Style()
        self.labStyle.configure(style='my.TLabel', font=('Helvetica', 18), background='black', foreground='red')
        self.checkStyle = Style()
        self.checkStyle.theme_use('alt')
        self.checkStyle.configure(style='my.TCheckbutton', font=('Helvetica', 18), background='black', foreground='red')

        #====================================BUTTONS==============================

        self.destructionBut = Button(self.frm, text='Close', command=self.master.quit, style='my.TButton')
        self.destructionBut.grid(column=1, row=100, padx=10, pady=10)

        try:

            #self.rm = visa.ResourceManager()
            #rList = self.rm.list_resources()
            #print(rList)
            #self.instr = self.rm.open_resource('NAME HERE')

            #STARTI
            self.startILab = Label(self.frm, text="Start current: ", style='my.TLabel')
            self.startILab.grid(column=0, row=2, padx=10, pady=10)
            self.startIEn = Entry(self.frm)
            self.startIEn.grid(column=1, row=2)
            self.startIEn.bind('<Return>', self.setStartCurrent)
            self.startILabel = Label(self.frm, text=f"- A", style='my.TLabel')
            self.startILabel.grid(column=2, row=2, padx=10, pady=10)

            #STOPI
            self.stopILab = Label(self.frm, text="Stop current: ", style='my.TLabel')
            self.stopILab.grid(column=0, row=3, padx=10, pady=10)
            self.stopIEn = Entry(self.frm)
            self.stopIEn.grid(column=1, row=3)
            self.stopIEn.bind('<Return>', self.setStopCurrent)
            self.stopILabel = Label(self.frm, text=f"- A", style='my.TLabel')
            self.stopILabel.grid(column=2, row=3, padx=10, pady=10)

            #STEPI
            self.stepILab = Label(self.frm, text="Current step: ", style='my.TLabel')
            self.stepILab.grid(column=0, row=4, padx=10, pady=10)
            self.stepIEn = Entry(self.frm)
            self.stepIEn.grid(column=1, row=4)
            self.stepIEn.bind('<Return>', self.setStepCurrent)
            self.stepILabel = Label(self.frm, text=f"- A", style='my.TLabel')
            self.stepILabel.grid(column=2, row=4, padx=10, pady=10)

            #RUN
            self.onOffBut = Button(self.frm, text="Run", command=self.runThread, style='my.TButton')
            self.onOffBut.grid(column=1, row=5)

            #Stahp
            self.stahpBut = Button(self.frm, text='Stop', command=self.stahp, style='my.TButton')
            self.stahpBut.grid(column=1, row=6)
            self.stahpBut.config(state='disabled')

        except Exception as e:

            print(e)
            self.noDeviceLab = Label(self.frm, text='No device', style='my.TButton')
            self.noDeviceLab.grid(column=1, row=0, padx=10, pady=10)
    
    def setStartCurrent(self, event=None):
        pass

    def setStopCurrent(self, event=None):
        pass

    def setStepCurrent(self, event=None):
        pass

    def runThread(self):
        pass

    def stahp(self):
        pass



def main():
    root = Tk()
    laserGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()