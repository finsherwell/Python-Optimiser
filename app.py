import tkinter
from tkinter import ttk
import os

import sv_ttk

root = tkinter.Tk()

theme_path = os.path.join(os.getcwd(), 'forest-dark.tcl')  # Ensure this is the correct path
root.tk.call('source', theme_path)
ttk.Style().theme_use('forest-dark')

button = ttk.Button(root, text="I'm a themed button")
button.pack(pady=20)

root.mainloop()