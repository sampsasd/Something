import tkinter as tk
from tkinter import ttk

class ValueUpdater:
    def __init__(self, root):
        self.root = root
        self.root.title("Value Updater")

        self.values = [tk.StringVar(value="Value 1"), tk.StringVar(value="Value 2"), tk.StringVar(value="Value 3")]

        self.create_widgets()

    def create_widgets(self):
        for i, val in enumerate(self.values):
            label = ttk.Label(self.root, textvariable=val)
            label.grid(row=i, column=0, padx=10, pady=10)

            entry = ttk.Entry(self.root)
            entry.grid(row=i, column=1, padx=10, pady=10)

            button = ttk.Button(self.root, text="Update", command=lambda i=i, entry=entry: self.update_value(i, entry))
            button.grid(row=i, column=2, padx=10, pady=10)

    def update_value(self, index, entry):
        new_value = entry.get()
        if new_value:
            self.values[index].set(new_value)

def main():
    root = tk.Tk()
    app = ValueUpdater(root)
    root.mainloop()

if __name__ == "__main__":
    main()