from tkinter.constants import ACTIVE, ANCHOR, DISABLED, NORMAL, S
from writePLCOpen import runPLCopenWriter
from writePNML import runPNMLWriter
from parsePNML import Place, Arc, Transition, getET, main, parsePNML, runPNMLParse, ET, tree
from writeTCTfiles import runTCTfileWriter
from writeTCT2PN import runTCT2PN
import tkinter as tk
from tkinter import BOTH, BooleanVar, Button, Frame, Grid, OptionMenu, StringVar, filedialog, Text
import os
from functools import partial


root = tk.Tk()
root.title("PN2IC - Petri Net to Implementable Code")
root.geometry("1098x610")
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
        label = tk.Label(fileNameFrame, text=app)
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
    labelSCTRestriction = tk.Label(frameSCT,text="M(P(i))+M(P(n))")
    labelSCTRestriction.grid(row=buttonAddSCTRestriction.grid_info()['row'], column='0', ipadx=10, ipady=10)
    global labelSCTLessThanEqual
    labelSCTLessThanEqual = tk.Label(frameSCT, text="<=", font="bold", width=6)
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
    
    canvas.configure(scrollregion=canvas.bbox('all'))
    
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
    
    canvas.configure(scrollregion=canvas.bbox('all')) 
                     
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

def runTCTfiles():
    print("Running TCT files generator")
    for place in Place.instances:
        stateName = place.name
        print("Place:" + place.name)
        if place.hasinitialmark:
            print("InitialMark")
            trSucList = Arc.getTSuc(place.id)
            trPreList = Arc.getTPre(place.id)
            uptransitions = []
            downtransitions = []
            for trSuc in trSucList:
                uptransitions.append(Transition.getName(trSuc))
            for trPre in trPreList:
                downtransitions.append(Transition.getName(trPre))
        else:
            trSucList = Arc.getTSuc(place.id)
            trPreList = Arc.getTPre(place.id)
            uptransitions = []
            downtransitions = []
            for trPre in trPreList:
                uptransitions.append(Transition.getName(trPre))
            for trSuc in trSucList:
                downtransitions.append(Transition.getName(trSuc))
        

        runTCTfileWriter(stateName,uptransitions,downtransitions)

def runSCT():
    print("RUN SCT")
    runTCT2PN()
    
def runPLCopen():
    runPLCopenWriter()

topFrame = tk.LabelFrame(root, text="File")
topFrame.pack(fill=tk.BOTH, expand=0,padx=1,pady=1)

fileNameFrame = tk.Frame(topFrame, bg="white")
fileNameFrame.pack(side=tk.LEFT)
  
mainFrame = tk.LabelFrame(root, text="Specification Equations")
mainFrame.pack(fill=BOTH, expand=1)


canvas = tk.Canvas(mainFrame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

sctScrollH = tk.Scrollbar(mainFrame, orient=tk.HORIZONTAL, command=canvas.xview)
sctScrollH.pack(side=tk.BOTTOM, fill=tk.X)

sctScrollV = tk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=canvas.yview)
sctScrollV.pack(side=tk.RIGHT, fill=tk.Y)


canvas.configure(yscrollcommand=sctScrollV.set, xscrollcommand=sctScrollH.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))


frameSCT = tk.Frame(canvas)
canvas.create_window((0,0), window=frameSCT, anchor="nw")


bapplySCT = BooleanVar()

buttonAddSCTRestriction = tk.Button(frameSCT,text="Add Restriction", state=DISABLED)
#buttonAddSCTRestriction.grid(row=1, column=0, ipadx=0, ipady=12)
buttonAddSCTRestriction.grid(row=1, column=0, ipady=20)
buttonAddSCTRestriction.config(command=lambda i=buttonAddSCTRestriction.grid_info()['row']: addSCTRestriction(i))


commandFrame = tk.LabelFrame(root, text="Commands", padx=2, pady=5)
commandFrame.pack()

openFile = tk.Button(commandFrame, text="Open File", padx=10, pady=2,
                     fg="white", bg="#263d42", command=addApp)

openFile.grid(row=0, column=0, padx=2, pady=2)

runApps = tk.Button(commandFrame, text="Run Apps", padx=10, pady=2,
                    fg="white", bg="#263d42", command=runApps)

runApps.grid(row=0, column=1, padx=2, pady=2)

checkBoxSCT = tk.Checkbutton(commandFrame, variable=bapplySCT, text="Apply SCT", command=applySCT, padx=2, pady=2, bg='#263d42', fg='white', activeforeground='white', selectcolor="gray")
#checkBoxSCT.grid(row=0, column=0, ipadx=0.2, ipady=10)
checkBoxSCT.grid(row=0, column=2, padx=2, pady=2)

runEquations = tk.Button(commandFrame, text="Run Spec Equations", padx=10, pady=2,
                    fg="white", bg="#263d42", command=runEquations)

runEquations.grid(row=0, column=3, padx=2, pady=2)

runTCTfiles = tk.Button(commandFrame, text="Gen TCT Files", padx=10, pady=2,
                    fg="white", bg="#263d42", command=runTCTfiles)

runTCTfiles.grid(row=0, column=4, padx=2, pady=2)

runSCTfiles = tk.Button(commandFrame, text="Run SCT", padx=10, pady=2,
                    fg="white", bg="#263d42", command=runSCT)

runSCTfiles.grid(row=0, column=5, padx=2, pady=2)


runPLCopen = tk.Button(commandFrame, text="Run PLCopen Converter", padx=10, pady=2,
                    fg="white", bg="#263d42", command=runPLCopen)

runPLCopen.grid(row=0, column=6, padx=2, pady=2)

root.mainloop()

