from parsePNML import ET, getET, Net, Page, Place, Transition, Arc, runPNMLParse

def writePetriNet():
    pnml = ET.Element("pnml")
    ET.register_namespace('', "http://www.pnml.org/version-2009/grammar/pnml")

    print(Net.listNet())

    net = ET.SubElement(pnml, "{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "net", {'id': Net.getID(Net.listNet()[0]), 'type': Net.getType(Net.listNet()[0])})
    
    ET.SubElement(ET.SubElement(net, "name"), "text").text = Net.listNet()[0]
    
    page = ET.SubElement(net, "{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "page", {'id': Page.listPageID[0]})
    
    for places in Place.instances:
        #<place id="p-">
        place = ET.SubElement(page, "{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "place", {'id': places.id})
        #<name>
        pname = ET.SubElement(place, "name")
        #   <text>
        ET.SubElement(pname, "text").text = places.name
        #   </text>
        #   <graphics>
        ET.SubElement(ET.SubElement(pname,"graphics"), "offset", {'x': places.name_graph_x, 'y': places.name_graph_y})
        #   </graphics>
        #</name>
        
        #<label>
        plabel = ET.SubElement(place, "label")
        #   <text>
        ET.SubElement(plabel, "text").text = places.label
        #   </text>
        #   <graphics>
        ET.SubElement(ET.SubElement(plabel, "graphics"), "offset", {'x': places.label_graph_x, 'y': places.label_graph_y})
        #   </graphics>
        #</label>

        #<initialMarking>
        if places.hasinitialmark:
            ET.SubElement(ET.SubElement(place, "initialMarking"), "text").text = places.initial_mark
        #</initialMarking>
        
        #<graphics>
        ET.SubElement(ET.SubElement(place, "graphics"), "position", {'x': places.position_x, 'y': places.position_y})
        #</graphics>
    
    
    for transitions in Transition.instances:
        #<transition id="p-">
        transition = ET.SubElement(page, "{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "transition", {'id': transitions.id})
        #<name>
        tname = ET.SubElement(transition, "name")
        #   <text>
        ET.SubElement(tname, "text").text = transitions.name
        #   </text>
        #   <graphics>
        ET.SubElement(ET.SubElement(tname,"graphics"), "offset", {'x': transitions.name_graph_x, 'y': transitions.name_graph_y})
        #   </graphics>
        #</name>
        
        #<label>
        tlabel = ET.SubElement(transition, "label")
        #   <text>
        ET.SubElement(tlabel, "text").text = transitions.label
        #   </text>
        #   <graphics>
        ET.SubElement(ET.SubElement(tlabel, "graphics"), "offset", {'x': transitions.label_graph_x, 'y': transitions.label_graph_y})
        #   </graphics>
        #</label>
        
        #<graphics>
        ET.SubElement(ET.SubElement(transition, "graphics"), "position", {'x': transitions.position_x, 'y': transitions.position_y})
        #</graphics>
        
    for arcs in Arc.instances:
        #<transition id="p-">
        ET.SubElement(page, "{http://www.pnml.org/version-2009/grammar/pnml}"
                            + "arc", {'id': arcs.id, 'source': arcs.source, 'target': arcs.target})   
            

    ET.indent(pnml, " ", 0)
    ET.ElementTree(pnml).write('WRITER.pnml')

def runPNMLWriter():
    main()

def main():
    
    #runPNMLParse()
    writePetriNet()
    
if __name__ == "__main__":
    main()