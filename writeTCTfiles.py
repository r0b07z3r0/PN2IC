from parsePNML import ET, getET, Net, Page, Place, Transition, Arc
import re
def writeTCTfiles(desName, uptransitions, downtransitions):
    print("Writing TCT file")
    
    with open(desName+'.ADS', 'w') as f:
        f.write('# CTCT ADS auto-generated\n')
        f.write('\n')
        f.write(desName+'\n')
        f.write('\n')
        f.write('State size (State set will be (0,1....,size-1)):\n')
        f.write('# <-- Enter state size, in range 0 to 2000000, on line below.\n')
        #State quantity
        f.write('2\n')
        f.write('\n')
        f.write('Marker states:\n')
        f.write('# <-- Enter marker states, one per line.\n')
        f.write('# To mark all states, enter *.\n')
        f.write('# If no marker states, leave line blank.\n')
        f.write('# End marker list with blank line.\n')
        f.write('0\n')
        f.write('\n')
        f.write('Vocal states:\n')
        f.write('# <-- Enter vocal output states, one per line.\n')
        f.write('# Format: State  Vocal_Output.  Vocal_Output in range 10 to 99.\n')
        f.write('# Example: 0 10\n')
        f.write('# If no vocal states, leave line blank.\n')
        f.write('# End vocal list with blank line.\n')
        f.write('\n')
        f.write('Transitions:\n')
        f.write('# <-- Enter transition triple, one per line.\n')
        f.write('# Format: Exit_(Source)_State  Transition_Label  Entrance_(Target)_State.\n')
        f.write('# Transition_Label in range 0 to 9999.\n')
        f.write('# Example: 2 0 1 (for transition labeled 0 from state 2 to state 1).\n')

        #up transition
        for upT in uptransitions:
            upT = re.findall("t(.*)", upT)[0]
            f.write('0     '+upT+'  1    \n') 
        #down transition
        for downT in downtransitions:
            #downT = downtransitions
            downT = re.findall("t(.*)", downT)[0]
            f.write('1     '+downT+'  0    \n')

def runTCTfileWriter(desName, uptransitions, downtransitions):
    main(desName, uptransitions, downtransitions)

def main(desName, uptransitions, downtransitions):
    
    #runPNMLParse()
    writeTCTfiles(desName, uptransitions, downtransitions)
    
if __name__ == "__main__":
    main()
    
#   # CTCT ADS auto-generated

#   ECP2

#   State size (State set will be (0,1....,size-1)):
#   # <-- Enter state size, in range 0 to 2000000, on line below.
#   2

#   Marker states:
#   # <-- Enter marker states, one per line.
#   # To mark all states, enter *.
#   # If no marker states, leave line blank.
#   # End marker list with blank line.
#   0

#   Vocal states:
#   # <-- Enter vocal output states, one per line.
#   # Format: State  Vocal_Output.  Vocal_Output in range 10 to 99.
#   # Example: 0 10
#   # If no vocal states, leave line blank.
#   # End vocal list with blank line.

#   Transitions:
#   # <-- Enter transition triple, one per line.
#   # Format: Exit_(Source)_State  Transition_Label  Entrance_(Target)_State.
#   # Transition_Label in range 0 to 9999.
#   # Example: 2 0 1 (for transition labeled 0 from state 2 to state 1).
#   0     10  1    
#   1     2  0   