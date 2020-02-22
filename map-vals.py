#!/usr/bin/python3

import json
import argparse


def map(inputFile):
    with open(inputFile, 'r') as file:
        jsonData = json.load(file)
        for item in jsonData:
            print (item)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile', nargs = '?')
    args = parser.parse_args()
    map(args.inputFile)
