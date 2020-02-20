#!/usr/bin/python3

# importing OpenCV(cv2) module
import cv2
import numpy as matrix
import sys
import argparse

# the setrecursionlimit function is
# used to modify the default recursion
# limit set by python. Using this,
# we can increase the recursion limit
# to satisfy our needs

# Step 1: Set the color that controls the interrogate function.
#bgr = (255,250,250)
bgr = (255,0,0)

font = cv2.FONT_HERSHEY_SIMPLEX
sys.setrecursionlimit(10**6)

objectsFound = []
boundingBoxes = []

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def thresh(self):
        return 7

    def sum(self):
        return self.x + self.y * self.thresh()

p = Point(3,1)
q = Point(5,2)
r = Point(0,1)

points = []

print (p.sum())

points.append(p)
points.append(q)
points.append(r)

sortedPoints = sorted(points,key=Point.sum)

while(len(sortedPoints) > 0):
    print(sortedPoints.pop().x)
