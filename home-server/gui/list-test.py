import tkinter as tk
from tkinter import ttk

top = tk.Tk()

lb1 = tk.Listbox(top)
lb1.insert(1, "Python")
lb1.insert(2, "Perl")
lb1.insert(tk.END, "C++")
lb1.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

cs = tk.Canvas(top)
cs.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

top.mainloop()
