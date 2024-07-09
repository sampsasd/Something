import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random
import tkinter.ttk as ttk
import pyvisa as visa
from time import sleep, time


class voltageSweepApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keithley6487 Voltage Sweep")
        self.styleb = Style()
        self.styleb.configure(style='my.TButton', font=('Helvetica', 12))
        self.stylel = Style()
        self.stylel.configure(style='my.TLabel', font=('Helvetica', 12))
        self.running = False
        self.time1 = 0
        self.time2 = None
        
        # VISA CONNECTIONS
        self.rm = visa.ResourceManager()
        self.instr = self.rm.open_resource("GPIB0::22::INSTR")
        #RUN THESE AFTER START OR GET FUCKED
        self.instr.write("*RST")  #Return 6487 to GPIB defaults, USE BEFORE DISCONNECTING SIGNALS
        self.instr.write("SYST:ZCH OFF")
        self.instr.write(":SENS:RANG 0.001")

        #===============================================FIGURE===================================================================================================

        self.fig, self.ax = plt.subplots()
        self.sc = self.ax.scatter([], [])
        #self.line, = self.ax.scatter([], [])
        
        #self.ax.set_xlim(-0.001, 0.001)
        #self.ax.set_ylim(-0.001, 0.001)
        self.xdata, self.ydata = [], []
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid()
        
        #===========================================OPERATING BUTTONS============================================================================================================

        self.button_frame = Frame(self.root)
        self.button_frame.grid()

        #SAVE
        self.saveBut = Button(self.button_frame, text="Save", command=self.save, style='my.TButton')
        self.saveBut.grid(column=5, row=2)

        #CLOSE PROGRAM
        self.stop_button = Button(self.button_frame, text="Close program", command=self.DESTRUCTION, style='my.TButton')
        self.stop_button.grid(column=5, row=3)

        #NEEDS COMMAND measurement ranges n stuff
        #self.settingsBut = Button(self.button_frame, text="Settings", style='my.TButton')
        #self.settingsBut.grid(column=0, row=0)

        #RUN
        self.runBut = Button(self.button_frame, text="Run", command=self.run, style='my.TButton')
        self.runBut.grid(column=5, row=0)

        #PAUSE
        self.pauseBut = Button(self.button_frame, text="Pause", command=self.pause, style='my.TButton')
        self.pauseBut.grid(column=5, row=1)

        #CLEAR
        self.clearBut = Button(self.button_frame, text="Clear", command=self.clear, style='my.TButton')
        self.clearBut.grid(column=5, row=2)
        
        #=========================================VOLTAGE PROGRAM================================================================================================================

        self.setVlabel = ttk.Label(self.button_frame, text="Set voltage", style='my.TLabel')
        self.setVlabel.grid(column=10, row=0)
        self.setVentry = ttk.Entry(self.button_frame)
        self.setVentry.grid(column=11, row=0)
        self.setVBut = Button(self.button_frame, text="Ok", command=self.setVoltage, style='my.TButton')
        self.setVBut.grid(column=12, row=0)

        #=========================================VOLTAGE SWEEP==================================================================================================================

        #NEEDS COMMAND
        self.startVlabel = ttk.Label(self.button_frame, text="Start voltage", style='my.TLabel')
        self.startVlabel.grid(column=0, row=0)
        self.startVentry = ttk.Entry(self.button_frame)
        self.startVentry.grid(column=1, row=0)
        self.startVoltageBut = Button(self.button_frame, text="Ok", command=self.startVoltage)
        self.startVoltageBut.grid(column=2, row=0)
        self.startVlab = ttk.Label(self.button_frame, text='No voltage')
        self.startVlab.grid(column=3, row=0)


        #NEEDS COMMAND
        self.stopVlabel = ttk.Label(self.button_frame, text="Stop voltage", style='my.TLabel')
        self.stopVlabel.grid(column=0, row=1)
        self.stopVentry = ttk.Entry(self.button_frame)
        self.stopVentry.grid(column=1, row=1)
        self.stopVoltageBut = Button(self.button_frame, text="Ok", command=self.stopVoltage)
        self.stopVoltageBut.grid(column=2, row=1)
        self.stopVlab = ttk.Label(self.button_frame, text='No voltage')
        self.stopVlab.grid(column=3, row=1)

        #NEEDS COMMAND
        self.stepVlabel = ttk.Label(self.button_frame, text="Voltage step", style='my.TLabel')
        self.stepVlabel.grid(column=0, row=2)
        self.stepVentry = ttk.Entry(self.button_frame)
        self.stepVentry.grid(column=1, row=2)
        self.stepVoltageBut = Button(self.button_frame, text="Ok", command=self.voltageStep)
        self.stepVoltageBut.grid(column=2, row=2)
        self.stepVlab = ttk.Label(self.button_frame, text='No step')
        self.stepVlab.grid(column=3, row=2)

        #NEEDS COMMAND
        self.averagelabel = ttk.Label(self.button_frame, text="Average points", style='my.TLabel')
        self.averagelabel.grid(column=0, row=3)
        self.averageentry = ttk.Entry(self.button_frame)
        self.averageentry.grid(column=1, row=3)
        self.averageBut = Button(self.button_frame, text="Ok", command=self.averagePoints)
        self.averageBut.grid(column=2, row=3)
        self.averagelab = ttk.Label(self.button_frame, text='No average')
        self.averagelab.grid(column=3, row=3)

        
        
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000, blit=True)
    
    def setVoltage(self):
        volt = self.setVentry.get()
        self.instr.write(f":SOUR:VOLT {volt}")
        sleep(2)

    def pause(self):
        self.time2 = time()
        self.instr.write(":SOUR:VOLT:STAT OFF")
        self.running = False
        
    def run(self):
        self.instr.write(":FORM:ELEM READ") #CURRENT/RESISTANCE, TIME FROM SWITCH ON, STATUS (idk), SOURCE VOLTAGE
        self.instr.write(":FORM:DATA ASCii") #CHOOSE DATA FORMAT
        self.instr.write(":SOUR:VOLT:STAT ON")
        self.instr.write(":SOUR:VOLT:RANG " + str(50))  # Set voltage range
        self.instr.write(":SOUR:VOLT:ILIM " + str(0.001)) # Set the maximum current limit
        self.instr.write(":SENS:RANG 0.001")
        if self.time2 is None:
            self.time1 = time()
        else:
            self.time1 = self.time2
        self.running = True

    def update_plot(self, frame):
        if self.running:
            self.instr.write(":INIT") #TRIGGER MEASUREMENT
            self.instr.write(":SENS:DATA?") # data plz UwU

            self.xdata.append(len(self.xdata))
            ydat = float(self.instr.read())
            self.ydata.append(ydat)
            
            self.ax.collections.clear()
            self.sc = self.ax.scatter(self.xdata, self.ydata, c='blue')

            self.canvas.draw()
        return self.sc,

    def startVoltage(self):
        """Sets start voltage in V"""
        self.startV = self.startVentry.get()
        self.startVlab.config(text=f"{self.startV} V")
        self.startVentry.delete(0, 'end')

    def stopVoltage(self):
        """Sets stop voltage in V"""
        self.stopV = self.stopVentry.get()
        self.stopVlab.config(text=f"{self.stopV} V")
        self.stopVentry.delete(0, 'end')

    def voltageStep(self):
        """Sets voltage step in V"""
        self.stepV = self.stepVentry.get()
        self.stepVlab.config(text=f"{self.stepV} V")
        self.stepVentry.delete(0, 'end')

    def averagePoints(self):
        """Sets number of averaging points"""
        self.average = self.averageentry.get()
        self.averagelab.config(text=f"Averaging {self.average} points")
        self.averageentry.delete(0, 'end')
    
    def save(self):
        self.running = False
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            self.fig.savefig(filename)
    
    def DESTRUCTION(self):
        self.instr.write(":SOUR:VOLT:STAT OFF")
        self.instr.close()
        self.root.quit()

    def clear(self):
        self.xdata = []
        self.ydata = []

if __name__ == "__main__":
    root = tk.Tk()
    app = voltageSweepApp(root)
    root.mainloop()
