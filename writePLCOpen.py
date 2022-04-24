import time
from parsePNML import ET, getET, Net, Page, Place, Transition, Arc, runPNMLParse
import xml.etree.ElementTree as POxml
import re

flowlist = []

class POU:

    objectId: str
    name: str
    lang: str

    instances: set
    instances = set()
    
    pouInstances = []
    listPOUName = []
    
    def __init__(self, oid):
        self.objectId = oid
        POU.pouInstances.append(self.objectId)
    
    def setPOUName(self, name):
        self.name = name
        POU.instances.add(self)
        POU.listPOUName.append(self.name)
        
          
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.obkectId)
            print('Name: ' + instance.name)
            
class Steps:
    
    POUname: str
    localID: str
    initialStep: str
    name: str
    
    
    
def defineFlows():
    print("Defining Flows")
    
    #The file must be inputed by user on app GUI
    #A pop-up must ask for the struct file
    file = open('pequenaFabricaInterpretada_wAUTONET-struct.txt')
    lines = file.readlines()
    file.close()
    for line in lines:
        print('line index:'+ str(lines.index(line)) + ' line:' + line)
    
    psemiflowindex = lines.index('P-SEMI-FLOWS GENERATING SET ------------------------------------- \n')
    tsemiflowindex = lines.index('T-SEMI-FLOWS GENERATING SET ------------------------------------- \n')
    print(str(lines.index('P-SEMI-FLOWS GENERATING SET ------------------------------------- \n')))
    print(str(lines.index('T-SEMI-FLOWS GENERATING SET ------------------------------------- \n')))
    
    flowslines = lines[psemiflowindex+4:tsemiflowindex-3]
    
    testflow = 'p0 p1 {p lugar} {p3 place} p4 (1)\n'
    
    flowslines.append(testflow)
    
    print(flowslines)
    
    
    for flows in flowslines:
        flows = re.sub('(\{)(.*?)\s(.*?)(\})', r'\2_\3', flows)
        flows = re.sub('\(.*?\n+', '', flows)
        flows = flows.strip()
        flowlist.append(flows.split(' '))
 
    print(flowlist)
    
    
def definePOUs():
    print('Defining POUs')
    
    
    
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
    for flow in flowlist:
        print(flow)
        pouInstance = POxml.SubElement(potask, "pouInstance", {"name":"flow"+str(flowcount),
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
    POxml.SubElement(POxml.SubElement(POxml.SubElement(globalVars, "variable", {"name":"tr0"}), "type"), "BOOL")
        
    
    adresource = POxml.SubElement(poresource, "addData")
    
    #for each sfc in flowlist + 1 sfc for transition declaration
    
    flowcount = 1
    for flow in flowlist:
        poudata = POxml.SubElement(adresource, "data", {"name":"http://www.3s-software.com/plcopenxml/pou",
                                                        "handleUnknown":"implementation"})
        
        pousfc = POxml.SubElement(poudata, "pou", {"name":"flow"+str(flowcount),
                                                                                      "pouType":"program"})
        
        pouinterface = POxml.SubElement(pousfc, "interface")
                        
        sfcbody = POxml.SubElement(POxml.SubElement(pousfc, "body"), "SFC")

        localid = 0
        
        for step in flow:
            sfcstep = POxml.SubElement(sfcbody, "step", {"localId":str(localid), "name":step})
            POxml.SubElement(sfcstep, "position", {"x":"0", "y":"0"})
            stepconnectionPointIn = POxml.SubElement(sfcstep, "connectionPointIn")
            #refLocalId in connectionPointIn points to previous transition
            connection = POxml.SubElement(stepconnectionPointIn, "connection", {"refLocalId":"2"})
            stepconnectionPointOut = POxml.SubElement(sfcstep, "connectionPointOut", {"formalParameter":"sfc"})
            POxml.SubElement(POxml.SubElement(POxml.SubElement(sfcstep, "addData"), "data",
                                              {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                               "handleUnknown":"implementation"}),
                             "attributes", {"xmlns":""})
            
        #inVariable are like arches in PN
        inVariables = [1,2]
        for inVariable in inVariables:
            invar = POxml.SubElement(sfcbody, "inVariable", {"localId":"4"})
            POxml.SubElement(invar, "position", {"x":"0", "y":"0"})
            invarconnectionPointOut = POxml.SubElement(invar, "connectionPointOut")
            POxml.SubElement(invar,"expression").text = "transitions.t0"
         
        transitions = [1,2]   
        for transition in transitions:
            sfctrans = POxml.SubElement(sfcbody, "transistion", {"localId":"5"})
            POxml.SubElement(sfctrans, "position", {"x":"0", "y":"0"})
            transconnectionPointIn = POxml.SubElement(sfctrans, "connectionPointIn")
            POxml.SubElement(transconnectionPointIn, "connection", {"refLocalId":"3", "formalParameter":"SFC"})
            transcondition = POxml.SubElement(sfctrans, "condition")
            POxml.SubElement(POxml.SubElement(transcondition, "connectionPointIn"), "connection",
                             {"refLocalId":"4"})
            POxml.SubElement(POxml.SubElement(POxml.SubElement(sfctrans, "addData"), "data",
                                              {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                               "handleUnknown":"implementation"}),
                             "attributes", {"xmlns":""})
            
        jumpsteps = [1,2]
        for jumstep in jumpsteps:
            sfcjump = POxml.SubElement(sfcbody, "jumpStep", {"localId":"6", "targetName":"p0"})
            POxml.SubElement(sfcjump, "position", {"x":"0", "y":"0"})
            POxml.SubElement(POxml.SubElement(sfcjump, "connectionPointIn"), "connection",
                             {"refLocalId":"5"})  
            POxml.SubElement(POxml.SubElement(POxml.SubElement(sfcjump, "addData"), "data",
                                              {"name":"http://www.3s-software.com/plcopenxml/sfc/element",
                                               "handleUnknown":"implementation"}),
                             "attributes", {"xmlns":""})
            
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
               
                
        
        
            
    POxml.indent(plcopen, " ", 0)
    ET.ElementTree(plcopen).write("PLCopen_writer.xml")

    

def main():
    
    defineFlows()
    definePOUs()
    writePLCOpen()
    
if __name__ == "__main__":
    main()