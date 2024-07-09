import pyvisa as visa
from tkinter import Tk
from tkinter.ttk import *
from tkinter import simpledialog
from PIL import Image, ImageTk

class GUI:
    def __init__(self, master) -> None:
        self.style = Style()
        self.style.configure(style='my.TButton', font=('Helvetica', 15))
        self.master = master
        self.instr = None
        self.isOn = None
        self.on = None
        self.off = None
        self.master.title("Keithley 220 Current Source")

        self.frm = Frame(self.master, padding='1i')
        self.frm.grid()

        
        self.conBut = Button(self.frm, text="Connect", command=self.connect, style='my.TButton')
        self.conBut.grid(column=0, row=0)

        self.destruction = Button(self.frm, text="Quit", command=self.master.destroy, style='my.TButton')
        self.destruction.grid(column=0, row=1)
        
    
    def secondPage(self):

        self.master.destroy()

        self.master = Tk()
        self.master.title("Keithley 220 Current Source")
        self.frm = Frame(self.master, padding='0.5i')
        self.frm.grid()

        self.vLim = 1
        self.current = 1e-6

        self.onImage = Image.open("./AppsNshit/on.png")
        self.onIm = self.onImage.resize((50, 50))
        self.on = ImageTk.PhotoImage(self.onIm)
        self.offImage = Image.open("./AppsNshit/off.png")
        self.offIm = self.offImage.resize((50, 50))
        self.off = ImageTk.PhotoImage(self.offIm)

        self.style = Style()
        self.style.configure(style='my.TButton', font=('Helvetica', 12))
        self.stylel = Style()
        self.style.configure(style='my.TLabel', font=('Helvetica', 12))

        self.vLimLab = Label(self.frm, text="Set voltage limit: ", style='my.TLabel')
        self.vLimLab.grid(column=0, row=0)
        self.vLimEn = Entry(self.frm)
        self.vLimEn.grid(column=1, row=0)
        self.vLimBut = Button(self.frm, text="Ok", command=self.setVoltageLimit, style='my.TButton')
        self.vLimBut.grid(column=2, row=0)
        self.vLimLabel = Label(self.frm, text=f"{self.vLim} V", style='my.TLabel')
        self.vLimLabel.grid(column=3, row=0)

        self.currLab = Label(self.frm, text="Set current: ", style='my.TLabel')
        self.currLab.grid(column=0, row=1)
        self.currEn = Entry(self.frm)
        self.currEn.grid(column=1, row=1)
        self.currBut = Button(self.frm, text="Ok", command=self.setCurrent, style='my.TButton')
        self.currBut.grid(column=2, row=1)
        self.currLabel = Label(self.frm, text=f"{self.current} A", style='my.TLabel')
        self.currLabel.grid(column=3, row=1)

        self.light = Label(self.frm)
        self.light.grid(column=0, row=4)
        if self.isOn is None:
            self.instr.write("F0X")
            self.light.config(image = self.off)
            self.isOn = False
        
        self.onOffBut = Button(self.frm, text="Output On/Off", command=self.onOff, style='my.TButton')
        self.onOffBut.grid(column=1, row=4)

        self.destruction = Button(self.frm, text="Quit", command=quit, style='my.TButton')
        self.destruction.grid(column=1, row=6)

        
        


    def quit(self):
        self.instr.close()
        self.master.destroy()
    
    def onOff(self):
        if self.isOn:
            self.instr.write("F0X")
            self.light.config(image = self.off)
            self.isOn = False
        else:
            self.instr.write("F1X")
            self.light.config(image = self.on)
            self.isOn = True

    def setVoltageLimit(self):
        """Sets voltage limit in V"""
        self.vLim = self.vLimEn.get()
        self.vLimLabel.config(text=f"{self.vLim} V")
        self.vLimEn.delete(0, 'end')
        self.instr.write(f"V{self.vLim}X")
    
    def setCurrent(self):
        """Sets current in A"""
        self.instr.write("R0X")
        self.current = self.currEn.get()
        self.currLabel.config(text=f"{self.current} A")
        self.currEn.delete(0, 'end')
        self.instr.write(f"I{self.current}X")
    
    def setMeasRange(self):
        """Sets measurement range"""

        coolDict = {
            "Auto": "R0X",
            "1 nA": "R1X",
            "10 nA": "R2X",
            "100 nA": "R3X",
            "1 uA": "R4X",
            "10 uA": "R5X",
            "100 uA": "R6X",
            "1 mA": "R7X",
            "10 mA": "R8X",
            "100 mA": "R9X"
        }

        window = Tk()
        window.title("Set measurement range")

        def rang(self, window, rang: str):
            self.instr.write(coolDict[rang])
            window.destroy()

        
        for key in coolDict:
            Button(window, text=key, command=lambda: rang(self, window, key)).pack()
            
    
    def connect(self):
        rm = visa.ResourceManager()
        rList = rm.list_resources()
        #try:
        self.instr = rm.open_resource('GPIB0::12::INSTR')
        self.instr.write("F0X")
        self.secondPage()
        #except Exception as E:
        #    ip = simpledialog.askstring(title="Wrong resource", prompt=str(rList) + "\nWrong resource, type new resource")
        #    self.instr = rm.open_resource(str(ip))

def main():
    root = Tk()
    GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()