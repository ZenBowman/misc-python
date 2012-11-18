inf = 9999999999999999999999999

def findMaxCrossingSubarray(a, low, mid, high):
    leftsum = -inf
    sum = 0
    maxleft = None
    
    for i in range(mid, low, -1):
        sum = sum + a[i]
        if (leftsum is None) or (sum>leftsum):
            leftsum = sum
            maxleft = i

    rightsum = -inf
    sum = 0
    maxright = None

    for i in range(mid+1, high, +1):
        sum = sum + a[i]
        if (rightsum is None) or (sum>rightsum):
            rightsum = sum
            maxright = i

    return (maxleft, maxright, leftsum+rightsum)

def maxSubArray(a, low, high):
    if (low==high):
        return (low, high, a[low])
    else:
        mid = int((high+low)/2)
        print (low, mid, high)
        (leftlow, lefthigh, leftsum) = maxSubArray(a, low, mid)
        (midlow, midhigh, midsum) = findMaxCrossingSubarray(a, low, mid, high)
        (rightlow, righthigh, rightsum) = maxSubArray(a, mid+1, high)

        if (leftsum > midsum) and (leftsum > rightsum):
            return (leftlow, lefthigh, leftsum)
        elif (rightsum > midsum) and (rightsum > leftsum):
            return (rightlow, righthigh, rightsum)
        else:
            return (midlow, midhigh, midsum)

def msa(a):
    return maxSubArray(a, 0, len(a)-1)
        
