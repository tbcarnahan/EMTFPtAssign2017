#! /usr/bin/env python

import argparse
from commonVariables import *
from Run2Variables import *
from Run3Variables import *

def trainVarsSelToHex(trainVariables):
    ## function to return hex string with train variables
    selectedVars = [0] * len(allowedTrainingVars)
    for p in trainVariables:
        if p in allowedTrainingVars:
            selectedVars[allowedTrainingVars.index(p)] = 1

    ## reverse the list
    selectedVars.reverse()
    ## contatenate and turn into a hex string
    selection = "".join([str(p) for p in selectedVars])
    hexsel = hex(int(selection, 2))
    return hexsel

if __name__ == '__main__':

    ## expert options
    parser = argparse.ArgumentParser("Converts a list of training variables to a hexadecimal string")
    parser.add_argument("--isRun2", action="store_true", default = False)
    parser.add_argument("--isRun3Default", action="store_true", default = False)
    parser.add_argument("--emtfMode", action="store", default = 15)
    args = parser.parse_args()

    ## if no selection is provided for Run-2, use the default ones!
    trainVariables = []
    if args.isRun2:
        trainVariables = Run2TrainingVariables[args.emtfMode]
        print("Info: no training variable selection provided for Run-2 with mode {mode}. Using default selection.".format(
            mode = args.emtfMode))

    elif args.isRun3Default:
        trainVariables = Run3TrainingVariables[args.emtfMode]
        print("Info: no training variable selection provided for Run-3 with mode {mode}. Using default selection.".format(
            mode = args.emtfMode))

    print(trainVariables)
    hexkey = trainVarsSelToHex(trainVariables)
    print(hexkey)
