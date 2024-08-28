import pyvisa as visa
from tkinter import Tk
from tkinter.ttk import *
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk
from time import sleep
import threading
import tkinter as tk
from ThorlabsPM100 import ThorlabsPM100
import numpy as np
from Keithley6487Pro import Keithley6487Pro
import matplotlib.pyplot as plt

class childK6487(Keithley6487Pro):
    def __init__(self, root):
        Keithley6487Pro.__init__(self, root)
        self.stop_button.grid_remove()
        self.saveBut.grid(column=3, row=3, pady=20)
    def DESTRUCTION(self):
        self.help = 0
        self.instr.write(":SOUR:VOLT:STAT OFF")
        self.instr.close()
        self.root.destroy()
        self.root.update()


class isweepGUI:
    def __init__(self, master) -> None:
        
        self.master = master
        self.master.state('zoomed')
        self.master.configure(background='#f0f0f0')
        self.master.protocol('WM_DELETE_WINDOW', self.quit)
        self.instr = None
        self.isOn = None
        self.on = None
        self.off = None
        self.running = False
        self.pmAver = 1
        self.wl = 275
        self.master.title("Keithley 220 Current Sweep")

        self.fStyle = Style()
        self.fStyle.theme_use('alt')
        self.fStyle.configure(style='my.TFrame', background='#f0f0f0')
        self.frm = Frame(self.master, padding='1i', style='my.TFrame')
        self.frm.grid()

        #=====================================================HARRY STYLES===============================================================================================

        self.bStyle = Style()
        self.bStyle.theme_use('alt')
        self.bStyle.configure(style='my.TButton', font=('Helvetica', 15), background='#f0f0f0', foreground='black')

        self.bStyle = Style()
        self.bStyle.theme_use('alt')
        self.bStyle.configure(style='my.TButton', font=('Helvetica', 12), background='#f0f0f0', foreground='black')

        self.lStyle = Style()
        self.lStyle.theme_use('alt')
        self.lStyle.configure(style='my.TLabel', font=('Helvetica', 12), background='#f0f0f0', foreground='black')

        self.stylecb = Style()
        self.stylecb.theme_use('alt')
        self.stylecb.configure(style='my.TCheckbutton', font=('Helvetica', 12), background='#f0f0f0', foreground='black')

        #==================================================================KEITHLEY220======================================================================================

        self.rm = visa.ResourceManager()
        rList = self.rm.list_resources()
        print(rList)
        self.instr = self.rm.open_resource('GPIB0::12::INSTR')
        self.instr.write("F0X")

        self.vLim = 5
        self.instr.write(f"V{self.vLim}X")
        self.startCurrent = 10e-5
        self.stopCurrent = 1e-3
        self.stepCurrent = 100e-6

    
        #IMAGE
        self.onImage = Image.open("./AppsNshit/on.png")
        self.onIm = self.onImage.resize((50, 50))
        self.on = ImageTk.PhotoImage(self.onIm)
        self.offImage = Image.open("./AppsNshit/off.png")
        self.offIm = self.offImage.resize((50, 50))
        self.off = ImageTk.PhotoImage(self.offIm)

        #VLIM
        self.vLimLab = Label(self.frm, text="Voltage limit: ", style='my.TLabel')
        self.vLimLab.grid(column=0, row=1)
        self.vLimEn = Entry(self.frm)
        self.vLimEn.bind('<Return>', self.setVoltageLimit)
        self.vLimEn.grid(column=1, row=1)
        self.vLimBut = Button(self.frm, text="Ok", command=self.setVoltageLimit, style='my.TButton')
        self.vLimBut.grid(column=2, row=1)
        self.vLimLabel = Label(self.frm, text=f"{self.vLim} V", style='my.TLabel')
        self.vLimLabel.grid(column=3, row=1)

        #STARTI
        self.startILab = Label(self.frm, text="Start current: ", style='my.TLabel')
        self.startILab.grid(column=0, row=2)
        self.startIEn = Entry(self.frm)
        self.startIEn.grid(column=1, row=2)
        self.startIEn.bind('<Return>', self.setStartCurrent)
        self.startIBut = Button(self.frm, text="Ok", command=self.setStartCurrent, style='my.TButton')
        self.startIBut.grid(column=2, row=2)
        self.startILabel = Label(self.frm, text=f"- A", style='my.TLabel')
        self.startILabel.grid(column=3, row=2)

        #STOPI
        self.stopILab = Label(self.frm, text="Stop current: ", style='my.TLabel')
        self.stopILab.grid(column=0, row=3)
        self.stopIEn = Entry(self.frm)
        self.stopIEn.grid(column=1, row=3)
        self.stopIEn.bind('<Return>', self.setStopCurrent)
        self.stopIBut = Button(self.frm, text="Ok", command=self.setStopCurrent, style='my.TButton')
        self.stopIBut.grid(column=2, row=3)
        self.stopILabel = Label(self.frm, text=f"- A", style='my.TLabel')
        self.stopILabel.grid(column=3, row=3)

        #STEPI
        self.stepILab = Label(self.frm, text="Current step: ", style='my.TLabel')
        self.stepILab.grid(column=0, row=4)
        self.stepIEn = Entry(self.frm)
        self.stepIEn.grid(column=1, row=4)
        self.stepIEn.bind('<Return>', self.setStepCurrent)
        self.stepIBut = Button(self.frm, text="Ok", command=self.setStepCurrent, style='my.TButton')
        self.stepIBut.grid(column=2, row=4)
        self.stepILabel = Label(self.frm, text=f"- A", style='my.TLabel')
        self.stepILabel.grid(column=3, row=4)

        #LIGHT
        self.light = Label(self.frm)
        self.light.grid(column=0, row=5)
        if self.isOn is None:
            self.instr.write("F0X")
            self.light.config(image = self.off)
            self.isOn = False

        #DARKMODE
        self.darkmode = tk.IntVar(value=1)
        self.toggleDm()
        self.dmCheck = Checkbutton(self.frm, text='Darkmode', variable=self.darkmode, onvalue=1, offvalue=0, command=self.toggleDm, style='my.TCheckbutton')
        self.dmCheck.grid(column=0, row=6, pady=10)
        
        #RUN
        self.onOffBut = Button(self.frm, text="Run", command=self.runThread, style='my.TButton')
        self.onOffBut.grid(column=1, row=5)

        #loop
        self.var =  tk.IntVar(value=0)
        self.loopRadio = Radiobutton(self.frm, text='Loop', variable=self.var, value=1)
        self.loopRadio.grid(column=2, row=5)
        self.singleRadio = Radiobutton(self.frm, text='Single', variable=self.var, value=0)
        self.singleRadio.grid(column=3, row=5)

        #Stahp
        self.stahpBut = Button(self.frm, text='STAHP', command=self.stahp, style='my.TButton')
        self.stahpBut.grid(column=1, row=6)
        self.stahpBut.config(state='disabled')

        #QUIT
        self.destruction = Button(self.frm, text="Quit", command=self.quit, style='my.TButton')
        self.destruction.grid(column=1, row=7, padx=20, pady=20)

        #======================================================POWERMETER=========================================================================================

        self.pmBut = tk.Button(self.frm, text='Thorlabs PM101', relief='raised', command=self.toggle)
        self.pmBut.grid(column=5, row=2, padx=20)

        #PM AVERAGE
        self.tlLab = Label(self.frm, text='Averaging: ', style='my.TLabel')
        self.tlEn = Entry(self.frm)
        self.tlEn.bind('<Return>', self.pmAverage)
        self.tlLabel = Label(self.frm, text=f'{self.pmAver}', style='my.TLabel')

        #PM WAVELENGTH
        self.wlLab = Label(self.frm, text='Wavelength: ', style='my.TLabel')
        self.wlEn = Entry(self.frm)
        self.wlEn.bind('<Return>', self.pmWavelength)
        self.wlLabel= Label(self.frm, text=f'{self.wl} nm', style='my.TLabel')

        #PM angle
        self.angleLab = Label(self.frm, text='Angle: ', style='my.TLabel')
        self.angleEn = Entry(self.frm)
        self.angleEn.bind('<Return>', self.angle)
        self.angleLabel = Label(self.frm, text='-', style='my.TLabel')

        #SAVE DATA
        self.saveVar = tk.IntVar(value=0)
        self.saveCheck = Checkbutton(self.frm, text='Save', style='my.TCheckbutton', variable=self.saveVar, onvalue=1, offvalue=0)
        
        #==========================================KEITHLEY6487===================================================================================================

        self.k6487But = tk.Button(self.frm, text='Keithley6487 Pro', relief='raised', command=self.openKeithley6487)
        self.k6487But.grid(column=5, row=1)
        
    def toggle(self):
        if self.pmBut.config('relief')[-1] == 'sunken':
            self.pmBut.config(relief="raised")
            self.tlLab.grid_remove()
            self.tlEn.grid_remove()
            self.tlLabel.grid_remove()

            self.wlLab.grid_remove()
            self.wlEn.grid_remove()
            self.wlLabel.grid_remove()
            self.saveCheck.grid_remove()

            self.angleLab.grid_remove()
            self.angleEn.grid_remove()
            self.angleLabel.grid_remove()
            try:
                self.powermeter.system.beeper.immediate()
                self.powermeter.close()
            except:
                pass

        else:
            try:
                pm1 = self.rm.open_resource('USB0::0x1313::0x8076::M00904927::INSTR')
                self.powermeter = ThorlabsPM100(inst=pm1)
                self.powermeter.system.beeper.immediate()
                self.powermeter.sense.power.dc.range.auto = 'ON'
                self.powermeter.sense.average.count = self.pmAver
                self.powermeter.sense.correction.wavelength = self.wl

                self.pmBut.config(relief="sunken")
                self.tlLab.grid(column=6, row=2)
                self.tlEn.grid(column=7, row=2, padx=10)
                self.tlLabel.grid(column=8, row=2)

                self.wlLab.grid(column=6, row=1)
                self.wlEn.grid(column=7, row=1, padx=10)
                self.wlLabel.grid(column=8, row=1)

                self.angleLab.grid(column=6, row=3)
                self.angleEn.grid(column=7, row=3, padx=10)
                self.angleLabel.grid(column=8, row=3)

                self.saveCheck.grid(column=6, row=4)

            except Exception as e:
                print(e)

    def toggleDm(self):
        if self.darkmode.get() == 0:
            self.master.configure(background='#f0f0f0')

            self.fStyle.configure(style='my.TFrame', background='#f0f0f0')
            
            self.bStyle.configure(style='my.TButton', font=('Helvetica', 15), background='#f0f0f0', foreground='black')

            
            self.bStyle.configure(style='my.TButton', font=('Helvetica', 12), background='#f0f0f0', foreground='black')

            
            self.lStyle.configure(style='my.TLabel', font=('Helvetica', 12), background='#f0f0f0', foreground='black')

           
            self.stylecb.configure(style='my.TCheckbutton', font=('Helvetica', 12), background='#f0f0f0', foreground='black')
        else:
            self.master.configure(background='black')

            self.fStyle.configure(style='my.TFrame', background='black')

            self.bStyle.configure(style='my.TButton', font=('Helvetica', 15), background='black', foreground='red')

            
            self.bStyle.configure(style='my.TButton', font=('Helvetica', 12), background='black', foreground='red')

            
            self.lStyle.configure(style='my.TLabel', font=('Helvetica', 12), background='black', foreground='red')

           
            self.stylecb.configure(style='my.TCheckbutton', font=('Helvetica', 12), background='black', foreground='red')
    
    def angle(self, event=None):
        self.ang = int(self.angleEn.get())
        self.angleLabel.config(text=f'{self.ang} deg')
        self.angleEn.delete(0, 'end')


    def pmAverage(self, event=None):
        self.pmAver = int(self.tlEn.get())
        self.tlLabel.config(text=f'{self.pmAver}')
        self.tlEn.delete(0, 'end')
    
    def pmWavelength(self, event=None):
        self.wl = self.wlEn.get()
        self.powermeter.sense.correction.wavelength = int(self.wl)
        self.wlLabel.config(text=f'{self.wl} nm')
        self.wlEn.delete(0, 'end')

    def animate(self):
        if self.running:
            self.light.config(image=self.on)
            self.master.after(100, self.animate)
        else:
            self.light.config(image=self.off)
            self.onOffBut.config(state='normal')
            self.stahpBut.config(state='disabled')

    def quit(self):
        if self.running:
            self.running = False
            sleep(2)
        self.instr.close()
        self.master.quit()
    
    def runThread(self):
        if not self.running:
            self.running = True
            self.startILabel.config(text=f"{self.startCurrent} A")
            self.stopILabel.config(text=f"{self.stopCurrent} A")
            self.stepILabel.config(text=f"{self.stepCurrent} A")
            self.onOffBut.config(state='disabled')
            self.stahpBut.config(state='normal')
            threading.Thread(target=self.run).start()
            self.animate()

    def run(self):
        self.instr.write("R0X")
        self.instr.write("F0X")
        print(self.var.get())
        
        current = float(self.startCurrent)
        currentStep = float(self.stepCurrent)
        stopCurrent = float(self.stopCurrent)

        self.angleList = []
        self.currentList = []
        self.pmDataList = []
        self.pmStdList = []

        #IF POWERMETER
        if self.pmBut.config('relief')[-1] == 'sunken':

            #IF SINGLE SWEEP
            if self.var.get() == 0:
                while current <= stopCurrent:
                    if self.running:
                        self.instr.write(f"I{current}X")
                        self.instr.write("F1X")
                        
                        sleep(0.5)
                        
                        self.angleList.append(self.ang)

                        self.currentList.append(current)

                        measTemp = []
                        #for i in range(self.pmAver):
                        #    measTemp.append(self.powermeter.read)
                        #    sleep(0.01)
                        #measTemp = np.array(measTemp)
                        measTemp = np.array([self.powermeter.read for i in range(self.pmAver)])
                        meas = measTemp.mean()
                        std = measTemp.std()
                        print(current, meas)
                        self.pmDataList.append(meas)
                        self.pmStdList.append(std)
                        
                    else:
                        break

                    current = round(current + currentStep, 9)
                self.running = False
                self.instr.write("F0X")
                plt.scatter(self.currentList, self.pmDataList, s=10, c='mediumorchid')
                plt.tight_layout()
                plt.show()
                #print(f'{self.angleList}\n{self.currentList}\n{self.pmDataList}\n{self.pmStdList}')
                if self.saveVar.get():
                    self.save()

            #IF LOOPING SWEEP
            elif self.var.get() == 1:
                print(self.var)
                while True:
                    if current > stopCurrent:
                        current = self.startCurrent
                    if self.running:
                        self.instr.write(f"I{current}X")
                        self.instr.write("F1X")
                        print(current)
                        sleep(1)
                    else:
                        break
                    current = round(current + currentStep, 9)
                self.running = False
                self.instr.write("F0X")

        #NO POWERMETER
        else:

            #IF SINGLE SWEEP
            if self.var.get() == 0:
                while current <= stopCurrent:
                    if self.running:
                        self.instr.write(f"I{current}X")
                        self.instr.write("F1X")
                        print(current)
                        sleep(1)
                    else:
                        break

                    current = round(current + currentStep, 9)
                self.running = False
                self.instr.write("F0X")

            #IF LOOPING SWEEP
            elif self.var.get() == 1:
                print(self.var)
                while True:
                    if current > stopCurrent:
                        current = self.startCurrent
                    if self.running:
                        self.instr.write(f"I{current}X")
                        self.instr.write("F1X")
                        print(current)
                        sleep(1)
                    else:
                        break
                    current = round(current + currentStep, 9)
                self.running = False
                self.instr.write("F0X")
        
    def stahp(self):
        self.running = False

    def setVoltageLimit(self, event=None):
        """Sets voltage limit in V"""
        self.vLim = float(self.vLimEn.get())
        self.vLimLabel.config(text=f"{self.vLim} V")
        self.vLimEn.delete(0, 'end')
        self.instr.write(f"V{self.vLim}X")
    
    def setStartCurrent(self, event=None):
        """Sets start current in A"""
        self.startCurrent = float(self.startIEn.get())
        self.startILabel.config(text=f"{self.startCurrent} A")
        self.startIEn.delete(0, 'end')

    def setStopCurrent(self, event=None):
        """Sets stop current in A"""
        self.stopCurrent = float(self.stopIEn.get())
        self.stopILabel.config(text=f"{self.stopCurrent} A")
        self.stopIEn.delete(0, 'end')
    
    def setStepCurrent(self, event=None):
        self.stepCurrent = float(self.stepIEn.get())
        self.stepILabel.config(text=f"{self.stepCurrent} A")
        self.stepIEn.delete(0, 'end')

    def openKeithley6487(self):
        if self.k6487But.config('relief')[-1] == 'raised':
            try:
                self.k6487But.config(relief='sunken')
                window = tk.Toplevel()
                self.child = childK6487(window)
            except Exception as e:
                window.destroy()
                self.k6487But.config(relief='raised')
                print(e)
        else:
            self.k6487But.config(relief='raised')
            self.child.DESTRUCTION()

    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as file:
                file.write('Angle / deg, Current / A, Power / W, Standard deviation of power / W')
                for i in range(len(self.currentList)):
                    file.write(f'\n{self.angleList[i]}, {self.currentList[i]}, {self.pmDataList[i]}, {self.pmStdList[i]}')
        self.angleList.clear()
        self.currentList.clear()
        self.pmDataList.clear()
        self.pmStdList.clear()

def main():
    root = Tk()
    isweepGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()