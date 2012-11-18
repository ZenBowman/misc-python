def binarySearchHelper(elem, sortedArray, start, end):
    if (start == end):
        if (sortedArray[start] != elem):
            return -1
        else:
            return start
    else:
        halfie = int(((end-start)/2) + start)
        print halfie
        if (sortedArray[halfie] == elem):
            return halfie
        elif (sortedArray[halfie] > elem):
            return binarySearchHelper(elem, sortedArray, start, halfie)
        else:
            return binarySearchHelper(elem, sortedArray, halfie, end)
            
def binarySearch(elem, sortedArray):
    return binarySearchHelper(elem, sortedArray, 0, len(sortedArray))
