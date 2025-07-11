#!/usr/bin/env python3
"""
Simple test GUI to check if tkinter is working
"""

import tkinter as tk
from tkinter import messagebox

def test_function():
    messagebox.showinfo("Test", "GUI is working!")

# Create main window
root = tk.Tk()
root.title("Test GUI")
root.geometry("300x200")

# Add a label
label = tk.Label(root, text="Quick Document Converter Test", font=("Arial", 12))
label.pack(pady=20)

# Add a button
button = tk.Button(root, text="Click Me!", command=test_function, font=("Arial", 10))
button.pack(pady=10)

# Add status
status = tk.Label(root, text="If you see this, tkinter is working!", fg="green")
status.pack(pady=10)

print("Starting test GUI...")
print("If you don't see a window, there might be a display issue.")

# Start the GUI
root.mainloop()

print("GUI closed.")
