def selectionSort(inputArray):
    length = len(inputArray)
    currentIndex = 0

    while currentIndex < (length-1):
        minindex = currentIndex
        min = inputArray[currentIndex]
        for i in range(currentIndex, length):
            if (inputArray[i] < min):
                minindex = i
                min = inputArray[i]

        inputArray[minindex] = inputArray[currentIndex]
        inputArray[currentIndex] = min
        currentIndex += 1

    return inputArray

def selection_sort_by_heuristic(inputArray):
    length = len(inputArray)
    currentIndex = 0

    while currentIndex < (length-1):
        minindex = currentIndex
        min = inputArray[currentIndex].heuristic()
        for i in range(currentIndex, length):
            if (inputArray[i].heuristic() < min):
                minindex = i
                min = inputArray[i].heuristic()

	temp = inputArray[minindex]
        inputArray[minindex] = inputArray[currentIndex]
        inputArray[currentIndex] = temp
        currentIndex += 1

    a = []
    for i in range(8):
        a.append(inputArray[i].heuristic())
    #print a
    return inputArray

def selection_sort_by_func(inputArray, comparefunc):
    length = len(inputArray)
    currentIndex = 0

    while currentIndex < (length-1):
        minindex = currentIndex
        min = comparefunc(inputArray[currentIndex])
        for i in range(currentIndex, length):
            thish = comparefunc(inputArray[i])
            if (thish < min):
                minindex = i
                min = thish

	temp = inputArray[minindex]
        inputArray[minindex] = inputArray[currentIndex]
        inputArray[currentIndex] = temp
        currentIndex += 1

    return inputArray

