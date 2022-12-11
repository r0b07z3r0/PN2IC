from parsePNML import ET, getET, Net, Page, Place, Transition, Arc
import re
import os
import collections
from writePNML import runPNMLWriter

def runTCT2PN():
    main()   

def main():
    print("Running TCT2PN")
    
    listaADS = []
    listaPasta = os.listdir()
    for fileADS in listaPasta:
        if fileADS.startswith('SUPCON_') and fileADS.endswith('.ADS'):
            listaADS.append(fileADS)
    #print(listaADS)

    for fileSUPCON in listaADS:
        fileSUPCON = open(fileSUPCON)
        linesSUPCON = fileSUPCON.readlines()
        fileSUPCON.close()

        num = 1
        startIndex = linesSUPCON.index('# Example: 2 0 1 (for transition labeled 0 from state 2 to state 1).\n') + 1
        totalSize = len(linesSUPCON)
        stepsList = []
        stepTrList = []
        for line in linesSUPCON:
            if num == 3:
                nameBase = re.split(r'\n',line)[0]
                print(nameBase)
            if num > startIndex and num != totalSize:
                bufferArr = re.split(r'\b',line)
                print(bufferArr)
                stepTrList.append([bufferArr[1],bufferArr[3],bufferArr[5]])
                stepsList.append(bufferArr[1])
            num+=1


        print(stepsList)
        print(stepTrList)
        stepsList = list(dict.fromkeys(stepsList))
        print(stepsList)

        for stepsName in stepsList:
            stepsList[stepsList.index(stepsName)] = nameBase + "_" + stepsName
        
        print(stepsList)


        for specs in stepsList:
            #LOOP Each Specification
            print(specs)
            globals()["p-" + str(specs)] = Place("p-" + str(specs))
            globals()["p-" + str(specs)].setPlaceName(str(specs))
            if specs.endswith("0"):
                globals()["p-" + str(specs)].setInitialMark("1")
            else:
                globals()["p-" + str(specs)].setInitialMark("0")
            globals()["p-" + str(specs)].setPlaceLabel("AUTONET_" + str(specs))
            globals()["p-" + str(specs)].setPlaceNameGraph('0', '-10')
            globals()["p-" + str(specs)].setPlaceLabelGraph('0', '0')
            globals()["p-" + str(specs)].setPlacePos('0', '0')
        
        stepTrListID = []
        for bufferModel in stepTrList:
            transitionName = "t" + bufferModel[1]
            transitionID = Transition.getID(transitionName)
            print(transitionID)
            stepTrListID.append(["p-" + nameBase + "_" + bufferModel[0], transitionID, "p-" + nameBase + "_" + bufferModel[2]])
        
        arcID = 0
        for bufferModelID in stepTrListID:
            globals()["e-ARC-SUP-" + nameBase + "_" + str(arcID)] = Arc("e-ARC-SUP-" + nameBase + "_" + str(arcID),bufferModelID[0], bufferModelID[1])
            arcID+=1
            globals()["e-ARC-SUP-" + nameBase + "_" + str(arcID)] = Arc("e-ARC-SUP-" + nameBase + "_" + str(arcID),bufferModelID[1], bufferModelID[2])
            arcID+=1
            
        print("stepTrListID:")
        print(stepTrListID)
    
    trimPN()    
    runPNMLWriter()

def trimPN():
    print("Trimming Petri Net")
    placesToRemove = []
    arcsToRemove = []
    
    #trim Spec places
    for place in Place.instances:
        if "Spec" in place.name:
            placesToRemove.append(place)
    
    for placeToRemove in placesToRemove:
        for arcToRemove in Arc.instances:
            if arcToRemove.source == placeToRemove.id:
                arcsToRemove.append(arcToRemove)
            if arcToRemove.target == placeToRemove.id:
                arcsToRemove.append(arcToRemove)
        Place.instances.remove(placeToRemove)
    
    for arcToRemove in arcsToRemove:
        Arc.instances.remove(arcToRemove)
    
    placesToRemove = []
    arcsToRemove = []
    
    for place in Place.instances:
        listTr = []#[[Tpre],[Tsuc]]
        listTPre = []
        listTSuc = []
        
        
        if "SUPCON" in place.name:
            listTPre = Arc.getTPre(place.id)
            listTSuc = Arc.getTSuc(place.id)
        listTr = [listTPre,listTSuc]
        #print(places.name)
        #print(listTr)

        for placesToCompare in Place.instances:
            listTrCompare = []
            listTPreCompare = []
            listTSucCompare = []
            if place.id != placesToCompare.id:
                listTPreCompare = Arc.getTPre(placesToCompare.id)
                listTSucCompare = Arc.getTSuc(placesToCompare.id)
            listTrCompare = [listTPreCompare,listTSucCompare]
            #print(placesToCompare.name)
            #print(listTrCompare)
            if (collections.Counter(listTr[0]) == collections.Counter(listTrCompare[0])) & (collections.Counter(listTr[1]) == collections.Counter(listTrCompare[1])) & (listTr != [[],[]]):
                print(place.name + " igual a " + placesToCompare.name)
                placesToRemove.append(place)
    
    for placeToRemove in placesToRemove:
        for arcToRemove in Arc.instances:
            if arcToRemove.source == placeToRemove.id:
                arcsToRemove.append(arcToRemove)
            if arcToRemove.target == placeToRemove.id:
                arcsToRemove.append(arcToRemove)
        Place.instances.remove(placeToRemove)
    
    for arcToRemove in arcsToRemove:
        Arc.instances.remove(arcToRemove)

if __name__ == "__main__":
    main()