from tkinter import *

root = Tk()
listPlace = ["p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8", "p9","p10"]
variable_dict = {}
selectedPlace = StringVar(root)
selectedPlace.set(listPlace[0])
listSelected = []
listplaces =[""]

def addPlaceToTCS():
    variable = Stri
    globals()[listplaces[myButton.grid_info()['column']]] = OptionMenu(root, selectedPlace, *listPlace)
    globals()[listplaces[myButton.grid_info()['column']]].grid(row=3, column = myButton.grid_info()['column'])
    print(myButton.grid_info()['column'])
    print(globals()[listplaces[myButton.grid_info()['column']]].grid_info())
    listSelected.append(listplaces[myButton.grid_info()['column']].get())
    myButton.grid(row=3, column = myButton.grid_info()['column']+1)
    print(listSelected)

myLabel1 = Label(root, text="Hello World 1")
myLabel2 = Label(root, text="Hello World 2")
myLabel3 = Label(root, text="Hello World 3")
myButton = Button(root, text="+", padx=10, pady=10, command=addPlaceToTCS)


myLabel1.grid(row = 0, column=0)
myLabel2.grid(row = 0, column=3)
myLabel3.grid(row = 1, column=0)
myButton.grid(row=3, column=3)

root.mainloop()