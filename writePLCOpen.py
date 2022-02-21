from parsePNML_dev import ET, getET, Net, Page, Place, Transition, Arc, runPNMLParse

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
    
    
    
def definePOU():
    print("Defining POUs")
    

def writePLCOpen():
    print("Writing PLCopen file")



def main():
    
    definePOU()
    writePLCOpen()
    
if __name__ == "__main__":
    main()