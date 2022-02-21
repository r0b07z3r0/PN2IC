import csv
import xml.etree.ElementTree as ET


def parsePNML(pnmlfile):
 
    tree = ET.parse(pnmlfile)
    root = tree.getroot()
    print("root tag:" + root.tag)
    print(root.attrib)
    pnmlitems = []

    for item in root:
        print("item tag:" + item.tag)
        print(item.attrib)
    
        for child in item:
            print("child tag:" + child.tag)
            print(child.attrib)
      
            for child2 in child:
                print("child2 tag:" + child2.tag)
                print(child2.attrib)
                
                for child3 in child2:
                    print("child3 tag:" + child3.tag)
                    print(child3.attrib)
                    
                    for child4 in child3:
                        print("child4 tag:" + child4.tag)
                        print(child4.attrib)            

                        for child5 in child4:
                            print("child5 tag:" + child5.tag)
                            print(child5.attrib)  
                             
    return pnmlitems


def main():
    
    pnmlitems = parsePNML('pequenaFabricaInterpretada_wAUTONET.pnml')
    print(pnmlitems)
    
    
if __name__ == "__main__":
    main()