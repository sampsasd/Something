import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from tkinter.ttk import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class coatingPlotter:
    def __init__(self, master) -> None:
        self.master = master
        self.master.title('Coating Plotter')
        self.time = None
        self.temperature = None
        self.freq = None
        self.deltaF = None
        self.finalDeltaF = None
        self.sDens = None
        self.title = None

        self.infoFrm = Frame(self.master)
        self.infoFrm.grid(column=0, row=0, padx=10, pady=10)

        self.frm = Frame(self.master)
        self.frm.grid(column=0, row=1, padx=10, pady=10)

        self.butStyle = Style()
        self.butStyle.configure(style='my.TButton', font=('Helvetica', 15))
        
        self.labStyle = Style()
        self.labStyle.configure(style='my.TLabel', font=('Helvetica', 15))

    #============================BUTTONS=====================================================================

        self.closeBut = Button(self.frm, text='Close', command=self.master.quit, style='my.TButton')
        self.closeBut.grid(column=1, row=100, padx=20, pady=20)

        self.fileBut = Button(self.frm, text='Select file', command=self.readDatData, style='my.TButton')
        self.fileBut.grid(column=1, row=0, padx=10, pady=10)

        self.titleLab = Label(self.frm, text='Image title:', style='my.TLabel')
        self.titleLab.grid(column=0, row=1, padx=10, pady=10)
        self.titleEn = Entry(self.frm)
        self.titleEn.bind('<Return>', self.setTitle)
        self.titleEn.grid(column=1, row=1)
        self.titleLabel = Label(self.frm, text='-', style='my.TLabel')
        self.titleLabel.grid(column=2, row=1, padx=10, pady=10)

        self.plotBut = Button(self.frm, text='Plot', command=self.plotCoating, style='my.TButton')
        self.plotBut.configure(state='disabled')
        self.plotBut.grid(column=1, row=2, padx=10, pady=10)

        self.clearBut = Button(self.frm, text='Clear', command=self.clear, style='my.TButton')
        self.clearBut.configure(state='disabled')
        self.clearBut.grid(column=1, row=3, padx=10, pady=10)

        #================INFO=================

        self.fileLab = Label(self.infoFrm, text='File name: -', style='my.TLabel')
        self.fileLab.grid(column=0, row=0, padx=10, pady=10)

        self.finalFLab = Label(self.infoFrm, text='Final DeltaF: - Hz', style='my.TLabel')
        self.finalFLab.grid(column=0, row=1, padx=10, pady=10)

        self.sDensLab = Label(self.infoFrm, text='Surface density: - g/cm^2', style='my.TLabel')
        self.sDensLab.grid(column=0, row=2, padx=10, pady=10)
    
    #========================================================FUNC====================================================

    def clear(self):
        self.time = None
        self.temperature = None
        self.freq = None
        self.deltaF = None
        self.finalDeltaF = None
        self.title = None
        self.finalFLab.config(text='Final DeltaF: - Hz')
        self.sDensLab.config(text='Surface density: - g/cm^2')
        self.titleLabel.config(text='-')
        self.fileLab.config(text='File name: -')
        self.clearBut.configure(state='disabled')
        self.plotBut.configure(state='disabled')
        self.fileBut.configure(state='normal')

    def setTitle(self, event=None):
        self.title = self.titleEn.get()
        self.titleLabel.config(text=self.title)
        #self.titleEn.delete(0, 'end')

    def readDatData(self):
        """Returns (time, temperature, frequency)"""
        freq = []
        temp = []
        time = []
        fileName = askopenfilename(initialdir='.', filetypes=(('dat files', 'dat'), ))
        try:
            with open(fileName, 'r') as file:
                for row in file:
                    rawRow = row.strip().split()
                    freq.append(float(rawRow[3]))
                    if not time:
                        t_i = float(rawRow[2])
                        time.append(0.)
                    else:
                        tMin = (float(rawRow[2]) - t_i) / 60
                        time.append(tMin)
                    temp.append(float(rawRow[5]))
                
            self.time = np.array(time)
            self.temperature = np.array(temp)
            self.freq = np.array(freq)

            f_i = np.amax(self.freq)
            self.deltaF = [(point - f_i)*1E-3 for point in self.freq]
            if len(self.freq) % 2 == 0:
                self.finalDeltaF = f_i - np.amin(np.split(self.freq, 2)[1])
            else:
                self.freq2 = np.delete(self.freq, 0)
                self.finalDeltaF = f_i - np.amin(np.split(self.freq2, 2)[1])
            self.sDens = self.finalDeltaF * 17.7e-9
            
            self.clearBut.configure(state='normal')
            self.plotBut.configure(state='normal')

            self.fileLab.config(text=f'File name: {fileName[-10:]}')
            self.finalFLab.config(text=f'Final DeltaF: {self.finalDeltaF:.1f} Hz')
            self.sDensLab.config(text=f'Surface density: {self.sDens} g/cm^2')

            self.fileBut.configure(state='disabled')
        except Exception as e:
            print(e)

    def plotCoating(self):
        
        try:
            fig, ax = plt.subplots(1, 1)
            if self.title is not None:
                fig.suptitle(self.title)
            
            line1, = ax.plot(self.time, self.deltaF, color="mediumorchid", label="$\\Delta f$")
            ax.set_xlabel("$t$ / min")
            ax.set_ylabel("$\\Delta f$ / kHz")
            #ax.yaxis.set_major_locator(ticker.MultipleLocator(base=0.1))
            #ax.xaxis.set_major_locator(ticker.MultipleLocator(base=30))
            ax.grid(linestyle="-")
            axa = ax.twinx()
            line2, = axa.plot(self.time, self.temperature, color="coral", label="$T$", lw=1, ls="-")
            axa.set_ylabel("$T$ / $^{\\circ}$C")
            axa.legend(handles=[line1, line2], loc="center left")
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(e)

def main():
    root = Tk()
    coatingPlotter(root)
    root.mainloop()

if __name__ == '__main__':
    main()