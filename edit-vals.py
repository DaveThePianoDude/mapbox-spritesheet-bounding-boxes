#!/usr/bin/python3

## PURPOSE:  The purpose of this tool is to perform arithmetic edits on the cartesian coordinates
##           embedded in the sprite manifeset json.  This facilitates updates to the spritesheet.

import csv
import json
import argparse

jsonRows = []
transformedJsonObject = {}

xOffset = 0
yOffset = 0

def mapNameToIconId(inputFile):
    totalCount = 0
    with open(inputFile, 'r') as file:
        # Get the json from the sprite sheet manifest.
        jsonRows = json.loads(file.read())
        # For each entry,
        for key in jsonRows:
            entry = jsonRows[key]
            entry['x'] += int(xOffset)
            entry['y'] += int(yOffset)
            transformedJsonObject[key] = entry
            totalCount +=1

    print("Total count of sprite json entries edited: " + str(totalCount))

def dumpOutput(outputFile):
    # Dump the transformed object to outpujson t file.
    with open(outputFile, 'w') as file:
        json.dump(transformedJsonObject, file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile')
    parser.add_argument('xOffset')
    parser.add_argument('yOffset')

    args = parser.parse_args()
    xOffset = args.xOffset
    yOffset = args.yOffset
    mapNameToIconId(args.inputFile)
    dumpOutput(args.outputFile)
