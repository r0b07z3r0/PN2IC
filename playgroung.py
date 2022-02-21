
from parsePNML import Place, Arc, parsePNML, runPNMLParse


def main():
    print("Start PlayGround")
    
    runPNMLParse()

    plist = ['p2', 'p8', 'p4']
    tup = []
    tlow = []
    for p in plist:
        print(Place.getID(p))
        print(Arc.getTPre(Place.getID(p)))
        tup.extend(Arc.getTPre(Place.getID(p)))
    
    print(tup)
    
if __name__ == '__main__':
    main()