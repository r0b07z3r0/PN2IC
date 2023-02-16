def selConvRecusive(flow,trList, next):
    print('Flow Recursive:')
    print(flow)
    print('trList Recursive:')
    print(trList)
    print('next Recursive:')
    print(next)
    for each in flow:
        if each[0].startswith(next):
            print('next Found: ' + next)
        if each[0].startswith('selDiv'):
            selConvRecusive(flow[flow.index(each)+1:], each[1], each[1][0])
            break


newFlowSequence = [['pSUPCON_S1_0'], ['selDiverge_0', ['t7', 't1', 't3']], ['t7'], ['p1'], 
                   ['selDiverge_1', ['t11', 't2']], ['t11'], ['p12'], ['t13'], ['JumpStep_t13'], 
                   ['t2'], ['p0'], 
                   ['selDiverge_2', ['t0', 't20']], ['t0'], ['p15'], 
                   ['selDiverge_3', ['t19', 't18']], ['t19'], ['JumpStep_t19'], 
                   ['t18'], ['JumpStep_t18'], 
                   ['t20'], ['p17'], ['t21'], ['JumpStep_t21'], 
                   ['t1'], ['p3'], ['t4'], ['p4'], ['t6'], ['JumpStep_t6'], 
                   ['t3'], ['p7'], ['t10'], ['p8'], ['t12'], ['p9'], ['t14'], ['p10'], 
                   ['selDiverge_4', ['t15', 't5']], ['t15'], ['p14'], ['t17'], ['JumpStep_t17'], 
                   ['t5'], ['p13'], ['t16'], ['JumpStep_t16']]

for each in newFlowSequence:
    if each[0].startswith('selDiv'):
        selConvRecusive(newFlowSequence[newFlowSequence.index(each)+1:], each[1], each[1][0])
        break