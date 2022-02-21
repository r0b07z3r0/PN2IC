from tkinter.constants import ACTIVE, ANCHOR, DISABLED, NORMAL, S
from parsePNML import Place, main, parsePNML, runPNMLParse
import tkinter as tk
from tkinter import BooleanVar, Frame, Grid, OptionMenu, StringVar, filedialog, Text
import os
from functools import partial
import re

root = tk.Tk()
apps = []
placeAvailable = [""]
selectedPlace = StringVar(root)
selectedPlace.set(placeAvailable[0])

listPlace = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9","p10"]
listAddPlaceButton = [""]
listRemSCT = [""]
listPlaceEquation = []
listLabelLessThanEqual = [""]
listEntryEquation = [""]
dictSelectedPlaces = {}
addVardict = {}

class Specification:
    
    id: str
    places = []
    ntoken = str
    specInstances = []
    instances = set()
    
    def __init__(self, id, places, ntoken):
        self.id = id
        self.places = places
        self.ntoken = ntoken
        Specification.specInstances.append(self.id)
        Specification.instances.add(self)
    
    
    

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
    runPNMLParse()
    Place.print_instances()
    print(Place.listPlace())
    #placeAvailable = Place.listPlace()

    
def applySCT():
    if bapplySCT.get():
        buttonAddSCTRestriction.config(state=NORMAL)
    else:
        buttonAddSCTRestriction.config(state=DISABLED)


def addSCTRestriction(self):
    labelSCTRestriction = tk.Label(frameSCT,text="M(P(i))+M(P(n))", background="#D3D3D3")
    labelSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='0', ipadx=10, ipady=10)
    global labelSCTLessThanEqual
    labelSCTLessThanEqual = tk.Label(frameSCT, text="<=", background="#D3D3D3", font="bold", width=6)
    labelSCTLessThanEqual.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='1', ipadx=10, ipady=10)
    listLabelLessThanEqual.append(labelSCTLessThanEqual)
    global entrySCTEquation
    entrySCTEquation = tk.Entry(frameSCT, width=6)
    entrySCTEquation.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='2', ipadx=10, ipady=10)
    listEntryEquation.append(entrySCTEquation)
    buttonAddVar = StringVar(frameSCT)
    addVardict[buttonAddSCTRestriction.grid_info()['row']+1] = buttonAddVar
    global buttonAddSCTPlace
    buttonAddSCTPlace = tk.Button(frameSCT,text="+",state=NORMAL, command= lambda i=buttonAddSCTRestriction.grid_info()['row']: addSCTPlace(i))
    buttonAddSCTPlace.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='3', ipadx=10, ipady=10)
    listAddPlaceButton.append(buttonAddSCTPlace)
    global buttonRemSCT
    buttonRemSCT = tk.Button(frameSCT,text="DEL",state=NORMAL, command= lambda i=buttonAddSCTRestriction.grid_info()['row']: removeSCTRestriction(i))
    buttonRemSCT.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='3', ipadx=10, ipady=10)
    listRemSCT.append(buttonRemSCT)
    buttonAddSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row']+1)

    addSCTPlace(buttonAddSCTRestriction.grid_info()['row']-1)
    addSCTPlace(buttonAddSCTRestriction.grid_info()['row']-1)
        
def addSCTPlace(self):
    print("CALLING ADD SCT PLACE from ADD %d" % self)
    print(buttonAddSCTPlace.winfo_id())
    selectedPlace = StringVar(frameSCT)
    selectedPlace.set(listPlace[0])
    dictSelectedPlaces[str(listAddPlaceButton[self].grid_info()['row']) + "," + str(listLabelLessThanEqual[self].grid_info()['column'])] = selectedPlace
    listPlaceEquation.append(dictSelectedPlaces)
    optPlaceMenu = tk.OptionMenu(frameSCT, selectedPlace, *listPlace)
    optPlaceMenu.grid(row=self, column = listLabelLessThanEqual[self].grid_info()['column'])
    listLabelLessThanEqual[self].grid(row=listAddPlaceButton[self].grid_info()['row'], column=listLabelLessThanEqual[self].grid_info()['column']+1)
    listEntryEquation[self].grid(row=listAddPlaceButton[self].grid_info()['row'], column=listLabelLessThanEqual[self].grid_info()['column']+1)
    listAddPlaceButton[self].grid(row=self, column = listLabelLessThanEqual[self].grid_info()['column']+2)
    listRemSCT[self].grid(row=self, column = listLabelLessThanEqual[self].grid_info()['column']+3)

def removeSCTRestriction(self):
    print("REMOVE " + str(self))
    print("Before removal")
    remDict = []
    for x, y in dictSelectedPlaces.items():
        print(x,y.get())
        if x.startswith(str(self)+','):
            remDict.append(x)
            
    for x in remDict:
        del dictSelectedPlaces[x]
    
    print("After removal")
    for x, y in dictSelectedPlaces.items():
        print(x,y.get())
    
    for x in frameSCT.grid_slaves(self):
        x.destroy()
    
    listEntryEquation.pop(self)
    listAddPlaceButton.pop(self)
    listLabelLessThanEqual.pop(self)
    listRemSCT.pop(self)
    
    
    listAddPlaceButton[self].configure(command= lambda i=self: addSCTPlace(i))
    buttonAddSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row']-1)
    buttonAddSCTRestriction.configure(command=lambda i=buttonAddSCTRestriction.grid_info()['row']: addSCTRestriction(i))


    
    
def runEquations():
    eliminateBlank = []
    for x,y in dictSelectedPlaces.items():
        if y.get() == "":
            eliminateBlank.append(x)
    for x in eliminateBlank:
        del dictSelectedPlaces[x]
    print(eliminateBlank)
    
    for x,y in dictSelectedPlaces.items():
        print(x,y.get())
        
    for z in listEntryEquation[1:]:
        print(z.get())
        
    print(list(dictSelectedPlaces))
    
canvas = tk.Canvas(root, height=400, width=1000, bg="#263d42")
canvas.pack()

frame = tk.Frame(canvas, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.05)


frameSCT = tk.Frame(frame, bg="#D3D3D3")
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

runEquations = tk.Button(root, text="Run Spec Equations", padx=10, pady=5,
                    fg="white", bg="#263d42", command=runEquations)

runEquations.pack()

root.mainloop()

