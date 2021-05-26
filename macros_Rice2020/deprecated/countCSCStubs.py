# -*- coding: utf-8 -*-
print '------> Setting Environment'
import sys
import math
import ROOT
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

## run quiet mode
sys.argv.append( '-b' )
gROOT.SetBatch(1)

nEntries = -1000000

## ================ Read input files ======================
oldfile = ROOT.TFile.Open("root://cmsxrootd-site.fnal.gov///store/user/mdecaro/Ntuples/EMTF_MC_NTuple_01062021.root")
run2_tree = oldfile.Get("FlatNtupleMCRun2").Get("tree")
run3_tree = oldfile.Get("FlatNtupleMC").Get("tree")

newfile = ROOT.TFile("EMTF_MC_NTuple_Match_20210121.root","RECREATE")
print run2_tree, run3_tree
newtree = run2_tree.CloneTree(0)
newtree3 = run3_tree.CloneTree(0)

ME_2p = np.empty((1), dtype=bool)
ME_3p = np.empty((1), dtype=bool)
ME_4p = np.empty((1), dtype=bool)

ME_2n = np.empty((1), dtype=bool)
ME_3n = np.empty((1), dtype=bool)
ME_4n = np.empty((1), dtype=bool)

newtree.Branch("ME_2p", ME_2p, 'ME_2p/O')
newtree.Branch("ME_3p", ME_3p, 'ME_3p/O')
newtree.Branch("ME_4p", ME_4p, 'ME_4p/O')

newtree.Branch("ME_2n", ME_2n, 'ME_2n/O')
newtree.Branch("ME_3n", ME_3n, 'ME_3n/O')
newtree.Branch("ME_4n", ME_4n, 'ME_4n/O')

## ================ Event loop ======================
for iEvt in range(0,min(nEntries,run2_tree.GetEntries())):
  run2_tree.GetEntry(iEvt)

  ME1_p = False
  ME2_p = False
  ME3_p = False
  ME4_p = False

  ME1_n = False
  ME2_n = False
  ME3_n = False
  ME4_n = False

  ME_2p[0] = False
  ME_3p[0] = False
  ME_4p[0] = False

  ME_2n[0] = False
  ME_3n[0] = False
  ME_4n[0] = False

  if iEvt%100000 == 0:
    print("Processing event", iEvt)

  for i in range(len(run2_tree.hit_phi)):
    if run2_tree.hit_endcap[i]>0 and run2_tree.hit_neighbor[i]==0 and run2_tree.hit_isCSC == 1:
      if run2_tree.hit_station[i] == 1: ME1_p = True
      if run2_tree.hit_station[i] == 2: ME2_p = True
      if run2_tree.hit_station[i] == 3: ME3_p = True
      if run2_tree.hit_station[i] == 4: ME4_p = True

    if run2_tree.hit_endcap[i]<0 and run2_tree.hit_neighbor[i]==0 and run2_tree.hit_isCSC == 1:
      if run2_tree.hit_station[i] == 1: ME1_n = True
      if run2_tree.hit_station[i] == 2: ME2_n = True
      if run2_tree.hit_station[i] == 3: ME3_n = True
      if run2_tree.hit_station[i] == 4: ME4_n = True

    ## once all are true, break from loop
    if (ME1_p and ME2_p and ME3_p and ME4_p and
        ME1_n and ME2_n and ME3_n and ME4_n): break

  #print(ME1_p,ME1_n,ME2_p,ME2_n,ME3_p,ME3_n,ME4_p,ME4_n)

  ## 2 stub requirement
  ME1_2_p = ME1_p and ME2_p
  ME1_3_p = ME1_p and ME3_p
  ME1_4_p = ME1_p and ME4_p
  ME2_3_p = ME2_p and ME3_p
  ME2_4_p = ME2_p and ME4_p
  ME3_4_p = ME3_p and ME4_p

  ME1_2_n = ME1_n and ME2_n
  ME1_3_n = ME1_n and ME3_n
  ME1_4_n = ME1_n and ME4_n
  ME2_3_n = ME2_n and ME3_n
  ME2_4_n = ME2_n and ME4_n
  ME3_4_n = ME3_n and ME4_n

  ## 3 stub requirement
  ME1_2_3_p = ME1_2_p and ME1_3_p
  ME1_3_4_p = ME1_3_p and ME1_4_p
  ME1_2_4_p = ME1_2_p and ME1_4_p
  ME2_3_4_p = ME2_3_p and ME2_4_p

  ME1_2_3_n = ME1_2_n and ME1_3_n
  ME1_3_4_n = ME1_3_n and ME1_4_n
  ME1_2_4_n = ME1_2_n and ME1_4_n
  ME2_3_4_n = ME2_3_n and ME2_4_n

  ME_2p[0] = ME1_2_p or ME1_3_p or ME1_4_p or ME2_3_p or ME2_4_p or ME3_4_p
  ME_2n[0] = ME1_2_n or ME1_3_n or ME1_4_n or ME2_3_n or ME2_4_n or ME3_4_n

  ME_3p[0] = ME1_2_3_p or ME1_3_4_p or ME1_2_4_p or ME2_3_4_p
  ME_3n[0] = ME1_2_3_n or ME1_3_4_n or ME1_2_4_n or ME2_3_4_n

  ## 4 stub requirement
  ME_4p[0] = ME1_2_3_p and ME1_2_4_p
  ME_4n[0] = ME1_2_3_n and ME1_2_4_n

  #print(ME_2p,ME_2n,ME_3p,ME_3n,ME_4p,ME_4n)
  newtree.Fill()

newfile.mkdir("FlatNtupleMCRun2").cd();
newtree.CopyEntries(run2_tree, nEntries)
newtree.Write()
newfile.Cd("../")

newfile.mkdir("FlatNtupleMC").cd();
newtree3.CopyEntries(run3_tree, nEntries)
newtree3.Write()
newfile.Cd("../")

newfile.Close()
