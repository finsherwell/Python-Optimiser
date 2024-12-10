# app.py
import tkinter as tk
from tkinter import ttk, filedialog
import sv_ttk
from profile_script import profile_script
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
root = tk.Tk()
root.title("Python Script Profiler")
root.geometry("900x650")  # Resize for more space

# Apply the Forest theme
sv_ttk.set_theme("dark")

# Use a consistent font
font_style = ("Arial", 12)

root.mainloop()