from telnetlib import theNULL
from threading import local
import time
from tokenize import String
from parsePNML import ET, getET, Net, Page, Place, Transition, Arc, parsePNML, runPNMLParse
import xml.etree.ElementTree as POxml
import re

flowlist = []

class POU:

    objectId: str
    name: str
    lang: str
    
    #flowSequence : []
    trSequence = []
    instances: set
    instances = set()
    
    pouInstances = []
    listPOUName = []
    
    def __init__(self, name):
        self.name = name
        self.stepSequence = []
        self.transitionSequence = []
        self.flowSequence = []
        self.flowElements = []
        POU.pouInstances.append(self.name)
        POU.instances.add(self)
    
    def setPOUName(self, name):
        self.name = name
        
        POU.listPOUName.append(self.name)
    
    def setStepSequence(self, placeSeq):
        self.stepSequence = placeSeq
    
    def setTrSequence(self, trseq):
        self.transitionSequence = trseq
    
    def setFlowSequence(self, flowseq):
        self.flowSequence = flowseq
    
    def setFlowElements(self, flowelem):
        self.flowElements = flowelem
    
          
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.objectId)
            print('Name: ' + instance.name)
            
class Steps:
    
    POUname: str
    id: str
    localID: str
    initialStep: str
    name: str
    connectionPointInRefId: str
    
    transitions: list
    
    instances: set
    instances = set()
    
    stepsInstances = []
    listStepsName = []
    
    
    def __init__(self, id):
        self.id = id
        Steps.instances.add(self)
        Steps.stepsInstances.append(self.id)
    
    def setStepsName(self, name):
        self.name = name
        #Steps.instances.add(self)
        Steps.listStepsName.append(self.name)
        
    def setStepsPOU(self, pou):
        self.POUname = pou
        
    def setStepsInitialMark(self, initialStep):
        self.initialStep = initialStep

    def setStepsLocalID(self, localID):
        self.localID = localID
        
    def setStepsConnPointIn(self, connPointIn):
        self.connectionPointInRefId = connPointIn
    
    @classmethod
    def getStepLocalID(cls, id):
        for instance in cls.instances:
            if instance.id == id:
                return instance.localID
            
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.id)
            print('Name: ' + instance.name)
            print('InitialStep: ' + instance.initialStep)
            print("LocalID:" + instance.localID)
            

class SFCtransition:
    
    POUname: str
    name: str
    localID: str
    connectionPointInRefId: str
    condition: str
    
    instances: set
    instances = set()

    def __init__(self, name):
        self.name = name
        self.instances.add(self)
    
    def setPOUname(self, pouname):
        self.POUname = pouname
        
    def setLocalID(self, localID):
        self.localID = localID
        
    def setConnPointIn(self, connPointIn):
        self.connectionPointInRefId = connPointIn
        
    def setCondition(self, condition):
        self.condition = condition
        
        
class InVariable:
    
    POUname: str
    localID: str
    name: str
    expression: str
    
    def __init__(self, name):
        self.name = name
    
    def setPOUname(self, pouname):
        self.POUname = pouname
        
    def setLocalID(self, localID):
        self.localID = localID
        
    def setExpression(self, expression):
        self.expression = expression
    
class SelectDiverg:
    
    POUname: str
    name: str
    localID: str
    connectionPointInRefId: str
    connectionPointOutQty: int
    
    def __init__(self, name):
        self.name = name
    
    def setPOUname(self, pouname):
        self.POUname = pouname
        
    def setLocalID(self, localID):
        self.localID = localID
               
    def setConnPointIn(self, connPointIn):
        self.connectionPointInRefId = connPointIn
        
    def setConnPointOutQty(self, connOutQty):
        self.connectionPointOutQty = connOutQty
    
class SelectConverg:
    
    name: str
    POUname: str
    localID: str
    connectionPointInRefId: str
    connectionPointOutRefId: str
    
    def __init__(self, name):
        self.name = name
        self.connPointIn = []
        
    def setPOUname(self, pouname):
        self.POUname = pouname
        
    def setLocalID(self, localID):
        self.localID = localID
        
    def setConnPointIn(self, connPointIn):
        self.connPointIn.append(connPointIn)
      
class JumpStep:
    
    name: str
    POUname: str
    localID: str
    connectionPointInRefId: str
    targetName: str
    
    def __init__(self, name):
        self.name = name
        
    def setPOUname(self, pouname):
        self.POUname = pouname
        
    def setLocalID(self, localID):
        self.localID = localID
        
    def setConnPointIn(self, connPointIn):
        self.connectionPointInRefId = connPointIn

    def setTargetName(self, targetName):
        self.targetName = targetName
        
def tlookup(p1, p2):
    print("tlookup")
    p1id = Place.getID(p1)
    p2id = Place.getID(p2)
    p1trlist = []
    p2trlist = []
    arcp1list = []
    arcp2list = []
    trlist = []
    
    p1trlist = Arc.getTSuc(p1id)
    p2trlist = Arc.getTPre(p2id)    
    
    print("getTsuc: " + p1)
    print(p1trlist)
    print("getTpre: " + p2)
    print(p2trlist)
    
    for p1tr in p1trlist:
        for p2tr in p2trlist:
            if p1tr == p2tr:
                trlist.append(p1tr)
    
    return trlist
    
    
def defineFlows():
    print("Defining Flows")
    
    #The file must be inputed by user on app GUI
    #A pop-up must ask for the struct file
    file = open('WRITER-struct.txt')
    lines = file.readlines()
    file.close()
    #for line in lines:
    #    print('line index:'+ str(lines.index(line)) + ' line:' + line)
    
    psemiflowindex = lines.index('P-SEMI-FLOWS GENERATING SET ------------------------------------- \n')
    tsemiflowindex = lines.index('T-SEMI-FLOWS GENERATING SET ------------------------------------- \n')
    print(str(lines.index('P-SEMI-FLOWS GENERATING SET ------------------------------------- \n')))
    print(str(lines.index('T-SEMI-FLOWS GENERATING SET ------------------------------------- \n')))
    
    flowslines = lines[psemiflowindex+4:tsemiflowindex-3]
    
    #testflow = 'p0 p1 {p lugar} {p3 place} p4 (1)\n'
    
    #flowslines.append(testflow)
    
    print(flowslines)
    
    
    for flows in flowslines:
               
        flows = re.sub('(\{)(.*?)\s(.*?)(\})', r'\2_\3', flows)
        flows = re.sub('\(.*?\n+', '', flows)
        flows = flows.strip()
        flowlist.append(flows.split(' '))
        
        

        
    print("Flowlist: " + str(flowlist))
    
    
def definePOUs():
    print('Defining POUs')
    #print(flowlist)
    
    flowscount = 1
    
    for flow in flowlist:
        
        print("------------------------ Flow Specs Detection -----------------------------")
        for places in flow:
            if places.startswith("Spec"):
                print(places)
                if flow.index(places) == len(flow)-1:
                    print("Ultimo Spec")
                    specflow = re.findall("(.*)_", places)[0]
                    print(specflow)
                    pouname = specflow
            else:
                print("Not Spec")
                pouname = "flow_" + str(flowscount)
                break
                
        #pouname = "flow_" + str(flowscount)
        print('POU Name:')
        print(pouname)
        print("Places in " + pouname)
        print(flow)
        globals()[pouname] = POU(pouname)
        flowAux = flow.copy()
        placeSequence = []
        flowSequence = []
        trSequence = []
        
        for place in flow:
            print("place: " + str(place))
            print("initialMark of " + place + " is " + Place.getInitialMark(place))
            #define steps
            placeId = pouname + "_" + place
            globals()[placeId] = Steps(placeId)
            globals()[placeId].setStepsPOU(pouname)
            globals()[placeId].setStepsName(place)
            globals()[placeId].setStepsInitialMark(Place.getInitialMark(place))
            if Place.getInitialMark(place) == "1":
               placeSequence.append(place)
               flowAux.remove(place)
            
                        
            #define invariables
        print("teste: " + str(flow))
        #define Transitions
        trlist = []
        placeIndex = 0
        seq = 0
        print("printFlow:" + str(flow))
        
        while len(flowAux) > 0:
            print("flowAux: " + str(flowAux))
            print("seq: " + str(seq))
            trlist = tlookup(placeSequence[placeIndex], flowAux[seq])
            print("trlist:")
            print(trlist)
            if len(trlist) > 0:
                placeSequence.append(flowAux[seq])
                flowAux.remove(flowAux[seq])
                trSequence.append(trlist)
                seq = 0
                placeIndex+=1
            else:
                seq+=1
        trlist = tlookup(placeSequence[len(placeSequence)-1], placeSequence[0])
        trSequence.append(trlist)
        globals()[pouname].setStepSequence(placeSequence)
        globals()[pouname].setTrSequence(trSequence)
        
        for i in range(len(placeSequence)):
            flowSequence.append(placeSequence[i])
            flowSequence.append(trSequence[i])
        
        globals()[pouname].setFlowSequence(flowSequence)
        
        print("Original Flow: ")
        print(flow)
        print("Place Sequence: " + str(placeSequence))
        print("Tr Sequence: " + str(trSequence))
        print("Flow Sequence: " + str(flowSequence))
        
        #Complete Steps definition and ...
        #Selection Divergences, InVariables, Transitions, Selection Convergences and Jump Steps
        flowElements = []
        
        isStep = True
        localID = 0
        print("~~~~~~~~~~DEFINING ELEMENTS~~~~~~~~~~")
        for elements in flowSequence:
            print("isStep:" + str(isStep)) 
            if isStep:
                if flowSequence.index(elements) == 0:
                    print("Defining Initial Step")
                    placeId = pouname + "_" + elements
                    #print("POU name: " + pouname)
                    #print("Element Name: " + elements)
                    #print("-----------------------: " + placeId)
                    #print("localID: " + str(localID))
                    globals()[placeId].setStepsLocalID(str(localID))
                    flowElements.append("initialStep_(" + placeId + ")" + "_ID_" + str(localID))
                    #print(Steps.getStepLocalID(placeId))
                    localID = localID + 1
                else:
                    print("Defining Normal Step")
                    
                    placeId = pouname + "_" + elements
                    #print("POU name: " + pouname)
                    #print("Element Name: " + elements)
                    #print("-----------------------: " + placeId)
                    #print("localID: " + str(localID))
                    globals()[placeId].setStepsLocalID(str(localID))
                    globals()[placeId].setStepsConnPointIn(str(localID-1))
                    flowElements.append("Step_(" + placeId + ")" + "_ID_" + str(localID))
                    #print(Steps.getStepLocalID(placeId))
                    localID = localID + 1
            else:
                if len(elements) > 1:
                    print("Transition in parallel detected")
                    #More than 1 transition needs a select Divergence to make it parallel
                    print(elements)
                    selDivName = pouname + "_selectDiverg_" + str(flowSequence.index(elements))
                    flowElements.append("SelectDiverg_("+selDivName+")_ID_"+str(localID))
                    globals()[selDivName] = SelectDiverg(selDivName)
                    globals()[selDivName].setPOUname(pouname)
                    globals()[selDivName].setLocalID(str(localID))
                    globals()[selDivName].setConnPointIn(str(localID-1))
                    globals()[selDivName].setConnPointOutQty(len(elements))
                    
                    localID = localID + 1
                    
                    for transition in elements:
                        print("Defining transitions in parallel")
                        #InVariables
                        inVarName = pouname + "_inVar_" + str(localID)
                        globals()[inVarName] = InVariable(inVarName)
                        globals()[inVarName].setPOUname(pouname)
                        globals()[inVarName].setLocalID(str(localID))
                        globals()[inVarName].setExpression("transitions." + Transition.getName(transition))
                        flowElements.append("inVar_(" + inVarName + ")_ID_" + str(localID))
                        
                        
                        localID = localID + 1
                        
                        trname = pouname + "_" + Transition.getName(transition) + "_" + str(flowSequence.index(elements))
                        flowElements.append("transition_(" + trname + ")_ID_" + str(localID))
                        globals()[trname] = SFCtransition(trname)
                        globals()[trname].setPOUname(pouname)
                        globals()[trname].setLocalID(str(localID))
                        globals()[trname].setConnPointIn(globals()[selDivName].localID)
                        globals()[trname].setCondition(str(localID-1))
                        
                        localID = localID + 1
                        
                    #Defining Select Convergence
                    selConvName = pouname + "_selectConverg_" + str(flowSequence.index(elements))
                    flowElements.append("SelectConverg_("+ selConvName+")_ID_"+str(localID))
                    globals()[selConvName] = SelectConverg(selConvName)
                    globals()[selConvName].setPOUname(pouname)
                    globals()[selConvName].setLocalID(str(localID))
                    for transition in elements:
                        trname = pouname + "_" + Transition.getName(transition) + "_" + str(flowSequence.index(elements))
                        globals()[selConvName].setConnPointIn(trname)
                    localID = localID + 1
                
                else:
                    transition = elements[0]
                    print("Defining simple transitions")
                    #InVariables
                    inVarName = pouname + "_inVar_" + str(localID)
                    globals()[inVarName] = InVariable(inVarName)
                    globals()[inVarName].setPOUname(pouname)
                    globals()[inVarName].setLocalID(str(localID))
                    globals()[inVarName].setExpression("transitions." + Transition.getName(transition))
                    flowElements.append("inVar_(" + inVarName + ")_ID_" + str(localID))
                    
                    
                    localID = localID + 1
                    
                    trname = pouname + "_" + Transition.getName(transition) + "_" + str(flowSequence.index(elements))
                    flowElements.append("transition_(" + trname + ")_ID_" + str(localID))
                    globals()[trname] = SFCtransition(trname)
                    globals()[trname].setPOUname(pouname)
                    globals()[trname].setLocalID(str(localID))
                    globals()[trname].setConnPointIn(str(localID-2))
                    globals()[trname].setCondition(str(localID-1))
                    
                    localID = localID + 1
                    
                    
            if isStep:
                isStep = False
            else:
                isStep = True
        
        #Defining jumStep
        jumpStepName = pouname + "_jumpStep"
        flowElements.append("jumpStep_("+ jumpStepName+")_ID_"+str(localID))
        globals()[jumpStepName] = JumpStep(jumpStepName)
        globals()[jumpStepName].setPOUname(pouname)
        globals()[jumpStepName].setLocalID(str(localID))
        globals()[jumpStepName].setConnPointIn(str(localID-1))
        globals()[jumpStepName].setTargetName(flowSequence[0])
        
                    
        globals()[pouname].setFlowElements(flowElements)   
            

        
        flowscount+=1
    
    #print("Print Steps")
    #Steps.print_instances()
        
    #arcos = Arc.getTPre(Place.getID(flowlist[0][0]))
    #transicao = Transition.getName(arcos[0])
    #print(arcos[0] + ":" + transicao)
    #trlist = tlookup(flowlist[0][0],flowlist[0][1])
    #print(trlist)
    
    
def writePLCOpen():
    print("Writing PLCopen file")

    plcopen = POxml.Element("project",{"xmlns":"http://www.plcopen.org/xml/tc6_0200"})
    POxml.register_namespace('',"http://www.plcopen.org/xml/tc6_0200")
    
    
    creationDateTime = time.strftime("%Y-%m-%dT%H:%m:%S",time.localtime())
    
    fileHeader = POxml.SubElement(plcopen,"fileHeader", 
                                  {"companyName":"PN2IC", "productName":"PLCopen", 
                                   "productVersion":"CODESYS V3.5 SP17 Patch 3", 
                                   "creationDateTime":creationDateTime})
    
    contentHeader = POxml.SubElement(plcopen, "contentHeader",
                                     {"name":"CodesysTest.project", "modificationDateTime":creationDateTime})
    
    coordinateInfo = POxml.SubElement(contentHeader, "coordinateInfo")
    
    scalingfdb = POxml.SubElement(POxml.SubElement(coordinateInfo,"fbd"), "scaling", {"x":"1", "y":"1"})
    scalingld = POxml.SubElement(POxml.SubElement(coordinateInfo,"ld"), "scaling", {"x":"1", "y":"1"})
    scalingsfc = POxml.SubElement(POxml.SubElement(coordinateInfo,"sfc"), "scaling", {"x":"1", "y":"1"})
    
    aDcontentHeader = POxml.SubElement(contentHeader,"addData")
    datacontentHeader = POxml.SubElement(aDcontentHeader,"data",{"name":"http://www.3s-software.com/plcopenxml/projectinformation",
                                                                 "handleUnknown":"implementation"})
    picontentHeader = POxml.SubElement(datacontentHeader,"ProjectInformation")
    
    potypes = POxml.SubElement(plcopen, "types")
    POxml.SubElement(potypes, "dataTypes")
    POxml.SubElement(potypes, "pous")
    
    poinstances = POxml.SubElement(plcopen, "instances")
    POxml.SubElement(poinstances, "configurations")
    
    poaddData = POxml.SubElement(plcopen, "addData")
    podata = POxml.SubElement(poaddData, "data", {"name":"http://www.3s-software.com/plcopenxml/application",
                                                  "handleUnknown":"implementation"})
    poresource = POxml.SubElement(podata, "resource", {"name":"Application"})
    potask = POxml.SubElement(poresource, "task",{"name":"MainTask", "interval":"PT0.02S", "priority":"1"})
    
    flowcount = 1
    for flow in POU.instances:
        #print(flow.name)
        pouInstance = POxml.SubElement(potask, "pouInstance", {"name": flow.name,
                                                               "typeName":""})
        POxml.SubElement(POxml.SubElement(pouInstance, "documentation"),
                         "xhtml", {"xmlns":"http://www.w3.org/1999/xhtml"})
        
        flowcount = flowcount + 1
        
    adtask = POxml.SubElement(potask, "addData")
    datatask = POxml.SubElement(adtask, "data", {"name":"http://www.3s-software.com/plcopenxml/tasksettings",
                                                 "handleUnknown":"implementation"})
    tasksettings = POxml.SubElement(datatask, "TaskSettings", {"KindOfTask":"Cyclic",
                                                "Interval":"t#100ms", "IntervalUnit":"ms",
                                                "WithinSPSTimeSlicing":"true"})
    
    globalVars = POxml.SubElement(poresource, "globalVars", {"name":"GVL"})
    
    #for transition in transition.instances:
    for transition in Transition.instances:
        POxml.SubElement(POxml.SubElement(POxml.SubElement(globalVars, "variable", {"name":transition.name}), "type"), "BOOL")
        
    
    adresource = POxml.SubElement(poresource, "addData")
    
    #for each sfc in flowlist + 1 sfc for transition declaration
    
    flowcount = 1
    for flow in POU.instances:
        print("Writing flow:" + flow.name)
        poudata = POxml.SubElement(adresource, "data", {"name":"http://www.3s-software.com/plcopenxml/pou",
                                                        "handleUnknown":"implementation"})
        
        pousfc = POxml.SubElement(poudata, "pou", {"name":flow.name,"pouType":"program"})
        
        pouinterface = POxml.SubElement(pousfc, "interface")
                        
        sfcbody = POxml.SubElement(POxml.SubElement(pousfc, "body"), "SFC")

        localid = 0
        print("Flow elements:")
        print(flow.flowElements)
        
        for element in flow.flowElements:
            print("Elements: " + element)
            
            if element.startswith("initialStep"):
                #Write initialStep
                print("Writing initialStep")
                stepID = re.findall("\((.*?)\)", element)[0]
                print(stepID)
                stepName = globals()[stepID].name
                localID = globals()[stepID].localID
                print(stepName)
                
                sfcstep = POxml.SubElement(sfcbody, "step", {"localId":localID, "initialStep": "true", "name":stepName})
                POxml.SubElement(sfcstep, "position", {"x":"0", "y":"0"})
                stepconnectionPointIn = POxml.SubElement(sfcstep, "connectionPointIn")
                #refLocalId in connectionPointIn points to previous transition
                #connection = POxml.SubElement(stepconnectionPointIn, "connection", {"refLocalId":"2"})
                stepconnectionPointOut = POxml.SubElement(sfcstep, "connectionPointOut", {"formalParameter":"sfc"})
                POxml.SubElement(POxml.SubElement(POxml.SubElement(sfcstep, "addData"), "data",
                                                {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                                "handleUnknown":"implementation"}),
                                "attributes", {"xmlns":""})
                
            elif element.startswith("Step"):
                #Write Step
                print("Writing Step")
                stepID = re.findall("\((.*?)\)", element)[0]
                print(stepID)
                stepName = globals()[stepID].name
                localID = globals()[stepID].localID
                refLocalId = globals()[stepID].connectionPointInRefId
                
                print(stepName)
                
                sfcstep = POxml.SubElement(sfcbody, "step", {"localId":localID, "name":stepName})
                POxml.SubElement(sfcstep, "position", {"x":"0", "y":"0"})
                stepconnectionPointIn = POxml.SubElement(sfcstep, "connectionPointIn")
                #refLocalId in connectionPointIn points to previous transition
                connection = POxml.SubElement(stepconnectionPointIn, "connection", {"refLocalId":refLocalId})
                stepconnectionPointOut = POxml.SubElement(sfcstep, "connectionPointOut", {"formalParameter":"sfc"})
                POxml.SubElement(POxml.SubElement(POxml.SubElement(sfcstep, "addData"), "data",
                                                {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                                "handleUnknown":"implementation"}),
                                "attributes", {"xmlns":""})
                
            elif element.startswith("SelectDiverg"):
                #Write SelectDiverg
                print("Writing SelectDiverg")
                selDivID = re.findall("\((.*?)\)", element)[0]
                print(selDivID)
                selDivName = globals()[selDivID].name
                localID = globals()[selDivID].localID
                refLocalId = globals()[selDivID].connectionPointInRefId
                connOutQty = globals()[selDivID].connectionPointOutQty
                print(selDivName)
                
                selDiv = POxml.SubElement(sfcbody,"selectionDivergence", {"localId":localID})
                POxml.SubElement(selDiv, "position", {"x":"0", "y":"0"})
                selDivconnectionPointIn = POxml.SubElement(selDiv, "connectionPointIn")
                #refLocalId in connectionPointIn points to previous step
                POxml.SubElement(selDivconnectionPointIn, "connection", {"refLocalId":refLocalId})
                #Repeat connectionPointOut for each transition in parallel
                for connOut in range(connOutQty):
                    POxml.SubElement(selDiv, "connectionPointOut", {"formalParameter":"sfc"})
                
                POxml.SubElement(POxml.SubElement(POxml.SubElement(selDiv, "addData"), "data",
                                                    {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                                    "handleUnknown":"implementation"}),
                                    "attributes", {"xmlns":""})
        
        
            elif element.startswith("inVar"):
                #Write inVar
                print("Writing inVar")
                inVarID = re.findall("\((.*?)\)", element)[0]
                print(inVarID)
                inVarName = globals()[inVarID].name
                localID = globals()[inVarID].localID
                expression = globals()[inVarID].expression
                print(inVarName)
                
                print("Writing inVar")
                invar = POxml.SubElement(sfcbody, "inVariable", {"localId":localID})
                POxml.SubElement(invar, "position", {"x":"0", "y":"0"})
                invarconnectionPointOut = POxml.SubElement(invar, "connectionPointOut")
                POxml.SubElement(invar,"expression").text = expression
            
            elif element.startswith("transition"):
                #Write transition
                print("Writing transition")
                transitionID = re.findall("\((.*?)\)", element)[0]
                print(transitionID)
                trName = globals()[transitionID].name
                localID = globals()[transitionID].localID
                refLocalId = globals()[transitionID].connectionPointInRefId
                condition = globals()[transitionID].condition
                print(trName)
                
                sfctrans = POxml.SubElement(sfcbody, "transition", {"localId":localID})
                POxml.SubElement(sfctrans, "position", {"x":"0", "y":"0"})
                transconnectionPointIn = POxml.SubElement(sfctrans, "connectionPointIn")
                POxml.SubElement(transconnectionPointIn, "connection", {"refLocalId":refLocalId, "formalParameter":"SFC"})
                transcondition = POxml.SubElement(sfctrans, "condition")
                POxml.SubElement(POxml.SubElement(transcondition, "connectionPointIn"), "connection",
                                {"refLocalId":condition})
                POxml.SubElement(POxml.SubElement(POxml.SubElement(sfctrans, "addData"), "data",
                                                {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                                "handleUnknown":"implementation"}),
                                "attributes", {"xmlns":""})
            
            elif element.startswith("SelectConverg"):
                #Write SelectConverg
                print("Writing SelectConverg")
                selConvID = re.findall("\((.*?)\)", element)[0]
                print(selConvID)
                selConvName = globals()[selConvID].name
                localID = globals()[selConvID].localID
                connInList = globals()[selConvID].connPointIn
                print(connInList)
                print(selConvName)
                
                selConv = POxml.SubElement(sfcbody,"selectionConvergence", {"localId":localID})
                POxml.SubElement(selConv, "position", {"x":"0", "y":"0"})
                for connTr in connInList:
                    refLocalId = globals()[connTr].localID
                    #Loop connectionPointIn for each transition in parallel
                    selConvconnectionPointIn = POxml.SubElement(selConv, "connectionPointIn")
                    #refLocalId in connectionPointIn points to previous transition
                    POxml.SubElement(selConvconnectionPointIn, "connection", {"refLocalId":refLocalId})
                
                POxml.SubElement(selConv, "connectionPointOut", {"formalParameter":"sfc"})
        
            elif element.startswith("jumpStep"):
                #Write jumpStep
                print("Writing jumpStep")
                jumpStepID = re.findall("\((.*?)\)", element)[0]
                print(transitionID)
                jumpName = globals()[jumpStepID].name
                localID = globals()[jumpStepID].localID
                refLocalId = globals()[jumpStepID].connectionPointInRefId
                targetName = globals()[jumpStepID].targetName
                
                print(jumpName)
                
                sfcjump = POxml.SubElement(sfcbody, "jumpStep", {"localId":localID, "targetName":targetName})
                POxml.SubElement(sfcjump, "position", {"x":"0", "y":"0"})
                POxml.SubElement(POxml.SubElement(sfcjump, "connectionPointIn"), "connection",
                                {"refLocalId":refLocalId})  
                POxml.SubElement(POxml.SubElement(POxml.SubElement(sfcjump, "addData"), "data",
                                                {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                                "handleUnknown":"implementation"}),
                                "attributes", {"xmlns":""})
            
            else:
                print("Element Invalid!")
        
            
        #Settings of POU
        sfcsettings = POxml.SubElement(POxml.SubElement(POxml.SubElement(pousfc, "addData"), "data",
        {"name":"http://www.3s-software.com/plcopenxml/sfcsettings", "handleUnknown":"implementation"}),
        "SFCSettings")
        
        POxml.SubElement(sfcsettings, "CalcActiveTramsOnly").text = "false"
        POxml.SubElement(sfcsettings, "UseDefaults").text = "false"
        sfcsetflags = POxml.SubElement(sfcsettings, "Flags")
        POxml.SubElement(sfcsetflags, "EnableLimit", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Init", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Reset", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "QuitError", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Pause", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Error", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Trans", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "ErrorStep", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "ErrorPOU", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "CurrentStep", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "Tip", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "TipMode", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "MaxFlags", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "SFCErrorAnalyzation", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "SFCErrorAnalyzationTable", {"Declare":"true", "Use":"false"})
        POxml.SubElement(sfcsetflags, "CurrentSteps", {"Declare":"true", "Use":"false"})
        
     #POU Transition          
    datatrans = POxml.SubElement(adresource, "data", {"name":"http://www.3s-software.com/plcopenxml/pou",
                                                        "handleUnknown":"implementation"})
    poutrans = POxml.SubElement(datatrans, "pou", {"name":"transitions", "pouType":"program"})
        
    POxml.SubElement(poutrans, "interface")            
    
    trans = POxml.SubElement(poutrans, "transitions")
    
    #transitions = [1,1]
    for tr in Transition.instances:
        
        decList = []
        #print(tr.name)
        print(Arc.getTPre(tr.id))
        for pSpec in Arc.getTPre(tr.id):
            specif = re.findall("p-(.*)", pSpec)[0]
            print("Specification:")
            print(specif)
            if specif.startswith("Spec"):
                specif2 = re.findall("(.*)_", specif)[0]
                decList.append(" AND " + specif2 + "." + specif + ".x")
            print("End specification")
        
        transitionName = tr.name
        transitionDeclaration = transitionName
        for decla in decList:
            transitionDeclaration = transitionDeclaration + decla
            
        print("Declaration:" + transitionDeclaration)                    
        
        transst = POxml.SubElement(POxml.SubElement(POxml.SubElement(trans, "transition",{"name":transitionName}),
                                                           "body"), "ST")
        #trigger of in ST of transitions
        POxml.SubElement(transst, "xhtml",{"xmlns":"http://www.w3.org/1999/xhtml"}).text = "GVL." + transitionDeclaration
    
    POxml.SubElement(POxml.SubElement(POxml.SubElement(poutrans, "body"), "ST"), "xhtml",
    {"xmlns":"http://www.w3.org/1999/xhtml"})
    
    
    
    
    
    
    
    
    POxml.indent(plcopen, " ", 0)
    ET.ElementTree(plcopen).write("PLCopen_writer.xml")

    

def main():
    
    writerpnml = open("WRITER.pnml")
    parsePNML(writerpnml)
    defineFlows()
    definePOUs()
    writePLCOpen()
    
    #print("Checking POUs:")
    #print("Total Number of POUs:")
    #print(len(POU.instances))
    '''
    for pous in POU.instances:
        print("POU Name:")
        print(pous.name)
        print("Step Sequence:")
        print(pous.stepSequence)
        print("Tr Sequence:")
        print(pous.transitionSequence)
        print("Flow Sequence:")
        print(pous.flowSequence)
        print("Flow Elements:")
        print(pous.flowElements)        
    '''
    
    #Steps.print_instances()
    
    
if __name__ == "__main__":
    main()