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
