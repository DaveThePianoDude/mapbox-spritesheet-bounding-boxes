#!/usr/bin/python3

import csv
import json
import argparse

prefix = "icon-" # Should be passed in as arg?

csvRows = []
transformedJsonObject = {}

def parseCsv(csvFile):
    with open(csvFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            csvRows.append(row)

def lookupIndex(iconNumber):
    index = 0cd
    for row in csvRows:
        if row[1] == iconNumber:
            return index
        index += 1;
    return -1; # return -1 if not found

# key is a base-1 integer but csv rows are base-0.  Subtract 1 to get the correct value.
def lookupNameValue(key):
    #key -= 1
    mappedValue = csvRows[key][0]

    return mappedValue

def map(inputFile, outputFile):
    totalCount = 0
    with open(inputFile, 'r') as file:
        jsonData = json.loads(file.read())
        # generate a new set of data using new keys:
        for key in jsonData:
            # get the number in the auto-generated icon id (e.g. "icon-1")
            iconNumber = key[5:]
            #print(iconNumber)
            # use that to get the index into array 'csvRows'
            index = lookupIndex(iconNumber)
            if (index > 0):
                transformedJsonObject[lookupNameValue(index)] = jsonData[key]
                totalCount += 1
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
    map(args.inputFile,args.outputFile)
