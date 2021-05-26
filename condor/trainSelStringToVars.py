#! /usr/bin/env python

import argparse
from commonVariables import *
from Run2Variables import *
from Run3Variables import *

def selHexToTrainVars(selHex):
    nBits = len(allowedTrainingVars)
    maxBit = nBits - 1
    bitstring = str(bin(int(selHex, 16))[2:].zfill(nBits))
    selectedVars = []
    for idx in xrange(len(bitstring)-1,-1,-1):
        if int(bitstring[idx]):
            selectedVars.append(allowedTrainingVars[nBits - idx])
    return selectedVars

if __name__ == '__main__':

    ## expert options
    parser = argparse.ArgumentParser()
    parser.add_argument("--hex", action="store", default = 0x0)
    args = parser.parse_args()

    chosenTrainVariables = selHexToTrainVars(args.hex)
    print(chosenTrainVariables)
