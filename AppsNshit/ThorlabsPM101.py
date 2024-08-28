import pyvisa as visa
from tkinter import Tk
from tkinter.ttk import *
from tkinter import simpledialog, filedialog
import tkinter as tk
from ThorlabsPM100 import ThorlabsPM100
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from time import time, sleep

class thorlabsGUI:
    def __init__(self, master):
        self.master = master
        #self.master.attributes('-fullscreen', True)
        self.master.title('Thorlabs PM101')
        self.master.configure(background='black')
        self.master.state('zoomed')
        self.master.protocol('WM_DELETE_WINDOW', self.DESTRUCTION)
        self.pmAver = 1
        self.wl = 450
        self.running = False
        self.xAxisLen = 20
        self.darkmode = Style()
        self.darkmode.theme_use('alt')
        self.darkmode.configure(style='my.TFrame', background='black')
        self.rgb = False
        self.timeStart = None
        self.timeIdle = 0
        self.firstRun = 0
        self.currentList = []
        self.angleList = []
        self.angle = '-'
        self.measList = []
        self.stdList = []
        self.laser = '-'
        self.autoLaser = False

        self.frm = Frame(self.master, padding='1i', style='my.TFrame')
        self.frm.grid(column=0, row=0)

        self.rm = visa.ResourceManager()
        self.rList = self.rm.list_resources()

        #=========================================HARRY STYLES===========================================

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

        try:
            self.pm1 = self.rm.open_resource('USB0::0x1313::0x8076::M00904927::INSTR')
            self.powermeter = ThorlabsPM100(inst=self.pm1)

            #PM WAVELENGTH
            self.wlLab = Label(self.frm, text='Wavelength: ', style='my.TLabel')
            self.wlLab.grid(column=0, row=1, padx=10, pady=10)
            self.wlEn = Entry(self.frm)
            self.wlEn.grid(column=1, row=1, padx=10, pady=10)
            self.wlEn.bind('<Return>', self.pmWavelength)
            self.wlLabel= Label(self.frm, text=f'{self.wl} nm', style='my.TLabel')
            self.wlLabel.grid(column=2, row=1, padx=10, pady=10)

            #RUN
            self.runBut = Button(self.frm, text="Run", command=self.run, style='my.TButton')
            self.runBut.grid(column=1, row=2)

            #PAUSE
            self.pauseBut = Button(self.frm, text="Pause", command=self.pause, style='my.TButton')
            self.pauseBut.grid(column=1, row=3)

            #CLEAR
            self.clearBut = Button(self.frm, text="Clear", command=self.clear, style='my.TButton')
            self.clearBut.grid(column=1, row=4)

            #CLOSE PROGRAM
            self.stop_button = Button(self.frm, text="Close program", command=self.DESTRUCTION, style='my.TButton')
            self.stop_button.grid(column=1, row=100, padx=20, pady=20)

            #SHOW?
            self.showVar = tk.IntVar(value=1)
            self.showAll = Checkbutton(self.frm, text='Show all', variable=self.showVar, onvalue=1, offvalue=0, command=self.toggle, style='my.TCheckbutton')
            self.showAll.grid(column=1, row=5, padx=10, pady=10)

            #MEASURE check
            self.measVar = tk.IntVar(value=0)
            self.measCheck = Checkbutton(self.frm, text='Measurement', variable=self.measVar, onvalue=1, offvalue=0, style='my.TCheckbutton', command=self.toggle2)
            self.measCheck.grid(column=1, row=7, padx=10, pady=10)

            #PM AVERAGE
            self.averLab = Label(self.frm, text='Averaging: ', style='my.TLabel')
            self.averEn = Entry(self.frm, background='dimgrey', style='my.TEntry')
            self.averEn.bind('<Return>', self.pmAverage)
            self.averLabel = Label(self.frm, text=f'{self.pmAver}', style='my.TLabel')

            #Laser current
            self.laserLab = Label(self.frm, text='Laser current: ', style='my.TLabel')
            self.laserEn = Entry(self.frm, background='dimgrey', style='my.TEntry')
            self.laserEn.bind('<Return>', self.laserI)
            self.laserLabel = Label(self.frm, text=f'{self.laser} mA', style='my.TLabel')

            #Angle
            self.angleLab = Label(self.frm, text='Angle: ', style='my.TLabel')# HERE NEW ======================
            self.angleEn = Entry(self.frm, background='dimgrey', style='my.TEntry')
            self.angleEn.bind('<Return>', self.setAngle)
            self.angleLabel = Label(self.frm, text=f'{self.angle} deg', style='my.TLabel')

            #MEASURE
            self.measBut = Button(self.frm, text='Measure', style='my.TButton', command=self.measure)

            #MEASUREMENT LABEL
            self.measLabel = Label(self.frm, text='Measurement: -', style='my.TLabel')

            #DISCARD
            self.discBut = Button(self.frm, text='Discard', style='my.TButton', command=self.discard)
            if len(self.measList) == 0:
                self.discBut.configure(state='disabled')

            #SAVE
            self.saveBut = Button(self.frm, text='Save', command=self.save, style='my.TButton')

            #NUMBERS YES
            self.secondsLab = Label(self.frm, text='Show seconds', style='my.TLabel')
            self.secondsEn = Entry(self.frm)
            self.secondsEn.bind('<Return>', self.setSeconds)
            self.secondsLabel = Label(self.frm, text=f'{self.xAxisLen} s', style='my.TLabel')

            #CONTINUOUS
            self.fig, self.ax = plt.subplots()
            self.ax.set_facecolor('black')
            self.fig.set_facecolor('black')
            self.ax.spines['bottom'].set_color('maroon')
            self.ax.spines['top'].set_color('maroon') 
            self.ax.spines['right'].set_color('maroon')
            self.ax.spines['left'].set_color('maroon')
            self.ax.tick_params(axis='x', colors='red')
            self.ax.tick_params(axis='y', colors='red')
            self.ax.yaxis.label.set_color('red')
            self.ax.xaxis.label.set_color('red')
            self.fig.set_figheight((12 / 16 * 9))
            self.fig.set_figwidth(12)
            self.sc = self.ax.scatter([], [])
            self.ax.set_ylabel("Power / W")
            self.ax.set_xlabel('Time / s')
            
            self.xdata, self.ydata = [], []
            
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
            self.canvas.get_tk_widget().config(bg='midnightblue')
            self.canvas.draw()
            self.canvas.get_tk_widget().grid(column=1, row=0)

            #self.toolbar = NavigationToolbar2Tk(self.canvas, window=self.master)
            #self.toolbar.update()
            #self.canvas.get_tk_widget().grid(column=1, row=1)

            #ANIMATION
            self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=10, blit=True, cache_frame_data=False)

        except Exception as e:
            print(e)
            self.errorLab = Label(self.frm, text='No device').grid(column=0, row=0)
            self.close = Button(self.frm, text='Close', command=self.master.quit).grid(column=0, row=1)
    
    def toggle(self):
        if self.showVar.get() == 0:
                self.secondsLab.grid(column=0, row=6)
                self.secondsEn.grid(column=1, row=6)
                self.secondsLabel.grid(column=2, row=6)
        else:
            self.secondsLab.grid_remove()
            self.secondsEn.grid_remove()
            self.secondsLabel.grid_remove()
    
    def toggle2(self):
        if self.measVar.get() == 0:
            self.laserLab.grid_remove()
            self.laserEn.grid_remove()
            self.laserLabel.grid_remove()

            self.averLab.grid_remove()
            self.averEn.grid_remove()
            self.averLabel.grid_remove()
            self.measBut.grid_remove()
            self.saveBut.grid_remove()

            self.angleLab.grid_remove()
            self.angleEn.grid_remove()
            self.angleLabel.grid_remove()

            self.discBut.grid_remove()

            self.measLabel.grid_remove()
        else:
            self.laserLab.grid(column=0, row=8, pady=10)
            self.laserEn.grid(column=1, row=8, pady=10)
            self.laserLabel.grid(column=2, row=8, pady=10)

            self.averLab.grid(column=0, row=9, pady=10)
            self.averEn.grid(column=1, row=9, pady=10)
            self.averLabel.grid(column=2, row=9, pady=10)

            self.angleLab.grid(column=0, row=10, pady=10)#HERE NEW ===============
            self.angleEn.grid(column=1, row=10, pady=10)
            self.angleLabel.grid(column=2, row=10, pady=10)

            self.measBut.grid(column=1, row=11)
            self.saveBut.grid(column=1, row=13)

            self.discBut.grid(column=1, row=12)

            self.measLabel.grid(column=1, row=14, pady=10)
    
    def setAngle(self, event=None):# HERE NEW ==============================
        self.angle = int(self.angleEn.get())
        self.angleEn.delete(0, 'end')
        self.angleLabel.config(text=f'{self.angle} deg')
    
    def setSeconds(self, event=None):
        self.xAxisLen = float(self.secondsEn.get())
        self.secondsEn.delete(0, 'end')
        self.secondsLabel.config(text=f'{self.xAxisLen} s')

    def pmAverage(self, event=None):
        self.pmAver = int(self.averEn.get())
        self.averLabel.config(text=f'{self.pmAver}')
        self.averEn.delete(0, 'end')
    
    def pmWavelength(self, event=None):
        self.wl = self.wlEn.get()
        self.powermeter.sense.correction.wavelength = int(self.wl)
        self.wlLabel.config(text=f'{self.wl} nm')
        self.wlEn.delete(0, 'end')
    
    def DESTRUCTION(self):
        self.running = False
        sleep(0.5)
        self.pm1.close()
        sleep(0.5)
        self.master.quit()
    
    def update_plot(self, frame):
        if self.running:
            if self.rgb:
                if self.animiter == 0 or self.animiter % 10 == 0:
                    self.instr.write(":INIT") #TRIGGER MEASUREMENT
                    self.instr.write(":SENS:DATA?") # data plz UwU
                    self.animiter += 1
                    self.xdata.append(len(self.xdata))
                    ydat = float(self.instr.read())
                    self.ydata.append(ydat)

                    if len(self.ydata) % 200 == 0:
                        self.col1 = self.col1 + self.col1
            
                    list(self.ax.collections).clear()
                    self.currentLab.config(text=f'{ydat:.3e} A')
                    self.col1 = self.col1[1:] + self.col1[:1]
                    #for i, color in zip(range(len(self.ydata)), self.colors):
                    self.sc = self.ax.scatter(self.xdata, self.ydata, color=self.col1[:len(self.ydata)])
                else:
                    self.animiter += 1
                    list(self.ax.collections).clear()
                    self.col1 = self.col1[1:] + self.col1[:1]
                    #for i, color in zip(range(len(self.ydata)), self.colors):
                    self.sc = self.ax.scatter(self.xdata, self.ydata, color=self.col1[:len(self.ydata)])
                self.canvas.draw()
            else:
                self.xdata.append(time() - self.timeStart - self.timeIdle)
                ydat = float(self.powermeter.read)
                self.ydata.append(ydat)
                if self.showVar.get() == 0:
                    if self.xdata[-1] > self.xAxisLen:
                        self.ax.clear()
                        self.ax.set_ylabel("Power / W")
                        self.ax.set_xlabel("Time / s")
                        self.ax.yaxis.label.set_color('red')
                        self.ax.xaxis.label.set_color('red')
                        self.ax.tick_params(axis='x', colors='red')
                        self.ax.tick_params(axis='y', colors='red')
                        list(self.ax.collections).clear()
                        self.sc = self.ax.scatter(self.xdata[self.getIndex():], self.ydata[self.getIndex():], color='red')
                        self.canvas.draw()
                    else:
                        list(self.ax.collections).clear()
                        self.sc = self.ax.scatter(self.xdata, self.ydata, color='red')
                        self.canvas.draw()
                else:
                    list(self.ax.collections).clear()
                    self.sc = self.ax.scatter(self.xdata, self.ydata, color='red')
                    self.canvas.draw()

        return self.sc,

    def getIndex(self):
        return self.xdata.index(min(self.xdata, key=lambda x:abs(x - (self.xdata[-1] - self.xAxisLen))))

    def run(self):
        self.running = True
        if self.firstRun == 0:
            self.timeStart = time()
            self.firstRun += 1
        else:
            self.timeIdle += time()- self.timePaused
  
    def pause(self):
        self.running = False
        self.timePaused = time()

    def laserI(self, event=None):
        self.autoLaser = False
        self.laser = float(self.laserEn.get()) * 1e-3
        self.laserLabel.config(text=f'{self.laser * 1e3} mA')
        self.laserEn.delete(0, 'end')

    def measure(self):
        if self.laser == '-':
            self.autoLaser = True
        self.measBut.config(state='disabled')
        measTemp = np.array([self.powermeter.read for i in range(self.pmAver)])
        meas = measTemp.mean()
        std = measTemp.std()
        if self.autoLaser:
            self.currentList = [0, 5e-3, 15e-3, 30e-3]
        else:
            self.currentList.append(self.laser)
        self.angleList.append(self.angle)
        self.measList.append(meas)
        self.stdList.append(std)
        self.measBut.config(state='normal')
        if len(self.measList) != 0:
            self.discBut.configure(state='normal')
        self.measLabel.config(text=f'Angle: {self.angle} deg\nCurrent: {self.laser} A\nPower: {meas:.3e} W\nStd: {std:.3e} W')

    def clear(self):
        self.xdata = []
        self.ydata = []
        self.ax.clear()
        self.ax.set_ylabel("Power / W")
        self.ax.set_xlabel('Time / s')
        self.ax.yaxis.label.set_color('red')
        self.ax.xaxis.label.set_color('red')
        self.ax.tick_params(axis='x', colors='red')
        self.ax.tick_params(axis='y', colors='red')
        self.sc = self.ax.scatter(self.xdata, self.ydata, color='red')
        if self.running:
            self.timeStart = time()
            self.timeIdle = 0
        else:
            self.firstRun = 0
            self.timeIdle = 0
        self.canvas.draw()
        return self.sc, 

    def discard(self):
        self.angleList = []
        self.currentList = []
        self.measList = []
        self.stdList = []
        self.discBut.configure(state='disabled')
        self.measLabel.config(text='Measurement: -')
 
    def save(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if filename:
            with open(filename, 'w') as file:
                file.write('Angle / deg, Laser current / A, Power / W, Standard deviation of power / W')
                for i in range(len(self.measList)):
                    file.write(f'\n{self.angleList[i]}, {self.currentList[i]}, {self.measList[i]}, {self.stdList[i]}')
            self.angleList = []
            self.currentList = []
            self.measList = []
            self.stdList = []

def main():
    root = Tk()
    thorlabsGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()