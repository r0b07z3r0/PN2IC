from tkinter.constants import ACTIVE, ANCHOR, DISABLED, NORMAL, S
from writePNML import runPNMLWriter
from parsePNML import Place, Arc, getET, main, parsePNML, runPNMLParse, ET, tree
import tkinter as tk
from tkinter import BooleanVar, Frame, Grid, OptionMenu, StringVar, filedialog, Text
import os
from functools import partial

root = tk.Tk()
apps = []
placeAvailable = [""]
selectedPlace = StringVar(root)
selectedPlace.set(placeAvailable[0])

listPlace = [""]
listAddPlaceButton = [""]
listPlaceEquation = []
listLabelLessThanEqual = [""]
listEntryEquation = [""]
global numberOfRestriction
numberOfRestriction = 0
dictSelectedPlaces = {}
addVardict = {}

class Specification:
    
    id: str
    #places = []
    ntoken = str
    specInstances = []
    instances = set()
    
    def __init__(self, id):
        self.id = id
        self.places = []
        Specification.specInstances.append(self.id)
        Specification.instances.add(self)
    
    def addSpecPlace(self,place):
        self.places.append(place)
        Specification.instances.add(self)
        
    def setnToken(self, ntoken):
        self.ntoken = ntoken
        Specification.instances.add(self)
    
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.id)
            print('Places: ' + str(instance.places))
            print('Number of Token: ' + instance.ntoken)
            print(instance.id + ': ' + str(instance.places) + ' <= ' + instance.ntoken)

    

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
    #runPNMLParse(filename)
    Place.print_instances()
    print(Place.listPlace())
    listPlace.extend(Place.listPlace())
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
    buttonAddSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row']+1)
    listAddPlaceButton.append(buttonAddSCTPlace)
    addSCTPlace(buttonAddSCTRestriction.grid_info()['row']-1)
    addSCTPlace(buttonAddSCTRestriction.grid_info()['row']-1)
    global numberOfRestriction
    numberOfRestriction += 1
        
def addSCTPlace(self):
    print("CALLING ADD SCT PLACE from ADD %d" % self)
    print(buttonAddSCTPlace.winfo_id())
    selectedPlace = StringVar(frameSCT)
    selectedPlace.set(listPlace[1])
    dictSelectedPlaces[str(listAddPlaceButton[self].grid_info()['row']) + "," + str(listLabelLessThanEqual[self].grid_info()['column'])] = selectedPlace
    listPlaceEquation.append(dictSelectedPlaces)
    optPlaceMenu = tk.OptionMenu(frameSCT, selectedPlace, *listPlace)
    optPlaceMenu.grid(row=self, column = listLabelLessThanEqual[self].grid_info()['column'])
    listLabelLessThanEqual[self].grid(row=listAddPlaceButton[self].grid_info()['row'], column=listLabelLessThanEqual[self].grid_info()['column']+1)
    listEntryEquation[self].grid(row=listAddPlaceButton[self].grid_info()['row'], column=listLabelLessThanEqual[self].grid_info()['column']+1)
    listAddPlaceButton[self].grid(row=self, column = listLabelLessThanEqual[self].grid_info()['column']+2)

def runEquations():
    print("Number of Restriction: " + str(numberOfRestriction))
    
    eliminateBlank = []
    for x,y in dictSelectedPlaces.items():
        if y.get() == "":
            eliminateBlank.append(x)
    for x in eliminateBlank:
        del dictSelectedPlaces[x]
    print(eliminateBlank)
    
    for x in range(1, numberOfRestriction+1):
        globals()["Spec"+str(x)] = Specification("Spec"+str(x))
        
        for v,k in dictSelectedPlaces.items():
            print(v,k.get())
            if v.startswith(str(x)+","):
                print(v.startswith(str(x)+","))
                print("Spec"+str(x) + " " + str(k.get()))
                globals()["Spec"+str(x)].addSpecPlace(k.get())
    
    i = 1    
    for z in listEntryEquation[1:]:
        globals()["Spec"+str(i)].setnToken(z.get())
        print(z.get())
        i += 1
        
    print(list(dictSelectedPlaces))
    
    Specification.print_instances()

    for x in range(1, numberOfRestriction+1):
        print(globals()["Spec"+str(x)].places)

        
    bufferCalc()

def bufferCalc():
    print("Generating Places, Arcs and Selecting Transition")
    
    print("Number of Specifications: " + str(len(Specification.specInstances)))
    for specs in Specification.specInstances:
        #LOOP Each Specification
        pSpec = []
        print(specs)
        print(globals()[specs].places)
        globals()["p-" + str(specs) + "_0"] = Place("p-" + str(specs) + "_0")
        globals()["p-" + str(specs) + "_0"].setPlaceName(str(specs)+"_0")
        globals()["p-" + str(specs) + "_0"].setInitialMark("1")
        globals()["p-" + str(specs) + "_0"].setPlaceLabel("AUTONET_" + str(specs))
        globals()["p-" + str(specs) + "_0"].setPlaceNameGraph('0', '-10')
        globals()["p-" + str(specs) + "_0"].setPlaceLabelGraph('0', '0')
        globals()["p-" + str(specs) + "_0"].setPlacePos('0', '0')
        pSpec.append("p-" + str(specs) + "_0")
        globals()["p-" + str(specs) + "_1"] = Place("p-" + str(specs) + "_1")
        globals()["p-" + str(specs) + "_1"].setPlaceName(str(specs)+"_1")
        globals()["p-" + str(specs) + "_1"].setInitialMark("0")
        globals()["p-" + str(specs) + "_1"].setPlaceLabel("AUTONET_" + str(specs))
        globals()["p-" + str(specs) + "_1"].setPlaceNameGraph('0', '-10')
        globals()["p-" + str(specs) + "_1"].setPlaceLabelGraph('0', '0')
        globals()["p-" + str(specs) + "_1"].setPlacePos('10', '0')
        pSpec.append("p-" + str(specs) + "_1")
        tUpper = []
        tLower = []
        print("Define transition for buffer:")
        
        for place in globals()[specs].places:
            #LOOP Each place within a Specification
            print(place)
            print(Arc.getTPre(Place.getID(place)))
            print(Arc.getTSuc(Place.getID(place)))
        
        print("END")
        for place in globals()[specs].places:
            #LOOP Each place within a Specification
            print(place)
            if int(Place.getInitialMark(place)) > 0:
                tUpper.extend((Arc.getTSuc(Place.getID(place))))
                tLower.extend((Arc.getTPre(Place.getID(place))))
            else:
                tUpper.extend((Arc.getTPre(Place.getID(place))))
                tLower.extend((Arc.getTSuc(Place.getID(place))))
        
            #         if int(Place.getInitialMark(place)) > 0:
            #     if len(Arc.getTSuc(Place.getID(place))) > 1:
            #         tUpper.extend(Arc.getTSuc(Place.getID(place)))
            #     else:
            #         tUpper.append(Arc.getTSuc(Place.getID(place)))
                    
            #     if len(Arc.getTPre(Place.getID(place))) > 1:
            #         tLower.extend(Arc.getTPre(Place.getID(place)))
            #     else:   
            #         tLower.append(Arc.getTPre(Place.getID(place)))
            # else:
            #     if len(Arc.getTPre(Place.getID(place))) > 1:
            #         tUpper.extend(Arc.getTPre(Place.getID(place)))
            #     else:
            #         tUpper.append(Arc.getTPre(Place.getID(place)))
                    
            #     if len(Arc.getTSuc(Place.getID(place))) > 1:
            #         tLower.extend(Arc.getTSuc(Place.getID(place)))
            #     else:   
            #         tLower.append(Arc.getTSuc(Place.getID(place)))
                    
        print("Upper and Lower before Cut")
        print(tUpper)
        print(tLower) 
        popOutUp = []
        popOutLow = []
        
        for i in range(len(tUpper)):
            for j in range(len(tLower)):
                if tUpper[i] == tLower[j]:
                    popOutUp.append(i)
                    popOutLow.append(j)
        
        popOutUp.sort(reverse=True)
        popOutLow.sort(reverse=True)
        print("Pop")
        print(popOutUp)
        print(popOutLow) 
        
        for i in popOutUp:
            tUpper.pop(i)
        
        for i in popOutLow:
            tLower.pop(i)   
            
        
            
        # while nRepeat:
        #     for i in range(len(tUpper)):
        #         for j in range(len(tLower)):
        #             if tUpper[i] == tLower[j]:
        #                 tUpper.pop(i)
        #                 tLower.pop(j)
        #                 breaker = True
        #                 break
        #             nRepeat = False
        #         if breaker:
        #             break
        print("Upper and Lower after Cut")
        print(tUpper)
        print(tLower)         
        
        #Generate Arcs, Total number of Arcs = Places * Transitions
        for i in range(len(pSpec)-1):
            for j in range(len(tUpper)):
                
                globals()["e-" + str(specs) + "_UP_from_P_" + str(i) + str(j)] = Arc("e-" + str(specs) + "_UP_from_P_" + str(i) + str(j),
                                                                    pSpec[i], tUpper[j])
                
            for j in range(len(tLower)):
                globals()["e-" + str(specs) + "_LOW_to_P_" + str(i) + str(j)] = Arc("e-" + str(specs) + "_LOW_to_P_" + str(i) + str(j),
                                                                    tLower[j], pSpec[i]) 
                
        for i in range(1,len(pSpec)):
            for j in range(len(tUpper)):
                globals()["e-" + str(specs) + "_UP_to_P_" + str(i) + str(j)] = Arc("e-" + str(specs) + "_UP_to_P_" + str(i) + str(j),
                                                                    tUpper[j], pSpec[i])
                
            for j in range(len(tLower)):
                globals()["e-" + str(specs) + "_LOW_from_P_" + str(i) + str(j)] = Arc("e-" + str(specs) + "_LOW_from_P_" + str(i) + str(j),
                                                                    pSpec[i], tLower[j]) 
        
        
        #Arc.print_instances()
        #print(Place.getID(place))
        #print(Place.getInitialMark(place))
        #print(Arc.getTPre(Place.getID(place)))
        
    runPNMLWriter()
        
        
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

