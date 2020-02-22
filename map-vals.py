#!/usr/bin/python3

import json
import argparse

iconUniqueIds = {}
transformedJsonObject = {}

def map(inputFile, outputFile):
    with open(inputFile, 'r') as file:
        jsonData = json.loads(file.read())
        for key in jsonData:
            transformedJsonObject["t-"+key] = jsonData[key]
    with open(outputFile, 'w') as file:
        json.dump(transformedJsonObject, file, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile', nargs = '?')
    args = parser.parse_args()
    map(args.inputFile,args.outputFile)
