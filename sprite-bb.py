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

    def __repr__(self):
        return "<Icon x:%s y:%s w:%s h:%s>" % (self.x, self.y, self.width, self.height)

#returns true if the pixel at (x,y) is black.
def interrogate(x,y):
    _blue = img[y,x,0]
    _green = img[y,x,1]
    _red = img[y,x,2]
    #if this is a relatively black pixel
    return (_red < 225 and _green < 225 and _blue < 225 and scanned[x,y] < 1)

def scan(icon,x,y):
    icon.stack.append(Point(x,y))
    scanned[x,y] = 1
    if (x>0 and scanned[x-1,y]<1 and interrogate(x-1,y)):
        scan(icon,x-1,y)
    if (y>0 and scanned[x,y-1]<1 and interrogate(x,y-1)):
        scan(icon,x,y-1)
    if (x<width and scanned[x+1,y]<1 and interrogate(x+1,y)):
        scan(icon,x+1,y)
    if (y<height and scanned[x,y+1]<1 and interrogate(x,y+1)):
        scan(icon,x,y+1)

def growClusters(height, width):
    for y in range(height-2):
       for x in range(width-2):
           if interrogate(x,y):
            img[y,x] = [100, 0, 255]
            icon = Icon(x,y,0,0)
            scan(icon,x,y)
            objectsFound.append(icon)

#returns true if A completely contains B
def contains(A, B):
    if ((B.x > A.x) and (B.x + B.width) < (A.x + A.width) and (B.y > A.y) and (B.y + B.height < A.y + A.height)):
        return True
    else:
        return False

#returns true if some box A in boundingBoxes contains box B
def containsAny(A):
    for B in boundingBoxes:
        if (contains(A, B)):
            boundingBoxes.remove(B)
            boundingBoxes.insert(0,A)
            return True
    return False

# Save image in set directory
# Read RGB image
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile', nargs = '?')
    args = parser.parse_args()

    if args.inputFile == None or args.outputFile == None:
        print("Usage: ./sprite-bb.py <inputFile> <outputFile>")
    else:
        global img
        img = cv2.imread(args.inputFile)

        global height, width
        height, width = img.shape[:2]

        print ('Sprite Map width='+str(width))
        print ('Sprite Map height='+str(height))

        global scanned
        scanned = matrix.zeros([width,height], dtype = int)

        growClusters(height, width)

        # convert the objects (clusters of points) found into bounding boxes
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
            print(boundingBox)
            if (not containsAny(boundingBox)):
                boundingBoxes.append(boundingBox)

        # write the output file and markup the image for display
        file = open(args.outputFile,"w")
        file.write("{\n")

        print("# of bounding boxes remaining: " + str(len(boundingBoxes)))

        while(len(boundingBoxes) > 0):
            boundingBox = boundingBoxes.pop()

            cv2.rectangle(img, (boundingBox.x,boundingBox.y), (boundingBox.x+boundingBox.width,boundingBox.y+boundingBox.height), (255, 0, 0), 1)

            org = (boundingBox.x-10,boundingBox.y+5)
            fontScale = .5
            color = (20, 20, 20)
            thickness = 1

            name = str(len(boundingBoxes))

            # Using cv2.putText() method
            img = cv2.putText(img, name, org, font, fontScale, color, thickness, cv2.LINE_AA)

            file.write("\""+"icon-"+name+"\": {\n")
            file.write("\t\"x\": "+str(boundingBox.x)+",\n")
            file.write("\t\"y\": "+str(boundingBox.y)+",\n")
            file.write("\t\"width\": "+str(boundingBox.width)+",\n")
            file.write("\t\"height\": "+str(boundingBox.height)+",\n")
            file.write("\t\"pixelRatio\": 1\n")

            if (len(objectsFound)==0):
                file.write("}\n")
            else:
                file.write("},\n")

        file.write("}\n")
        file.close()

        scale_percent = 250 # percent of original size
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

if __name__ == '__main__':
    main()
