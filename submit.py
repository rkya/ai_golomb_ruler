#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

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
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
    if len(assignedVariables) == 0:
        return -1, []
    while True:
        prevL = L
        prevAssignedVariables = assignedVariables
        assignedVariables = list()
        L -= 1
        variables = [i for i in range(0, L + 1)]
        assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
        if len(assignedVariables) == 0:
            return prevL, prevAssignedVariables

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


def forwardCheck(L, remainingLegalValues, newDistance):
    index = next(iter(newDistance))
    remainingLegalValues[index] = list()
    remainingLegalValues[index].append(index)
    for i in range(0, L + 1):
        if i != index:
            if len(remainingLegalValues[i]) <= 0:
                return False
    return True


def backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues):
    if len(assignedVariables) == M:
        return assignedVariables
    for value in variables:
        result, newDistance = isValueConsistentFT(value, assignedVariables, distance)
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables
            if forwardCheck(L, remainingLegalValues, newDistance):
                assignedVariables = backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues)
                if len(assignedVariables) == M:
                    return assignedVariables
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables

def FC(L, M):
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    remainingLegalValues = list(list())
    for i in range(0, L + 1):
        remainingLegalValues.append(variables)
    assignedVariables = backTrackWithForwardChecking(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
    if len(assignedVariables) == 0:
        return -1, []
    while True:
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
            return prevL, prevAssignedVariables


#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]
