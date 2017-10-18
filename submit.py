#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation
def selectUnassignedVariable(variables, list, csp):
    return variables.pop()


def isValueConsistent(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        if newDistance in distance or newDistance in newSetValues or newDistance == 0:
            return 0, set()
        newSetValues.add(newDistance)

    if len(assignedVariables) == 0:
        if value in distance or value in newSetValues:
            return 0, set()
        newSetValues.add(value)
    # distance = distance.union(newSetValues)
    return 1, newSetValues


def backTrack(assignedVariables, csp, M, variables, distance):
    if len(assignedVariables) == M:
        return assignedVariables
    # var = selectUnassignedVariable(variables, assignedVariables, csp)
    for value in variables:
        result, newDistance = isValueConsistent(value, assignedVariables, distance)
        if result == 1:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables
            assignedVariables = backTrack(assignedVariables, csp, M, variables, distance)
            # assignedVariables.pop()
            if len(assignedVariables) == M:
                return assignedVariables
            # variables.append(value)
            assignedVariables.remove(value)
            distance = distance - distancePurge
    # variables = variables.sort(reverse=True)
    return assignedVariables


def BT(L, M):
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    # print variables
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
def FC(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]
