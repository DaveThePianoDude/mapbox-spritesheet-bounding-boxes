#!/usr/bin/python3

import pandas

df=pandas.read_csv("sprite-manifest.csv",converters={"Index":int})
