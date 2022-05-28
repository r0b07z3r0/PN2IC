import csv
from typing import Text
import xml.etree.ElementTree as ET

tree = ET

class Net:
    
    id: str
    type: str
    name: str
    instances: set
    instances = set()
    listNetName = []
    
    def __init__(self,attrib):
        self.id = attrib['id']
        self.type = attrib['type']
        Net.instances.add(self)
        
    def setNetName(self, name):
        self.name = name
        Net.instances.add(self)
        Net.listNetName.append(self.name)
        
    @classmethod
    def listNet(cls):
        return Net.listNetName
    
    @classmethod
    def getID(cls, name):
        for instance in cls.instances:
            if instance.name == name:
                return instance.id
    
    @classmethod
    def getType(cls, name):
        for instance in cls.instances:
            if instance.name == name:
                return instance.type
    
    @classmethod
    def getName(cls, id):
        for instance in cls.instances:
            if instance.id == id:
                return instance.name
        
class Page:
    
    id: str
    instances: set
    instances = set()
    listPageID = []
    def __init__(self,id):
        self.id = id
        Page.instances.add(self)
        Page.listPageID.append(id)
        
    @classmethod
    def listPage(cls):
        return Page.listPageID
    

class Place:

    id: str
    name: str
    name_graph_x: str
    name_graph_y: str
    label: str
    label_graph_x: str
    label_graph_y: str
    initial_mark: str
    hasinitialmark: bool
    position_x: str
    position_y: str

    instances: set

    instances = set()
    placesInstances = []
    listPlaceName = []
    
    def __init__(self, id):
        self.id = id
        Place.placesInstances.append(self.id)
    
    def setPlaceName(self, name):
        self.name = name
        Place.instances.add(self)
        Place.listPlaceName.append(self.name)
        
    def setPlaceNameGraph(self, x, y):
        self.name_graph_x = x
        self.name_graph_y = y
        Place.instances.add(self)
        
    def setPlaceLabel(self, label):
        self.label = label
        Place.instances.add(self)
        
    def setPlaceLabelGraph(self, x, y):
        self.label_graph_x = x
        self.label_graph_y = y
        Place.instances.add(self)
        
    def setInitialMark(self, initial_mark):
        self.initial_mark = initial_mark
        if int(initial_mark) > 0:
            self.hasinitialmark  = True
        else:
            self.hasinitialmark = False
        Place.instances.add(self)
        
    def setPlacePos(self, x, y):
        self.position_x = x
        self.position_y = y
        Place.instances.add(self)
        
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.id)
            print('Name: ' + instance.name)
            print('Name Graph: ' + instance.name_graph_x + " , " + instance.name_graph_y)
            print('Label: ' + instance.label)
            print('Label Graph: ' + instance.label_graph_x + " , " + instance.label_graph_y)
            print('Initial Mark: ' + instance.initial_mark)
            print('Has Initial Mark: ' + str(instance.hasinitialmark))
            print('Place Pos: ' + instance.position_x + " , " + instance.position_y)

    @classmethod
    def listPlace(cls):
        return Place.listPlaceName
    
    @classmethod
    def getID(cls, name):
        for instance in cls.instances:
            if instance.name == name:
                return instance.id
    
    @classmethod
    def getName(cls, id):
        for instance in cls.instances:
            if instance.id == id:
                return instance.name
    
    @classmethod
    def getInitialMark(cls, name):
        for instance in cls.instances:
            #print(instance.name)
            if instance.name == name:
                return instance.initial_mark       

class Transition:

    id: str
    name: str
    name_graph_x: str
    name_graph_y: str
    label: str
    label_graph_x: str
    label_graph_y: str
    position_x: str
    position_y: str

    instances: set

    instances = set()
    transitionInstances = []
    
    def __init__(self, id):
        self.id = id.attrib['id']
        Transition.transitionInstances.append(self.id)
    
    def setTransitionName(self, name):
        self.name = name
        Transition.instances.add(self)
        
    def setTransitionNameGraph(self, name_graph):
        self.name_graph_x = name_graph.attrib['x']
        self.name_graph_y = name_graph.attrib['y']
        Transition.instances.add(self)
        
    def setTransitionLabel(self, label):
        self.label = label
        Transition.instances.add(self)
        
    def setTransitionLabelGraph(self, label_graph):
        self.label_graph_x = label_graph['x']
        self.label_graph_y = label_graph['y']
        Transition.instances.add(self)
        
    def setTransitionPos(self, transition_pos):
        self.position_x = transition_pos.attrib['x']
        self.position_y = transition_pos.attrib['y']
        Transition.instances.add(self)
        
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.id)
            print('Name: ' + instance.name)
            print('Name Graph: ' + instance.name_graph_x + " , " + instance.name_graph_y)
            print('Label: ' + instance.label)
            print('Label Graph: ' + instance.label_graph_x + " , " + instance.label_graph_y)
            print('Transition Pos: ' + instance.position_x + " , " + instance.position_y)

    @classmethod
    def getName(cls, id):
        for instance in cls.instances:
            if instance.id == id:
                return instance.name
class Arc:
    
    id: str
    source: str
    hasPlaceAsSource: bool
    hasTransitionAsSource: bool
    target: str
    hasPlaceAsTarget: bool
    hasTransitionAsTarget: bool
    position1_x: str
    position1_y: str
    position2_x: str
    position2_y: str
    
    instances: set

    instances = set()
    arcInstances = []
    
    def __init__(self, id, source, target):
        self.id = id
        self.source = source
        self.target = target
        if source[0] == 'p':
            self.hasPlaceAsSource = True
            self.hasTransitionAsSource = False
        else:
            self.hasPlaceAsSource = False
            self.hasTransitionAsSource = True
            
        if target[0] == 'p':
            self.hasPlaceAsTarget = True
            self.hasTransitionAsTarget = False
        else:
            self.hasPlaceAsTarget = False
            self.hasTransitionAsTarget = True
            
        Arc.arcInstances.append(self.id)
        Arc.instances.add(self)
    
        
    @classmethod
    def print_instances(cls):
        for instance in cls.instances:
            print('ID: ' + instance.id)
            print('Source: ' + instance.source)
            print('Has Place as Source: ' + str(instance.hasPlaceAsSource))
            print('Has Transition as Source: ' + str(instance.hasTransitionAsSource))
            print('Target: ' + instance.target)
            print('Has Place as Target: ' + str(instance.hasPlaceAsTarget))
            print('Has Transition as Target: ' + str(instance.hasTransitionAsTarget))

    @classmethod
    def getTPre(cls, id):
        listTPre = []
        #print("Getting TPre")
        for instance in cls.instances:
            if instance.target == id:
                listTPre.append(instance.source)
        return listTPre
   
    @classmethod
    def getTSuc(cls, id):
        listTSuc = []
        for instance in cls.instances:
            if instance.source == id:
                listTSuc.append(instance.target)
        return listTSuc
    
def parsePNML(pnmlfile):

      
    tree = ET.parse(pnmlfile)
    root = tree.getroot()
    
    for net_elements in root.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "net"):
        # NET ELEMENTS: ID; NAME        
        print("NET ID: " + str(net_elements.attrib['id']))
        globals()[net_elements.attrib['id']] = Net(net_elements.attrib)
    
        for name_elements in net_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "name"):
        
            for text_elements in name_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                                + "text"):
                
                if isinstance(text_elements.text, str):
                    print("NAME: " + text_elements.text)
                    globals()[net_elements.attrib['id']].setNetName(text_elements.text)
                    break
            break
    
    for page_elements in root.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "page"):
        # PAGE ELEMENTS: ID        
        print("PAGE ID: " + str(page_elements.attrib['id']))
        globals()[page_elements.attrib['id']] = Page(page_elements.attrib['id']) 
    
    for place_elements in root.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "place"):
        # PLACE ELEMENTS: ID; NAME; NAME_GRAPHICS; LABEL; LABEL_GRAPHICS; INITIALMARKING; PLACE_POSITION
        print("Place ID: " + str(place_elements.attrib))
        globals()[place_elements.attrib['id']] = Place(place_elements.attrib['id'])
        
        hasInitialMarkings = False
        hasLabel = False
        
        for name_elements in place_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "name"):
            
            for text_elements in name_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "text"):
                
                if isinstance(text_elements.text, str):
                    print("NAME: " + text_elements.text)
                    globals()[place_elements.attrib['id']].setPlaceName(text_elements.text)
                    
            for graph_elements in name_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "offset"):
                
                print("NAME GRAPH: " + str(graph_elements.attrib))
                globals()[place_elements.attrib['id']].setPlaceNameGraph(graph_elements.attrib['x'], graph_elements.attrib['y'])
                
        for label_elements in place_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}" 
                                         + "label"):
            
            for text_elements in label_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "text"):
                
                if isinstance(text_elements.text, str):
                    print("LABEL: " + text_elements.text)
                    globals()[place_elements.attrib['id']].setPlaceLabel(text_elements.text)
                    hasLabel = True
                                    
            for graph_elements in label_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "offset"):
                
                print("LABEL GRAPH: " + str(graph_elements.attrib))
                globals()[place_elements.attrib['id']].setPlaceLabelGraph(graph_elements.attrib['x'],graph_elements.attrib['y'])
                
        if not hasLabel:
            globals()[place_elements.attrib['id']].setPlaceLabel("")
            globals()[place_elements.attrib['id']].setPlaceLabelGraph('0','0')
        
           
        for initialmarks_elements in place_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}" 
                                        + "initialMarking"):
            
            print(initialmarks_elements.text)
            for text_elements in initialmarks_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "text"):
                
                if isinstance(text_elements.text, str):
                    print("INITIAL MARKINGS: " + text_elements.text)
                    globals()[place_elements.attrib['id']].setInitialMark(text_elements.text)
                    hasInitialMarkings = True
                    
        if not hasInitialMarkings:
            globals()[place_elements.attrib['id']].setInitialMark("0")
                    
        for pos_elements in place_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "position"):
                
                print("PLACE POSITION: " + str(pos_elements.attrib))
                globals()[place_elements.attrib['id']].setPlacePos(pos_elements.attrib['x'], pos_elements.attrib['y'])


    for transition_elements in root.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "transition"):
        # TRANSITION ELEMENTS: ID; NAME; NAME_GRAPHICS; LABEL; LABEL_GRAPHICS; TRANSITION_POSITION
        print("Transition ID: " + str(transition_elements.attrib))
        globals()[transition_elements.attrib['id']] = Transition(transition_elements)
        
       
        for name_elements in transition_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "name"):
            
            for text_elements in name_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "text"):
                
                if isinstance(text_elements.text, str):
                    print("NAME: " + text_elements.text)
                    globals()[transition_elements.attrib['id']].setTransitionName(text_elements.text)
                    
            for graph_elements in name_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "offset"):
                
                print("NAME GRAPH: " + str(graph_elements.attrib))
                globals()[transition_elements.attrib['id']].setTransitionNameGraph(graph_elements)
                
        for label_elements in transition_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}" 
                                         + "label"):
            
            for text_elements in label_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "text"):
                
                if isinstance(text_elements.text, str):
                    print("LABEL: " + text_elements.text)
                    globals()[transition_elements.attrib['id']].setTransitionLabel(text_elements.text)
                    hasLabel = True
                                    
            for graph_elements in label_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "offset"):
                
                print("LABEL GRAPH: " + str(graph_elements.attrib))
                globals()[transition_elements.attrib['id']].setTransitionLabelGraph(graph_elements.attrib)
                
        if not hasLabel:
            globals()[transition_elements.attrib['id']].setTransitionLabel("")
            globals()[transition_elements.attrib['id']].setTransitionLabelGraph({'x': '0', 'y': '0'})
        
        for pos_elements in transition_elements.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "position"):
                
                print("TRANSITION POSITION: " + str(pos_elements.attrib))
                globals()[transition_elements.attrib['id']].setTransitionPos(pos_elements)


    for arc_elements in root.iter("{http://www.pnml.org/version-2009/grammar/pnml}"
                              + "arc"):
        # ARC ELEMENTS: ID; SOURCE; TARGET; POSITION1; POSITION2
        
        print("ARC ID: " + str(arc_elements.attrib['id']))
        globals()[arc_elements.attrib['id']] = Arc(arc_elements.attrib['id'],arc_elements.attrib['source'],arc_elements.attrib['target'])


                

def getET(pnmlfile):
    tree = ET.parse(pnmlfile)
    root = tree.getroot()
    return root

def runPNMLParse():
     main()                            
    


def main():
    
    #parsePNML('pequenaFabricaInterpretada_wAUTONET.pnml')
    #parsePNML('pequenaFabricaInterpretada.pnml')
    #parsePNML('2WayManufacturing.pnml')
    print("__PRINT_PLACES_START__")
    #print(len(Place.placesInstances))
    
    #Place.print_instances()
    #print("__PRINT_PLACES_END__")
    
    #print("\n__PRINT_TRANSITION_START__")
    #print(len(Transition.transitionInstances))
    
    #Transition.print_instances()
    #print("__PRINT_TRANSITION_END__")
    
    #print("\n__PRINT_ARC_START__")
    #print(len(Arc.arcInstances))
    
    #Arc.print_instances()
    #print("__PRINT_ARC_END__")
    
    #print(Place.listPlace())
    
if __name__ == "__main__":
    main()