#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
from ROOT import *
from termcolor import colored
from ROOT import gROOT
from optparse import OptionParser,OptionGroup
from helpers import *
from datetime import datetime
from trainingDict import *
from tdrstyle import *
from CMS_lumi import *
from efficiencyPlots import *
from occupancyPlots import *
from resolutionPlots import *

if __name__ == '__main__':

  ## Configuration settings
  parser = OptionParser()
  parser.add_option('--batchMode', dest='batchMode', action='store_true',default = True)
  parser.add_option("--addDateTime", dest="addDateTime", action="store_true", default = True)
  parser.add_option("--useEtaSlices", dest="useEtaSlices", action="store_true", default = False)
  parser.add_option("--single_pt", dest="single_pt", action="store_true", default = False)
  parser.add_option("--effVsPt", dest="effVsPt", action="store_true", default = False)
  parser.add_option("--effVsEta", dest="effVsEta", action="store_true", default = False)
  parser.add_option("--effVsPhi", dest="effVsPhi", action="store_true", default = False)
  parser.add_option("--res1DvsPt", dest="res1DvsPt", action="store_true", default = False)
  parser.add_option("--res1DvsEta", dest="res1DvsEta", action="store_true", default = False)
  parser.add_option("--res2D", dest="res2D", action="store_true", default = False)
  parser.add_option('--emtfModes',nargs='+', help='Set EMTF modes',
                    default = [15,14,13,11,7,12,10,9,6,5,3])
  parser.add_option('--emtfVersions',nargs='+', help='Set EMTF versions',
                    choices=['Run2','Run3_V1p0','Run3_V1p1','Run3_V1p2'],
                    default = ['Run2','Run3_V1p0','Run3_V1p1','Run3_V1p2'])
  parser.add_option('--etaMins',nargs='+', help='Set eta minima',
                    default = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 1.25])
  parser.add_option('--etaMaxs',nargs='+', help='Set eta maxima',
                    default = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.4])
  parser.add_option('--emtfPtCuts',nargs='+', help='Set pT cuts',
                    default = [5, 7, 10, 12, 15, 20, 22])
  parser.add_option("--treeName", dest="treeName", action="store", default = "f_logPtTarg_invPtWgt/TestTree")
  parser.add_option("--verbosity", dest="verbosity", action="store", default = 1, type=int)
  parser.add_option("--etaSlices", dest="etaSlices", action="store_true", default = False)

  (options, args) = parser.parse_args()

  ## Run in quiet mode
  if options.batchMode:
    sys.argv.append('-b')
    gROOT.SetBatch(1)

  if options.verbosity >= 1:
    print(colored("Configuring:", 'blue'))

    ## all data files have the same tree name
    print(colored("- Using Tree name: {}".format(options.treeName), 'blue'))

  ## default output directory takes a date and time
  currentDateTime = datetime.now().strftime("%Y%m%d_%H%M%S")
  plotDir = "plots_{}_TEST/".format(currentDateTime)
  if options.verbosity >= 1:
    print(colored("- Using output directory {}".format(plotDir), 'blue'))

    ## EMTF modes
    print(colored("- Analyzing EMTF modes {}".format(options.emtfModes), 'blue'))
    for p in options.emtfModes:
      if not p in [15,14,13,11,7,12,10,9,6,5,3]:
        sys.exit("Error: Invalid EMTF mode chosen {}".format(p))

    ## EMTF versions
    print(colored("- Analyzing EMTF versions {}".format(options.emtfVersions), 'blue'))

    ## EMTF pT thresholds
    print(colored("- Analyzing EMTF pT thresholds {}".format(options.emtfPtCuts), 'blue'))

    ## eta minima and maxima
    print(colored("- Analyzing eta slices with minima {}".format(options.etaMins), 'blue'))
    print(colored("- Analyzing eta slices with maxima {}".format(options.etaMaxs), 'blue'))

  ## Set proper ROOT style for plots...
  iPeriod = 0
  iPos = 0
  if( iPos==0 ): CMS_lumi.relPosX = 0.12
  setTDRStyle()

  if options.verbosity >= 1:
    print(colored("- Setting TDR style for plots\n", 'blue'))

  ## get testing data for each mode
  for emtfMode in options.emtfModes:

    if options.verbosity >= 1:
      print(colored("Analyzing EMTF Mode {}".format(emtfMode), 'blue'))

    ## need option to consider uncompressed or compressed
    trainings = []
    for emtfVersion in options.emtfVersions:
      trainings.append("{}_Mode{}_Compressed".format(emtfVersion, emtfMode))
    if options.verbosity >= 1:
      print(colored("{}".format(trainings), 'blue'))

    eventTrees = []
    for p in trainings:
      tTree = TChain(options.treeName)
      tTree.Add(trainingDict[p][0])
      eventTrees.append(tTree)

    legendEntries = []
    for p in trainings:
      legendEntries.append(trainingDict[p][1])

    ## create a simple helper object to attach attributes to
    class Plotter():
      def __init__(self, emtfMode, options, eventTrees, legendEntries, plotDir):
        self.options = options
        self.emtfMode = emtfMode
        self.eventTrees = eventTrees
        self.legendEntries = legendEntries
        self.plotDir = plotDir
        self.emtfColors = [kBlue, kRed, kGreen+2, kBlack]
        self.emtfDrawOptions = ["", "same", "same", "same"]
        self.iPos = iPos
        self.iPeriod = iPeriod

    myPlotter = Plotter(emtfMode, options, eventTrees, legendEntries, plotDir)

    plotEfficienciesSingleMode(myPlotter)
    #plotResolutionsSingleMode(myPlotter)

  """
## Data


markerStyles = [8,8,8,8,8]#,8,8]
drawOptions = ["AP", "same", "same", "same", "same"]#, "same", "same", "same", "same"]
drawOptions1D = ["", "same"]#, "same", "same", "same", "same"]
outFileString = ["Run2_dPhi12_23_34","Run3_dPhi12_23_34"]#, "Run3_bend1_bitCompr"]#"Run3QSBit", "Run3QSBitESBit"]

"""
