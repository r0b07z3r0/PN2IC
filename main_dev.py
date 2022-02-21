from tkinter.constants import ACTIVE, ANCHOR, DISABLED, NORMAL, S
from parsePNML_dev import Place, parsePNML
import tkinter as tk
from tkinter import BooleanVar, Frame, Grid, OptionMenu, StringVar, filedialog, Text
import os

root = tk.Tk()
apps = []
placeAvailable = [""]
selectedPlace = StringVar(root)
selectedPlace.set(placeAvailable[0])

listPlace = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9","p10"]
listAddPlaceButton = ["1"]
variable_dict = {}
addVardict = {}


def addApp():
    filename = filedialog.askopenfilename(initialdir="", title="Select File",
                                          filetypes=(("PNML Files", "*.pnml"),
                                                     ("all files", "*.*")))
    parsePNML(filename)
    apps.append(filename)
    print(filename)
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()

def runApps():
    Place.print_instances()
    print(Place.listPlace())
    placeAvailable = Place.listPlace()
    dropMenu = OptionMenu(frame, selectedPlace, *placeAvailable)
    dropMenu.pack()
    
def applySCT():
    if bapplySCT.get():
        buttonAddSCTRestriction.config(state=NORMAL)
    else:
        buttonAddSCTRestriction.config(state=DISABLED)


def addSCTRestriction(self):
    labelSCTRestriction = tk.Label(frameSCT,text="M(p(i))")
    labelSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='0', ipadx=10, ipady=10)
    buttonAddVar = StringVar(frameSCT)
    buttonAddVar.set(listAddPlaceButton[0])
    addVardict[buttonAddSCTRestriction.grid_info()['row']+1] = buttonAddVar
    global buttonAddSCTPlace
    buttonAddSCTPlace = tk.Button(frameSCT,text=buttonAddSCTRestriction.grid_info()['row'],state=NORMAL, command= lambda i=buttonAddSCTRestriction.grid_info()['row']: addSCTPlace(i))
    buttonAddSCTPlace.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='1', ipadx=10, ipady=10)
    buttonAddSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row']+1)
        
def addSCTPlace(self):
    print("CALLING ADD SCT PLACE from ADD %d" % self)
    print(buttonAddSCTPlace.winfo_id())
    tk.Widget(id)
    selectedPlace = StringVar(frameSCT)
    selectedPlace.set(listPlace[0])
    variable_dict[buttonAddSCTPlace.grid_info()['column']] = selectedPlace
    optPlaceMenu = tk.OptionMenu(frameSCT, selectedPlace, *listPlace)
    optPlaceMenu.grid(row=self, column = buttonAddSCTPlace.grid_info()['column'])
    buttonAddSCTPlace.grid(row=self, column = optPlaceMenu.grid_info()['column']+1)


canvas = tk.Canvas(root, height=500, width=1000, bg="#263d42")
canvas.pack()

frame = tk.Frame(canvas, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.05)


frameSCT = tk.Frame(frame, bg="gray")
frameSCT.place(rely=0.2, relx=0, relheight=1, relwidth=1)
bapplySCT = BooleanVar()
checkBoxSCT = tk.Checkbutton(frameSCT, variable=bapplySCT, text="Apply SCT", command=applySCT, border=5,borderwidth=1)
checkBoxSCT.grid(row='0', column='0', ipadx=0.2, ipady=10)
buttonAddSCTRestriction = tk.Button(frameSCT,text="Add Restriction", state=DISABLED)
buttonAddSCTRestriction.grid(row='1', column='0', ipadx=0, ipady=10)
buttonAddSCTRestriction.config(command=lambda i=buttonAddSCTRestriction.grid_info()['row']: addSCTRestriction(i))



openFile = tk.Button(root, text="Open File", padx=10, pady=5,
                     fg="white", bg="#263d42", command=addApp)

openFile.pack()

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5,
                    fg="white", bg="#263d42", command=runApps)

runApps.pack()




root.mainloop()

