## Program implements 'Median Maintenance'
## INPUT: A stream of integers
## OUTPUT: Median of the subset of data received in i'th iteration
## CONSTRAINT: Time complexity should be O(log(i))

import math as M
import Heaps_Basic as heap  ## File where insert(), extractMin() and extractMax() functions are defined

## The 'H_low' heap.
## Contains the smaller half of data stream received.
## Supports EXTRACT MAX operation
hL = []

## The 'H_high' heap.
## Contains the greater half of data stream received.
## Supports EXTRACT MIN operation
hH = [] 

def getMedian(num, val):
    global hL, hH
    hL.sort()
    hH.sort()

    ## SHORT CASES
    ## The first element of the stream is median so far
    if(num == 0):
        hL.append(val)
        return [val]

    ## The first two elements of the stream are medians so far
    if(num == 1):
        if(hL[0] < val):
            hH.append(val)
            return [hL[0], hH[0]]
        
        hH.append(hL[0])
        hL[0] = val
        return [hL[0], hH[0]]

    ## GENERAL CASES

    ## Get the max of H_low and min or H_high
    a, hL = heap.extractMax(len(hL), hL)
    b, hH = heap.extractMin(len(hH), hH)

    ## Before the latest value received, i.e., val, even no. of data has been received.
    ## After accepting 'val', total odd no. of data will have been received and so, there will be one median which will be the (num/2 + 1)'th value
    if(num % 2 == 0):
        ## Following two if-conditions test if val lies outside of range(a,b).
        ## If so,
        ##    'val' is appended into respective heap.
        ##    'a' and 'b' are inserted to their original heaps
        ##    The median is then set as 'a' or 'b', depending on where 'val' was inserted.
        if(val <= a):
            hL = heap.insert(len(hL), hL, val)
            hL = heap.insert(len(hL), hL, a)
            hH = heap.insert(len(hH), hH, b)
            return [a]

        if(val >= b):
            hH = heap.insert(len(hH), hH, val)
            hL = heap.insert(len(hL), hL, a)
            hH = heap.insert(len(hH), hH, b)
            return [b]

        ## If 'val' lies between 'a' and 'b',
        ##    'a' and 'b' are inserted to their original heaps and 'val' into H_low.
        ##    The median is returned as 'val'.
        hL = heap.insert(len(hL), hL, val)
        hL = heap.insert(len(hL), hL, a)
        hH = heap.insert(len(hH), hH, b)
        return [val]

    ## Before the latest value received, i.e., val, if odd no. of data has been received.
    ## After accepting 'val', total even no. of data will have been received and so, there will be two medians which will be the (num+1)/2'th and (num+3)/2'th values
    else:
        ## Following two if-conditions test if val lies outside of range(a,b).
        ## If so,
        ##      'val' is inserted into respective heap.
        ##      If after this the length of heap containing 'val' is greater than the other heap by one more, then 'a' and 'b' are inserted into the other heap.
        ##          This test is needed to maintain the invariant that difference between sizes of both heaps is one or zero.
        if(val <= a):
            hL = heap.insert(len(hL), hL, val)
            if(len(hL) >= len(hH) + 1):
                hH = heap.insert(len(hH), hH, a)
                hH = heap.insert(len(hH), hH, b)

                c, hL = heap.extractMax(len(hL), hL)
                hL = heap.insert(len(hL), hL, c)
                return [c, a]

            ##  If after insertion of 'val' the lengths of both heaps are same, then 'a' and 'b' are inserted into their original heaps.
            hL = heap.insert(len(hL), hL, a)
            hH = heap.insert(len(hH), hH, b)
            return [a, b]

        if(val >= b):
            hH = heap.insert(len(hH), hH, val)
            if(len(hH) >= len(hL) + 1):
                hL = heap.insert(len(hL), hL, a)
                hL = heap.insert(len(hL), hL, b)

                c, hH = heap.extractMin(len(hH), hH)
                hH = heap.insert(len(hH), hH, c)
                return [b, c]

            ##  If after insertion of 'val' the lengths of both heaps are same, then 'a' and 'b' are inserted into their original heaps.
            hL = heap.insert(len(hL), hL, a)
            hH = heap.insert(len(hH), hH, b)
            return [a, b]

        ## If 'val' lies between 'a' and 'b',
        ##      'val is inserted into the smaller heap (one heap is always smaller because 'num' is odd)
        ##      'a' and 'b' are inserted into their original heaps
        if(len(hL) > len(hH)):
            hH = heap.insert(len(hH), hH, val)
            hL = heap.insert(len(hL), hL, a)
            hH = heap.insert(len(hH), hH, b)
            return [a, val]

        hL = heap.insert(len(hL), hL, val)
        hL = heap.insert(len(hL), hL, a)
        hH = heap.insert(len(hH), hH, b)
        return [val, b]

## Function accepts path to a file containing a number of lines with one integer per line and returns a list containing the integers in the same order
def readFile(path):
    data = open(path)

    stream = []
    for value in data:
        stream.append(int(value))

    return stream
    
if __name__ == '__main__':
    stream = readFile("medians.txt")
    
    num = -1
    medians = []    ## Stores all medians sequentially as stream is accepted by the program

    ## Pass data one by one.
    for i in range(len(stream)):
        num += 1
        m = getMedian(num, stream[i])
        medians.append(m)
       
    s = 0
    for m in medians:
        s = s + m[0]    ## For sum calculation, only the first median is considered in case of two medians

    print("SUM OF MEDIANS IS = ", s)
