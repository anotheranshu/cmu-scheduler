#!/bin/env python2
from codes import *
from collections import deque
import sys

class Decoder(object):
    def __init__(self):
        self.initQueue()
        self.NUM_MAPPING_SET = set(NUM_MAPPING)
        self.verbose = False

    def initQueue(self):
        self.length = 0
        self.start = 0
        self.head = -1
        self.current = 0
        self.q = deque()
        self.num = 0
        self.currentMove = ""
        self.isReadingNumber = False
        self.currentHasStuff = False

    def dealWithNumbering(self, char):
        if self.isReadingNumber:
            for i in xrange(self.num-1):
                self.resolveMoves(self.currentMove, True)
        self.currentMove = char
        self.isReadingNumber = False

    def printQueue(self):
        # Just for debugging purposes
        if self.verbose:
            print"""
======= Queue Status =======
Length: %d
start: %d
head: %d
current: %d
num: %d
currentMove: %c
isReadingNumber: %d
self.q:
    """ % (self.length, self.start, self.head, self.current, self.num, self.currentMove, self.isReadingNumber), self.q

    def extend(self):
        self.q.append(0)
        self.length += 1

    def move(self):
        self.head += 1

    def dequeue(self):
        self.current = self.q.popleft()
        self.currentHasStuff = True
        self.head = (self.head - 1) % self.length
        self.start = (self.start - 1) % self.length

    def enqueue(self):
        if self.currentHasStuff:
            self.q.append(self.current)
        else:
            raise Exception("cannot enqueue when nothing in curretn")
        self.currentHasStuff = False

    def shuffle(self, fromRepeat):
        if not fromRepeat:
            self.printQueue()
        self.dequeue()
        self.enqueue()

    def inc(self):
        if self.head == 0:
            ele = self.q.popleft()
            ele += 1
            self.q.appendleft(ele)

    def inccurrent(self):
        if self.currentHasStuff:
            self.current += 1

    def flush(self):
        while True:
            try:
                stuff = self.q.popleft()
                sys.stdout.write(chr(stuff))
                #self.outfile.write(chr(stuff))
            except IndexError:
                break
        self.initQueue()

    def resolveMoves(self, char, fromRepeat=False):
        if char == EXTEND:
            self.extend()
        elif char == MOVE:
            self.move()
        elif char == DEQUEUE:
            self.dequeue()
        elif char == ENQUEUE:
            self.enqueue()
        elif char == SHUFFLE:
            self.shuffle(fromRepeat)
        elif char == INC:
            self.inc()
        elif char == INCCURRENT:
            self.inccurrent()
        elif char == FLUSH:
            self.flush()
        else:
            raise Exception("invalid moves")

    def main(self):
        with open(sys.argv[1], 'r') as f:
            #with open('spell.txt', 'w') as self.outfile:
            for char in f.read():
                if char.islower():
                    if not self.isReadingNumber:
                        self.num = 0
                        self.isReadingNumber = True
                    self.num = self.num * 10 + NUM_MAPPING.index(char)
                else:
                    self.dealWithNumbering(char)
                    self.resolveMoves(char)
        return self.q

if __name__ == '__main__':
    d = Decoder()
    d.main()
