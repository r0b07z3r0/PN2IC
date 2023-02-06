def findSublist(subList, inList):
    subListLength = len(subList)
    for i in range(len(inList)-subListLength):
        if subList == inList[i:i+subListLength]:
            return (i, i+subListLength)
    return None

def isSublist(subList, inList):
    subListLength = len(subList)
    for i in range(len(inList)-subListLength):
        if subList == inList[i:i+subListLength]:
            return True
    return False
# Removes the sublist, if it exists and returns a new list, otherwise returns the old list.

def removeSublistFromList(subList, inList):
    indices = findSublist(subList, inList)
    if not indices is None:
        return inList[0:indices[0]] + inList[indices[1]:]
    else:
        return inList


newFlowSequence = [['selDiverge', ['t7', 't1', 't3']], 't7', 'p1', ['selDiverge', ['t2', 't11']], 't2', 'p0', ['selDiverge', ['t0', 't20']], 't0', 'p15', ['selDiverge', ['t19', 't18']], 't19', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep', 't18', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep', 't20', 'p17', 't21', 'JumpStep', 't11', 'p12', 't13', 'p15', ['selDiverge', ['t19', 't18']], 't19', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep', 't18', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep', 't1', 'p3', 't4', 'p4', 't6', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep', 't3', 'p7', 't10', 'p8', 't12', 'p9', 't14', 'p10', ['selDiverge', ['t5', 't15']], 't5', 'p13', 't16', 'JumpStep', 't15', 'p14', 't17', 'JumpStep']

#print(newFlowSequence)
print('\n')
repSeq = []
repSeq = newFlowSequence.copy()
indRep = 0
indSet = 0
compList = [[]]
changeIndRep = False

#teste = [1,2,3,4,87,98,2,5,6,1,2,3,5,76,7,6,43,2,3,4,54,6,7,1,2,3,5,5,7,87,2,3,4,7,8,9,87]

teste = newFlowSequence.copy()

seqList = [[]]
indSeq = 0
for num in range(len(teste)):
    apt = seqList[indSeq].copy()
    if teste[num:].count(teste[num]) > 1:
        apt.append(teste[num])
        print(apt)
        print('Teste')
        print(teste[num:])
        print(isSublist(apt,teste[num:]))
        if isSublist(apt,teste[num:]):
            seqList[indSeq].append(teste[num])
            changeIndRep = True
        else:
            changeIndRep = True
    elif changeIndRep:
        indSeq+=1
        seqList.append([])
        changeIndRep = False
        
        
print('\n')
print(seqList)

for seqCl in seqList:
    teste = removeSublistFromList(seqCl, teste)

print(teste)
