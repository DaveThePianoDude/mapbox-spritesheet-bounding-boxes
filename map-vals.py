#!/usr/bin/python3

import csv
import json
import argparse

prefix = "icon-" # Should be passed in as arg?

csvRows = []
jsonRows = []
transformedJsonObject = {}

def parseCsv(csvFile):
    with open(csvFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csvRows.append(row)

def mapNameToIconId(inputFile, outputFile):
    totalCount = 0
    with open(inputFile, 'r') as file:
        jsonRows = json.loads(file.read())
        # generate a new set of data using new keys:
        for manifestEntry in csvRows:
            # get the human-readable name from the manifest entry
            readableName = manifestEntry[0]
            # get the index into the Sprite Sheet from the manifest entry
            indexToSpriteSheet = manifestEntry[1]

            for key in jsonRows:
                # get the number in the auto-generated icon id (e.g. "icon-1")
                iconNumber = key[5:] #"icon-" has five characters...

                # if the index from the manifest matches the number for this icon,
                # we've found the json for this sprite in the numbered contact sheet.
                try:
                    if (int(iconNumber) == int(indexToSpriteSheet)):
                        transformedJsonObject[readableName] = jsonRows[key]
                        totalCount += 1
                except:
                    print("Failed to map the index for: " + readableName)

                # increment tally for accountability

    print("Total count of sprite json entries created: " + str(totalCount))

    with open(outputFile, 'w') as file:
        json.dump(transformedJsonObject, file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile', nargs = '?')
    parser.add_argument('csvFile')

    args = parser.parse_args()
    parseCsv(args.csvFile)
    mapNameToIconId(args.inputFile, args.outputFile)
