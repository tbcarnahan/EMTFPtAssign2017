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
import CMS_lumi as CMS_lumi
from efficiencyPlots import *
from occupancyPlots import *
from resolutionPlots import *

if __name__ == '__main__':

  ## Configuration settings
  parser = OptionParser()
  parser.add_option('--batchMode', dest='batchMode', action='store_true',default = True)
  parser.add_option("--addDateTime", dest="addDateTime", action="store_true", default = True)
  parser.add_option("--eta_slices", dest="eta_slices", action="store_true", default = False)
  parser.add_option("--single_pt", dest="single_pt", action="store_true", default = False)
  parser.add_option("--effVsPt", dest="effVsPt", action="store_true", default = False)
  parser.add_option("--effVsEta", dest="effVsEta", action="store_true", default = False)
  parser.add_option("--effVsPhi", dest="effVsPhi", action="store_true", default = False)
  parser.add_option("--res1DvsPt", dest="res1DvsPt", action="store_true", default = False)
  parser.add_option("--res1DvsEta", dest="res1DvsEta", action="store_true", default = False)
  parser.add_option("--res2D", dest="res2D", action="store_true", default = False)
  parser.add_option('--emtfModes',nargs='+', help='Set EMTF modes',
                    choices=[15,14,13,11,7,12,10,9,6,5,3],
                    default = [15,14,13,11,7,12,10,9,6,5,3])
  parser.add_option('--training',nargs='+', help='Set trainings', choices = trainingChoices, default = [])
  parser.add_option('--emtfVersions',nargs='+', help='Set EMTF versions',
                    choices=['Run2','Run3_V1p0','Run3_V1p1','Run3_V1p2'],
                    default = ['Run2','Run3_V1p0','Run3_V1p1','Run3_V1p2'])
  (options, args) = parser.parse_args()

  ## Run in quiet mode
  if options.batchMode:
    sys.argv.append('-b')
    gROOT.SetBatch(1)

  ## default output directory takes a date and time
  currentDateTime = datetime.now().strftime("%Y%m%d_%H%M%S")
  plotDir = "plots_{}_TEST/".format(currentDateTime)
  print(colored("Using output directory {}\n".format(plotDir), 'blue'))

  ## EMTF modes
  print(colored("Analyzing EMTF modes {}\n".format(options.emtfModes), 'blue'))

  ## EMTF versions
  print(colored("Analyzing EMTF versions {}\n".format(options.emtfVersions), 'blue'))

  #setTDRStyle()

  plotEfficiencies(options)

"""
iPeriod = 0
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

if options.single_pt:
  pt_cut = [22]
  pt_str = ["22"]
else:
  pt_cut = [3, 5, 7, 10, 12, 15, 20, 22, 24, 27]
  pt_str = ["3", "5", "7", "10", "12", "15", "20", "22", "24", "27"]

if options.eta_slices:
  eta_min = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
  eta_max = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
  eta_str_min = ["1pt2", "1pt4", "1pt6", "1pt8", "2pt0", "2pt2"]
  eta_str_max = ["1pt4", "1pt6", "1pt8", "2pt0", "2pt2", "2pt4"]
else:
  #Whole endcap region.
  eta_min = [1.25]
  eta_max = [2.4]
  eta_str_min = ["1pt25"]
  eta_str_max = ["2pt4"]


## Data

trainings= [
  'Run2_Mode15_Compressed',
  'Run3_V1p0_Mode15_Compressed',
  'Run3_V1p1_Mode15_Compressed',
  'Run3_V1p2_Mode15_Compressed'
]

treeName = "f_logPtTarg_invPtWgt/TestTree"

evt_trees = []
for p in trainings:
  ttree = TChain(treeName)
  print("Reading file: {}".format(trainingDict[p][0]))
  ttree.Add(trainingDict[p][0])
  evt_trees.append(ttree)

legendEntries = []
for p in trainings:
  legendEntries.append(trainingDict[p][1])

markerColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
lineColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
markerStyles = [8,8,8,8,8]#,8,8]
drawOptions = ["AP", "same", "same", "same", "same"]#, "same", "same", "same", "same"]
drawOptions1D = ["", "same"]#, "same", "same", "same", "same"]
outFileString = ["Run2_dPhi12_23_34","Run3_dPhi12_23_34"]#, "Run3_bend1_bitCompr"]#"Run3QSBit", "Run3QSBitESBit"]

"""
