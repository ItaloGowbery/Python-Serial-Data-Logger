import serial
import serial.tools.list_ports
import threading
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog

ser = None
baud_rate = 9600
running = False
data = []

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]



root = ttk.Window(themename="superhero")
root.geometry("800x500")
root.title("ENose")



label = ttk.Label(root, text="ENose", font=("Arial", 18))
label.pack(padx=0, pady=0)

#READ DELAY
delaybox = ttk.Spinbox(bootstyle=SECONDARY)
delaybox.pack(side=LEFT, anchor=N, padx=10, pady=0)

#PORT MENU
port_var = ttk.StringVar()
port_menu = ttk.Combobox(root, textvariable=port_var, values=list_serial_ports(), state="readonly")
port_menu.pack(side=RIGHT, anchor=N, padx=10, pady=0)











#START BUTTON
BT2 = ttk.Button(root, text="Stop", bootstyle=DANGER)
BT2.pack(pady=10, padx=5, side=RIGHT, anchor=SW)

#STOP BUTTON
BT1 = ttk.Button(root, text="Start", bootstyle=SUCCESS)
BT1.pack(pady=10, padx=5, side=RIGHT, anchor=SW)






root.mainloop()