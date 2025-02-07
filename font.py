import tkinter as tk
import tkinter.font as tkFont

import os
import os
os.environ["GDK_BACKEND"] = "x11"
print("Session Type:", os.getenv("XDG_SESSION_TYPE"))

root = tk.Tk()
available_fonts = tkFont.families()
root.destroy()

print(available_fonts)