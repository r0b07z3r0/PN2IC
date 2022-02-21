from tkinter import *

root = Tk()
listPlace = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9","p10"]
variable_dict = {}

listSelected = []
listplaces =[""]

def addPlaceToTCS():
    selectedPlace = StringVar(root)
    selectedPlace.set(listPlace[0])
    variable_dict[myButton.grid_info()['column']] = selectedPlace
    optPlaceMenu= OptionMenu(root, selectedPlace, *listPlace)
    optPlaceMenu.grid(row=3, column = myButton.grid_info()['column'])
    print(myButton.grid_info()['column'])
    print(optPlaceMenu.grid_info())
    listSelected.append(selectedPlace.get())
    myButton.grid(row=3, column = myButton.grid_info()['column']+1)
    print(listSelected)


def printSelected():
    for x,y in variable_dict.items():
        print(x,y.get())
    
    
myLabel1 = Label(root, text="Hello World 1")
myLabel2 = Label(root, text="Hello World 2")
myLabel3 = Label(root, text="Hello World 3")
myButton = Button(root, text="+", padx=10, pady=10, command=addPlaceToTCS)
myGetSelected = Button(root, text="Get SELECTED", padx=10, pady=10, command=printSelected)


myLabel1.grid(row = 0, column=0)
myLabel2.grid(row = 0, column=3)
myLabel3.grid(row = 1, column=0)
myButton.grid(row=3, column=3)
myGetSelected.grid(row=10, column=0)

root.mainloop()