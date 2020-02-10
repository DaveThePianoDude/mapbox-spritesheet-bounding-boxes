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

# font
font = cv2.FONT_HERSHEY_SIMPLEX

sys.setrecursionlimit(10**6)

objectsFound = []
boundingBoxes = []

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

img = cv2.imread('TLM_MINI_MISC_CULT.png')

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

file = open("output.txt","w")

while (len(objectsFound) > 0):
    thing = objectsFound.pop()
    xLeft=width
    xRight=0
    yBottom=0
    yTop=height
    # Obtain bounding box for each set of organically-grown point clusters.
    for p in thing.stack:
        img[p.y,p.x] = [100,0,255]
        if p.x > xRight:
            xRight=p.x
        if p.x < xLeft:
            xLeft=p.x
        if p.y < yTop:
            yTop=p.y
        if p.y > yBottom:
            yBottom=p.y
    boundingBox = Icon(xLeft-1, yTop-1, (xRight-xLeft)+2, (yBottom-yTop)+2)
    cv2.rectangle(img, (boundingBox.x,boundingBox.y), (boundingBox.x+boundingBox.width,boundingBox.y+boundingBox.height), (255, 0, 0), 1)
    # org
    org = (boundingBox.x-10,boundingBox.y+5)

    # fontScale
    fontScale = .5

    # Blue color in BGR
    color = (20, 20, 20)

    # Line thickness of 2 px
    thickness = 1

    name = str(len(objectsFound))

    # Using cv2.putText() method
    img = cv2.putText(img, name, org, font,
                       fontScale, color, thickness, cv2.LINE_AA)

    boundingBoxes.append(boundingBox)

    file.write("\""+"icon-"+name+"\": {\n")
    file.write("\t\"x\": "+str(boundingBox.x)+",\n")
    file.write("\t\"y\": "+str(boundingBox.y)+",\n")
    file.write("\t\"width\": "+str(boundingBox.width)+",\n")
    file.write("\t\"height\": "+str(boundingBox.height)+",\n")
    file.write("\t\"pixelRatio\": 1\n")
    file.write("},\n")

file.close()

print("# of bounding boxes found: " + str(len(boundingBoxes)))

scale_percent = 150 # percent of original size
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
# resize image
resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

# Output img with window name as 'image'
cv2.imshow('image', resized)
cv2.waitKey(0)

# Destroying present windows on screen
cv2.destroyAllWindows()
