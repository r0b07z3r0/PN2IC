import csv
import xml.etree.ElementTree as ET


def parsePNML(pnmlfile):
 
    tree = ET.parse(pnmlfile)
    root = tree.getroot()
    print("root tag:" + root.tag)
    print(root.attrib)
    pnmlitems = []

    for item in root.iter(None):
        print("item tag:" + item.tag)
        if(len(item.attrib) != 0):
            print(item.attrib)
        for elements in item.itertext():
            if(len(elements.strip()) != 0):
                print(elements)

      

                

                             
    return pnmlitems


def main():
    
    pnmlitems = parsePNML('pequenaFabricaInterpretada_wAUTONET.pnml')
    print(pnmlitems)
    
    
if __name__ == "__main__":
    main()