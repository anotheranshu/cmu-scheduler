#!/bin/env python2
from codes import *
import sys
import random

FLUSHING_THRESHOLD = 8
GARBAGE_INC_LEVEL = 2
MAX_NUM_OF_ROUNDS = 2

################## Utils ####################
def numToChars(num):
    if num == 0:
        return NUM_MAPPING[0]
    elif num > 255:
        raise Exception("should not convert numbers larger than 255")
    else:
        s = ""
        while num > 0:
            s = NUM_MAPPING[num % 10] + s
            num /= 10
        return s

def writeNCom(outfile, com, n):
    if n == 0:
        return
    outfile.write(com)
    outfile.write(numToChars(n))

def pushToHead(outfile, length):
    if length-1 == 0:
        return
    n = random.randint(1, GARBAGE_INC_LEVEL)
    lst = genNStepRand(length-1, n)
    total = 0
    for i in xrange(n):
        writeNCom(outfile, SHUFFLE, lst[i])
        total += lst[i]
        if total != length-1:
            writeNCom(outfile, INC, random.randint(0,255))

def incAndShuffle(outfile, num, length):
    # There are four phases:
    #  inc at bottom of glass: a
    #  then pop out
    #  then inccurrent: b
    #  then shuffle till next time it is head
    #  then inc some more: c
    #  then inc even more as inccurrent: d
    #  put to end of queue
    n = random.randint(1, MAX_NUM_OF_ROUNDS)
    lst = genNStepRand(num, 2*n)
    for i in xrange(n):
        pushToHead(outfile, length)
        writeNCom(outfile, INC, lst[2*i])
        outfile.write(DEQUEUE)
        writeNCom(outfile, INCCURRENT, lst[2*i+1])
        outfile.write(ENQUEUE)

def addGarbage():
    pass

def flush(outfile):
    outfile.write(FLUSH)

def genNStepRand(num, n):
    lst = [0] * n
    cSum = 0
    for i in xrange(n-1):
        new = random.randint(0, num-cSum)
        lst[i] = new
        cSum += new
    lst[n-1] = num - cSum
    return lst

############## Main Functions ###############

def encodeChar(infileString, outfile, i, length):
    num = ord(infileString[i])
    outfile.write(EXTEND)
    outfile.write(MOVE)
    incAndShuffle(outfile, num, length)
    addGarbage()

def main():
    #TODO:
    # #1: numbering
    # #6: flushing
    # 2: use two ways to inc
    # #3: add incs when not head
    # 4: move head around a bit
    # 5: a few rounds of queueing
    # 7: garbage
    restartNums = 0
    with open('parchment.txt', 'w') as outfile:
        with open(sys.argv[1], 'r') as infile:
            infileString = infile.read()
            for i in xrange(len(infileString)):
                if i % FLUSHING_THRESHOLD == 0 and i!=0:
                    flush(outfile)
                    restartNums += 1
                encodeChar(infileString,
                           outfile,
                           i,
                           i-restartNums*FLUSHING_THRESHOLD+1)
            flush(outfile)
    return 0

if __name__ == '__main__':
    main()
