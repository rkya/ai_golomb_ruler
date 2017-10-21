#do not modify the function names
#You are given L and M as input
#Each of your functions should return the minimum possible L value alongside the marker positions
#Or return -1,[] if no solution exists for the given L

#Your backtracking function implementation
def isValueConsistent(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        # Check for consistency i.e. space between every pair of markers is distinct and markers do not overlap
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
        # Continue with current value only if the solution of current value is consistent
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables
            # Continue recursively to mark other positions on the ruler
            assignedVariables = backTrack(assignedVariables, csp, M, variables, distance)
            if len(assignedVariables) == M:
                return assignedVariables
            # This assignment did not work out, so backtrack
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables


def BT(L, M):
    # Check if M markers can be put for a ruler of length L
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
    if len(assignedVariables) == 0:
        return -1, []

    # Since length L is possible, check for length < L
    while True:
        prevL = L
        prevAssignedVariables = assignedVariables
        assignedVariables = list()
        L -= 1
        variables = [i for i in range(0, L + 1)]
        assignedVariables = backTrack(assignedVariables, 0, M, variables, distance)
        if len(assignedVariables) == 0:
            # Since current lenth's ruler is not possible, return the previous result i.e. the optimal length ruler
            return prevL, sorted(prevAssignedVariables)

#Your backtracking+Forward checking function implementation
def isValueConsistentFT(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        # Check for consistency i.e. space between every pair of markers is distinct and markers do not overlap
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
                    # Remove this value from the set of legal values for all its neighbours
                    temp.remove(value)
    return temp[:]


def forwardCheck(L, remainingLegalValues, newDistance, value, assignedVariables, M):
    index = len(assignedVariables) - 1
    remainingLegalValues[index] = [value]
    for i in range(index + 1, M):
        if i != index:
            remainingValuesRow = calculateLegalValues(newDistance, assignedVariables, remainingLegalValues[i])
            # Check if legal values of its neighbours is not empty
            if len(remainingValuesRow) == 0:
                return False
    return True


def backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues):
    if len(assignedVariables) == M:
        return assignedVariables

    #restoring remainingLegalValues:
    remainingLegalValues = list(list())
    for i in range(0, M):
        remainingLegalValues.append(variables)
    for index in range(0, M):
        if index < len(assignedVariables):
            remainingLegalValues[index] = [assignedVariables[index]]
        else:
            remainingLegalValues[index] = calculateLegalValues(distance, assignedVariables, remainingLegalValues[index])

    for value in variables:
        result, newDistance = isValueConsistentFT(value, assignedVariables, distance)
        # Continue with current value only if the solution of current value is consistent
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables

            if forwardCheck(L, remainingLegalValues, newDistance, value, assignedVariables, M):
                # Continue recursively to mark other positions on the ruler
                assignedVariables = backTrackWithForwardChecking(assignedVariables, csp, M, L, variables, distance, remainingLegalValues)
                if len(assignedVariables) == M:
                    return assignedVariables
            # This assignment did not work out, so backtrack
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables


def FC(L, M):
    # Check if M markers can be put for a ruler of length L
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    remainingLegalValues = list(list())
    for i in range(0, M):
        remainingLegalValues.append(variables)
    assignedVariables = backTrackWithForwardChecking(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
    if len(assignedVariables) == 0:
        return -1, []
    # Since length L is possible, check for length < L
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
            return prevL, sorted(prevAssignedVariables)


#Bonus: backtracking + constraint propagation
def isValueConsistentCP(value, assignedVariables, distance):
    newSetValues = set()
    for marker in assignedVariables:
        newDistance = abs(value - marker)
        # Check for consistency i.e. space between every pair of markers is distinct and markers do not overlap
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
                    # Remove this value from the set of legal values for all its neighbours
                    temp.remove(value)
    return temp[:]


def propagateConstraints(L, remainingLegalValues, newDistance, value, assignedVariables, M):
    index = len(assignedVariables) - 1
    remainingLegalValues[index] = [value]
    constrainedLegalValues = remainingLegalValues[:]

    for i in range(index + 1, M):
        if i != index:
            constrainedLegalValues[i] = calculateLegalValuesCP(newDistance, assignedVariables, constrainedLegalValues[i])
            # Check if legal values of its neighbours is not empty
            if len(constrainedLegalValues[i]) == 0:
                return False
    for i in range(0, M):
        # Check if its neighbour has only one legal value same as its own value, then fail early
        if len(constrainedLegalValues[i]) == 1 and i != index and constrainedLegalValues[i][0] == value:
            return False
    return True


def backTrackWithConstraintPropagation(assignedVariables, csp, M, L, variables, distance, remainingLegalValues):
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
        # Continue with current value only if the solution of current value is consistent
        if result:
            distancePurge = newDistance - distance
            distance = distance.union(newDistance)
            assignedVariables.append(value)
            if len(assignedVariables) == M:
                return assignedVariables

            if propagateConstraints(L, remainingLegalValues, newDistance, value, assignedVariables, M):
                # Continue recursively to mark other positions on the ruler
                assignedVariables = backTrackWithConstraintPropagation(assignedVariables, csp, M, L, variables, distance, remainingLegalValues)
                if len(assignedVariables) == M:
                    return assignedVariables
            # This assignment did not work out, so backtrack
            assignedVariables.remove(value)
            distance = distance - distancePurge
    return assignedVariables

def CP(L, M):
    # Check if M markers can be put for a ruler of length L
    assignedVariables = list()
    distance = set()
    variables = [i for i in range(0, L + 1)]
    remainingLegalValues = list(list())
    for i in range(0, M):
        remainingLegalValues.append(variables)
    assignedVariables = backTrackWithConstraintPropagation(assignedVariables, 0, M, L, variables, distance, remainingLegalValues)
    if len(assignedVariables) == 0:
        return -1, []
    # Since length L is possible, check for length < L
    while True:
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
            return prevL, sorted(prevAssignedVariables)

