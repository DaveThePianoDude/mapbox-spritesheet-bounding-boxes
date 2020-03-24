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

# key is a base-1 integer but csv rows are base-0.  Subtract 1 to get the correct value.
def lookupNameValue(key):
    key -= 1
    mappedValue = csvRows[key][0]
    
    return mappedValue

def map(inputFile, outputFile):
    with open(inputFile, 'r') as file:
        jsonData = json.loads(file.read())
        for key in jsonData:
            transformedJsonObject[lookupNameValue(int(key[5:]))] = jsonData[key]
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
