from parsePNML import ET, getET, Net, Page, Place, Transition, Arc
import re
import os

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
        
    Transition.getID(name)




if __name__ == "__main__":
    main()