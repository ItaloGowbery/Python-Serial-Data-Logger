#import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(themename="superhero")

root.geometry("800x500")
root.title("ENose")


label = ttk.Label(root, text="ENose", font=("Arial", 18))
label.pack(padx=0, pady=20)

delaybox = ttk.Spinbox(bootstyle=SECONDARY)
delaybox.pack(side=LEFT, anchor=N, padx=10, pady=10)

menuCOM = ttk.Menubutton(bootstyle=SECONDARY)
menuCOM.pack(side=RIGHT, anchor=N, padx=10, pady=10)

BT1 = ttk.Button(root, text="Start", bootstyle=SUCCESS)
BT1.pack(pady=20, padx=10, side=RIGHT, anchor=S)


BT2 = ttk.Button(root, text="STOP", bootstyle=DANGER)
BT2.pack(pady=20, padx=0, side=RIGHT, anchor=S)



root.mainloop()