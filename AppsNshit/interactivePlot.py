import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import random

class LivePlotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Live Data Plotter")
        
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [], lw=2)
        
        self.ax.set_xlim(0, 100)
        self.ax.set_ylim(0, 10)
        self.xdata, self.ydata = [], []
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.BOTTOM)
        
        self.stop_button = tk.Button(self.button_frame, text="Stop and Save", command=self.stop)
        self.stop_button.pack(side=tk.LEFT)
        
        self.running = True
        self.ani = animation.FuncAnimation(self.fig, self.update_plot, interval=1000, blit=True)
    
    def update_plot(self, frame):
        if self.running:
            self.xdata.append(len(self.xdata))
            self.ydata.append(random.uniform(0, 10))
            
            self.line.set_data(self.xdata, self.ydata)
            self.ax.set_xlim(0, max(100, len(self.xdata)))
            self.ax.set_ylim(0, 10)
        return self.line,
    
    def stop(self):
        self.running = False
        filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if filename:
            self.fig.savefig(filename)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = LivePlotApp(root)
    root.mainloop()
