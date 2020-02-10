#!/usr/bin/python3

# importing OpenCV(cv2) module
import cv2
import numpy as matrix
import sys

# the setrecursionlimit function is
# used to modify the default recursion
# limit set by python. Using this,
# we can increase the recursion limit
# to satisfy our needs

sys.setrecursionlimit(10**6)

objectsFound = []

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Icon:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.stack = []

    def __hash__(self):
        print('The hash is:')
        return hash((self.x, self.y))

#returns true if the pixel at (x,y) is black.
def interrogate(x,y):
    _blue = img[y,x,0]
    _green = img[y,x,1]
    _red = img[y,x,2]
    #if this is a relatively black pixel
    return (_red < 150 and _green < 150 and _blue < 150 and scanned[x,y] < 1)

def scan(icon,x,y):
    icon.stack.append(Point(x,y));
    scanned[x,y] = 1
    if (x>0 and scanned[x-1,y]<1 and interrogate(x-1,y)):
        scan(icon,x-1,y)
    if (y>0 and scanned[x,y-1]<1 and interrogate(x,y-1)):
        scan(icon,x,y-1)
    if (x<width and scanned[x+1,y]<1 and interrogate(x+1,y)):
        scan(icon,x+1,y)
    if (y<height and scanned[x,y+1]<1 and interrogate(x,y+1)):
        scan(icon,x,y+1)

# Save image in set directory
# Read RGB image

img = cv2.imread('20200130_074008.png')

height, width = img.shape[:2]

print ('width='+str(width))
print ('height='+str(height))

scannedPixelCount = 0
scanned = matrix.zeros([width,height], dtype = int)

print ('initialized numpy array')

for y in range(height-2):
   for x in range(width-2):
       if interrogate(x,y):
        img[y,x] = [100, 0, 255]
        scannedPixelCount+=1
        icon = Icon(x,y,0,0)
        scan(icon,x,y)
        objectsFound.append(icon)
        #print("x=" + str(x) + ",y=" + str(y) + ", len=" + str(len(icon.stack)))

print(len(objectsFound))

objectsFound.pop()
thing = objectsFound.pop()
print(len(thing.stack))

for p in thing.stack:
    print(str(p.x))
    print(str(p.y))
    img[p.y,p.x] = [100,0,255]

scale_percent = 50 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# Output img with window name as 'image'
cv2.imshow('image', resized)

print(scannedPixelCount)

# Maintain output window utill
# user presses a key
cv2.waitKey(0)

# Destroying present windows on screen
cv2.destroyAllWindows()
