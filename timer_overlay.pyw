import tkinter as tk
import time
import os

TIME_FILE = "C:\\ParentalControl\\time_left.txt"

def read_time_left():
    if os.path.exists(TIME_FILE):
        with open(TIME_FILE, "r") as f:
            return f.read().strip()
    return "??"

root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.7)  # transparency

# Place in bottom-right
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 160
height = 50
x = screen_width - width - 20
y = screen_height - height - 60
root.geometry(f"{width}x{height}+{x}+{y}")

label = tk.Label(root, text="", font=("Arial", 18), bg="black", fg="white")
label.pack(expand=True, fill="both")

def update_label():
    mins = read_time_left()
    label.config(text=f"{mins} min left")
    root.after(60000, update_label)  # update every minute

update_label()
root.mainloop()
