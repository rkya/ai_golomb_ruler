#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

counterBT = 0
counterFC = 0
counterCP = 0
#Your backtracking function implementation
def isValueConsistent(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        if newDistance in distance or newDistance in newSetValues or newDistance == 0:
            return False, set()
        newSetValues.add(newDistance)

    if len(assignedVariables) == 0:
        if value in distance or value in newSetValues:
            return False, set()
        newSetValues.add(value)
    return True, newSetValues


def backTrack(assignedVariables, csp, M, variables, distance):
    global counterBT
    counterBT += 1
    if len(assignedVariables) == M:
        return assignedVariables
    for value in variables:
        result, newDistance = isValueConsistent(value, assignedVariables, distance)
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables
            assignedVariables = backTrack(assignedVariables, csp, M, variables, distance)
            if len(assignedVariables) == M:
                return assignedVariables
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables


def BT(L, M):
    global counterBT
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
    if len(assignedVariables) == 0:
        print counterBT
        return -1, []
    while True:
        prevCounterBT = counterBT
        counterBT = 0
        prevL = L
        prevAssignedVariables = assignedVariables
        assignedVariables = list()
        L -= 1
        variables = [i for i in range(0, L + 1)]
        assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
        if len(assignedVariables) == 0:
            print prevCounterBT
            return prevL, sorted(prevAssignedVariables)

#Your backtracking+Forward checking function implementation
def isValueConsistentFT(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        if newDistance in distance or newDistance in newSetValues or newDistance == 0:
            return False, set()
        newSetValues.add(newDistance)

    if len(assignedVariables) == 0:
        if value in distance or value in newSetValues:
            return False, set()
        newSetValues.add(value)
    return True, newSetValues

def calculateLegalValues(distance, assignedVariables, remainingLegalValues):
    temp = remainingLegalValues[:]
    for value in remainingLegalValues:
        for marker in distance:
            newDistance = abs(value - marker)
            if newDistance in distance or newDistance in assignedVariables:
                if value in temp:
                    temp.remove(value)
    return temp[:]


def forwardCheck(L, remainingLegalValues, newDistance, value, assignedVariables, M):
    index = len(assignedVariables) - 1
    remainingLegalValues[index] = [value]
    # remainingLegalValues[index].append(value)
    for i in range(index + 1, M):
        if i != index:
            remainingValuesRow = calculateLegalValues(newDistance, assignedVariables, remainingLegalValues[i])
            if len(remainingValuesRow) == 0:
                return False
    return True
    # index = next(iter(newDistance))
    # remainingLegalValues[index] = list()
    # remainingLegalValues[index].append(index)
    # for i in range(0, L + 1):
    #     if i != index:
    #         if len(remainingLegalValues[i]) <= 0:
    #             return False
    # return True


def backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues):
    global counterFC
    counterFC += 1
    if len(assignedVariables) == M:
        return assignedVariables

    #restoring remainingLegalValues:
    remainingLegalValues = list( list() )
    for i in range(0, M):
        remainingLegalValues.append(variables)
    for index in range(0, M):
        if index < len(assignedVariables):
            remainingLegalValues[index] = [assignedVariables[index]]
        else:
            remainingLegalValues[index] = calculateLegalValues(distance, assignedVariables, remainingLegalValues[index])

    for value in variables:
        result, newDistance = isValueConsistentFT(value, assignedVariables, distance)
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables

            if forwardCheck(L, remainingLegalValues, newDistance, value, assignedVariables, M):
                # print "remainingLegalValues", remainingLegalValues
                assignedVariables = backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues)
                if len(assignedVariables) == M:
                    return assignedVariables
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables

def FC(L, M):
    global counterFC
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    remainingLegalValues = list(list())
    for i in range(0, M):
        remainingLegalValues.append(variables)
    assignedVariables = backTrackWithForwardChecking(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
    if len(assignedVariables) == 0:
        print counterFC
        return -1, []
    while True:
        prevCounterFC = counterFC
        counterFC = 0
        prevL = L
        prevAssignedVariables = assignedVariables
        assignedVariables = list()
        L -= 1
        variables = [i for i in range(0, L + 1)]
        remainingLegalValues = list(list())
        for i in range(0, L + 1):
            remainingLegalValues.append(variables)
        assignedVariables = backTrackWithForwardChecking(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
        if len(assignedVariables) == 0:
            print prevCounterFC
            return prevL, sorted(prevAssignedVariables)





#Bonus: backtracking + constraint propagation
def isValueConsistentCP(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        if newDistance in distance or newDistance in newSetValues or newDistance == 0:
            return False, set()
        newSetValues.add(newDistance)

    if len(assignedVariables) == 0:
        if value in distance or value in newSetValues:
            return False, set()
        newSetValues.add(value)
    return True, newSetValues

def calculateLegalValuesCP(distance, assignedVariables, remainingLegalValues):
    temp = remainingLegalValues[:]
    for value in remainingLegalValues:
        for marker in distance:
            newDistance = abs(value - marker)
            if newDistance in distance or newDistance in assignedVariables:
                if value in temp:
                    temp.remove(value)
    return temp[:]


def propagateConstraints(L, remainingLegalValues, newDistance, value, assignedVariables, M):
    index = len(assignedVariables) - 1
    remainingLegalValues[index] = [value]
    constrainedLegalValues = remainingLegalValues[:]

    # remainingLegalValues[index].append(value)
    for i in range(index + 1, M):
        if i != index:
            constrainedLegalValues[i] = calculateLegalValuesCP(newDistance, assignedVariables, constrainedLegalValues[i])
            if len(constrainedLegalValues[i]) == 0:
                return False
    for i in range(0, M):
        if len(constrainedLegalValues[i]) == 1 and i != index and constrainedLegalValues[i][0] == value:
            return False
    return True


def backTrackWithConstraintPropagation(assignedVariables, csp, M, L, variables, distance, remainingLegalValues):
    global counterFC
    counterFC += 1
    if len(assignedVariables) == M:
        return assignedVariables

    #restoring remainingLegalValues:
    remainingLegalValues = list( list() )
    for i in range(0, M):
        remainingLegalValues.append(variables)
    for index in range(0, M):
        if index < len(assignedVariables):
            remainingLegalValues[index] = [assignedVariables[index]]
        else:
            remainingLegalValues[index] = calculateLegalValuesCP(distance, assignedVariables, remainingLegalValues[index])

    for value in variables:
        result, newDistance = isValueConsistentCP(value, assignedVariables, distance)
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables

            if propagateConstraints(L, remainingLegalValues, newDistance, value, assignedVariables, M):
                # print "remainingLegalValues", remainingLegalValues
                assignedVariables = backTrackWithConstraintPropagation(assignedVariables, csp, M, L, variables, distance, remainingLegalValues)
                if len(assignedVariables) == M:
                    return assignedVariables
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables

def CP(L, M):
    global counterFC
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    remainingLegalValues = list(list())
    for i in range(0, M):
        remainingLegalValues.append(variables)
    assignedVariables = backTrackWithConstraintPropagation(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
    if len(assignedVariables) == 0:
        print counterFC
        return -1, []
    while True:
        prevCounterFC = counterFC
        counterFC = 0
        prevL = L
        prevAssignedVariables = assignedVariables
        assignedVariables = list()
        L -= 1
        variables = [i for i in range(0, L + 1)]
        remainingLegalValues = list(list())
        for i in range(0, L + 1):
            remainingLegalValues.append(variables)
        assignedVariables = backTrackWithConstraintPropagation(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
        if len(assignedVariables) == 0:
            print prevCounterFC
            return prevL, sorted(prevAssignedVariables)

