from parsePNML import parsePNML
import tkinter as tk
from tkinter import Frame, filedialog, Text
import os

root = tk.Tk()
apps = []


def addApp():
    filename = filedialog.askopenfilename(initialdir="", title="Select File",
                                          filetypes=(("executables", "*.exe"),
                                                     ("all files", "*.*")))
    apps.append(filename)
    print(filename)
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()

#def runApps():

canvas = tk.Canvas(root, height=500, width=500, bg="#263d42")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.05)

openFile = tk.Button(root, text="Open File", padx=10, pady=5,
                     fg="white", bg="#263d42", command=addApp)

openFile.pack()

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5,
                    fg="white", bg="#263d42")

runApps.pack()
root.mainloop()

