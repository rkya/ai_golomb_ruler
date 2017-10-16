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
    distance = distance.union(newSetValues)
    return 1, distance


def backTrack(assignedVariables, csp, M, variables, distance):
    if len(assignedVariables) == M:
        return assignedVariables
    # var = selectUnassignedVariable(variables, assignedVariables, csp)
    for value in variables:
        result, distance = isValueConsistent(value, assignedVariables, distance)
        if result == 1:
            assignedVariables.append(value)
            assignedVariables = backTrack(assignedVariables, csp, M, variables, distance)
            if len(assignedVariables) == M:
                return assignedVariables
            # assignedVariables.pop()
            variables.append(value)
    variables = variables.sort(reverse=True)
    return assignedVariables


def BT(L, M):
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    print variables
    assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
    return -1, assignedVariables

#Your backtracking+Forward checking function implementation
def FC(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]

#Bonus: backtracking + constraint propagation
def CP(L, M):
    "*** YOUR CODE HERE ***"
    return -1,[]
