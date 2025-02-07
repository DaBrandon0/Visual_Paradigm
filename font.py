import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
available_fonts = tkFont.families()
root.destroy()

print(available_fonts)