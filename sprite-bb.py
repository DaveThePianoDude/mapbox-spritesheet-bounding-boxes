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

font = cv2.FONT_HERSHEY_SIMPLEX
sys.setrecursionlimit(10**6)

objectsFound = []
sortedObjectsFound = []
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

    def getTier(self):
        if (self.y < 55):
            return 0
        if (self.y >= 55 and self.y <= 110):
            return 1
        if (self.y > 110):
            return 2

    def getRank(self):
        return self.x + (2000 * self.getTier())

#returns true if the pixel at (x,y) is black.
def interrogate(x,y,color):
    _blue = img[y,x,0]
    _green = img[y,x,1]
    _red = img[y,x,2]

    # Step 2: Set the interrogate function, depending on if we are doing the initial organic clustering of icon points
    # or the clustering of bounding boxes found during the first iteration.
    if (iter == 1):
        return (_red < color[2] and _green < color[1] and _blue < color[0] and scanned[x,y] < 1)
    else:
        return (_red == 0 and _green == 0 and _blue == 255 and scanned[x,y] < 1)

def scan(icon,x,y,color):
    icon.stack.append(Point(x,y))
    scanned[x,y] = 1
    if (x>0 and scanned[x-1,y]<1 and interrogate(x-1,y,color)):
        scan(icon,x-1,y,color)
    if (y>0 and scanned[x,y-1]<1 and interrogate(x,y-1,color)):
        scan(icon,x,y-1,color)
    if (x<width and scanned[x+1,y]<1 and interrogate(x+1,y,color)):
        scan(icon,x+1,y,color)
    if (y<height and scanned[x,y+1]<1 and interrogate(x,y+1,color)):
        scan(icon,x,y+1,color)

def growClusters(height, width, color):
    for y in range(height-2):
       for x in range(width-2):
           if interrogate(x,y,color):
            img[y,x] = [100, 0, 255]
            icon = Icon(x,y,0,0)
            scan(icon,x,y,color)
            objectsFound.append(icon)
            #print(icon.getRank())

#returns true if A completely contains B
def contains(A, B):
    if ((B.x > A.x) and (B.x + B.width) < (A.x + A.width) and (B.y > A.y) and (B.y + B.height < A.y + A.height)):
        return True
    else:
        return False

#returns true if some box A in boundingBoxes contains another box B
def containsAny(A):
    index=0
    for B in boundingBoxes:
        if (contains(A, B)):
            boundingBoxes.remove(B)
            boundingBoxes.insert(index,A)
            return True
        index +=1
    return False

# convert the objects (clusters of points) found into bounding boxes
def convertClusters(sortedObjectsFound,height, width):
    print ("Found " + str(len(sortedObjectsFound)) + " bounding boxes.")
    while (len(sortedObjectsFound) > 0):
        thing = sortedObjectsFound.pop()
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
        boundingBoxes.append(boundingBox)

# Save image in set directory
# Read bgr image
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile', nargs = '?')
    parser.add_argument('iteration')
    args = parser.parse_args()

    if args.inputFile == None or args.outputFile == None:
        print("Usage: ./sprite-bb.py <inputFile> <outputFile> <iteration# (1,2,etc)>")
    else:
        global img, iter
        iter = int(args.iteration)

        # If this is iteration 2, grab the file pre-pended with 'v-blue-'
        if (iter == 1):
            print ("Performing iteration 1...")
            img = cv2.imread(args.inputFile)
        else:
            print ("Performing iteration 2...")
            img = cv2.imread("v-blue-"+args.inputFile)

        global height, width
        height, width = img.shape[:2]

        print ('Sprite Map width='+str(width))
        print ('Sprite Map height='+str(height))

        global scanned
        scanned = matrix.zeros([width,height], dtype = int)

        # Step 1: Set the color that is used in the interrogate function.
        if (iter == 1):
            bgr = (255,250,250)
        else:
            bgr = (255,0,0)

        growClusters(height, width, bgr)
        sortedObjectsFound = sorted(objectsFound,key=Icon.getRank)
        convertClusters(sortedObjectsFound,height, width)

        foundContainedBox = True

        #improve the quality of the object detection by removing boxes contained in other boxes
        while (foundContainedBox):
            foundContainedBox = False
            for boundingBox in boundingBoxes:
                if (containsAny(boundingBox)):
                    boundingBoxes.remove(boundingBox)
                    foundContainedBox = True

        # write the output file and markup the image for display
        file = open(args.outputFile,"w")
        file.write("{\n")

        print("# of bounding boxes remaining after containment pruning: " + str(len(boundingBoxes)))

        totalLen = len(boundingBoxes)

        while(len(boundingBoxes) > 0):
            boundingBox = boundingBoxes.pop()

            #Step 3: Set the bounding box color, per iteration.
            if (iter == 1):
                cv2.rectangle(img, (boundingBox.x,boundingBox.y), (boundingBox.x+boundingBox.width,boundingBox.y+boundingBox.height), (255, 0, 0), 1)
            else:
                cv2.rectangle(img, (boundingBox.x,boundingBox.y), (boundingBox.x+boundingBox.width,boundingBox.y+boundingBox.height), (255, 255, 0), 1)

            org = (boundingBox.x-10,boundingBox.y+5)
            fontScale = .4
            color = (20, 20, 20)
            thickness = 1

            name = str(totalLen - len(boundingBoxes))

            # Step 4: Render text only after second iteration.
            if (iter == 2):
                img = cv2.putText(img, name, org, font, fontScale, color, thickness, cv2.LINE_AA)

            file.write("\""+"icon-"+name+"\": {\n")
            file.write("\t\"x\": "+str(boundingBox.x)+",\n")
            file.write("\t\"y\": "+str(boundingBox.y)+",\n")
            file.write("\t\"width\": "+str(boundingBox.width)+",\n")
            file.write("\t\"height\": "+str(boundingBox.height)+",\n")
            file.write("\t\"pixelRatio\": 1\n")

            if (len(sortedObjectsFound)==0):
                file.write("}\n")
            else:
                file.write("},\n")

        file.write("}\n")
        file.close()

        cv2.imwrite("v-blue-"+args.inputFile, img)

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

if __name__ == '__main__':
    main()
