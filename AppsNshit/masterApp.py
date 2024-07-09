from tkinter import Tk
from tkinter.ttk import *
from KeithleyCurrSour import GUI as GUI220


class masterGUI():
    def __init__(self, root: Tk) -> None:
        style = Style()
        style.configure(style='my.TButton', font=('Helvetica', 15))
        self.root = root
        self.frm = Frame(self.root, padding=50)
        self.frm.grid(columnspan=10, rowspan=10)
        self.root.title("Master App")

        but220 = Button(self.frm, text="Keithley 220 Current Source", style='my.TButton', command=keithley220)
        but220.grid(column=0, row=1)

        but6487 = Button(self.frm, text="Keithley 6487 Voltage Source", style='my.TButton')
        but6487.grid(column=0, row=2)
        Label(self.frm, text="Not usable yet").grid(column=1, row=2)

        butOsc = Button(self.frm, text="Keysight DSOX1102G oscilloscope", style='my.TButton')
        butOsc.grid(column=0, row=3)
        Label(self.frm, text="Not usable yet").grid(column=1, row=3)

        butKill = Button(self.frm, text="Quit", command=self.root.destroy, style='my.TButton')
        butKill.grid(column=0, row=10)

def keithley220():
    root220 = Tk()
    GUI220(root220)
    root220.mainloop()

def main():
    root = Tk()
    masterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()