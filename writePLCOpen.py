from parsePNML import ET, getET, Net, Page, Place, Transition, Arc, runPNMLParse
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
        

def writePLCOpen():
    print("Writing PLCopen file")



def main():
    
    defineFlows()
    writePLCOpen()
    
if __name__ == "__main__":
    main()