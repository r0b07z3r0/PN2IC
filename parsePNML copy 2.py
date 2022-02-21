import csv
import xml.etree.ElementTree as ET


def parsePNML(pnmlfile):

    pnmlitems = []
    
    tree = ET.parse(pnmlfile)
    root = tree.getroot()
    
    for places in root.iter('*'):
        print("Places TAG:  " + places.tag)
        print("Places Attr: ")
        print(places.attrib)
        if isinstance(places.text, str):
            print("Places Text: " + places.text)


        


      

                

                             
    return pnmlitems


def main():
    
    pnmlitems = parsePNML('pequenaFabricaInterpretada_wAUTONET.pnml')
    #print(pnmlitems)
    
    
if __name__ == "__main__":
    main()