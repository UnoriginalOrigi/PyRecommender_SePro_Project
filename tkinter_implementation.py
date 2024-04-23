from tkinter import *
from tkinter import ttk

def tkinter_program():
    root = Tk(screenName="PyRecommender",baseName="PyRecommender",className="PyRecommender")
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    ttk.Button(frm, text="Login", command=root.destroy).grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
    root.mainloop()