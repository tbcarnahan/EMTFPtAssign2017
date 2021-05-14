#! /usr/bin/env python

import pprint
"""
Simple script to organize trainings into a handy dictionary
"""

## step 1 open
f = open('training_Prep2018DataRate.txt')
mylist = f.readlines()
f.close()

## step 2 empty dictionary
mydict = {}

prefix = "root://cmseos.fnal.gov//store/user/dildick/"
outfile = "PtRegression_output.root"

## loop on the list
for myentry in mylist:
    myentrys = myentry.rstrip()

    ## filename
    filename = prefix + myentrys + "/" + outfile

    version = "Run-2"
    sversion = "Run2"
    bitComp = False
    mode_number = "15"
    if "isRun3_useQS_useES" in myentrys:
        version = "Run-3 V1.2"
        sversion = "Run3_V1p2"
    elif "isRun3_useQS" in myentrys:
        version = "Run-3 V1.1"
        sversion = "Run3_V1p1"
    elif "isRun3" in myentrys:
        version = "Run-3 V1.0"
        sversion = "Run3_V1p0"

    if "bitComp" in myentrys:
        bitComp = True
    label = version

    mode_index = myentrys.index("Mode")
    ## returns ModeXY
    mode_number = myentrys[mode_index+4:myentrys.find('_',mode_index)]
    ## add space between mode and the number
    mode_string = "Mode" + mode_number
    mode_string_space = "Mode " + mode_number

    ## build the legend and label
    legend = version
    label = sversion
    legend += ", " + mode_string_space
    label += "_" + mode_string
    if bitComp:
        legend += ", Compr."
        label += "_Compressed"
    else:
        legend += ", Uncompr."
        label += "_Uncompressed"

    mydict[label] = [filename, legend]

pp = pprint.PrettyPrinter(indent=1)
pp.pprint(mydict)
