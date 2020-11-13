# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

## ============= Settings ===============
printouts=False

## ================ Read input files ====
print '------> Importing Root File'
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
file_name = dir1+"EMTF_MC_NTuple_Run3stubs_2.root" #Input file w/ Run3 stubs
print colored('Loading file: '+file_name, 'green')


## ============= Read in the TTrees ======
evt_tree = TChain('FlatNtupleMC/tree') ; evt_tree.Add(file_name)
#evt_tree2 = TChain('tree') ; evt_tree2.Add(file_name)

## ============= Printouts ===============
if printouts==True:
  for iEvt in range(1000):
    evt_tree.GetEntry(iEvt)
    #for i in range(len(evt_tree.mu_pt)):
      #print "Gen muon",i, " pt, eta, phi: ", evt_tree.mu_pt[i], evt_tree.mu_eta[i], evt_tree.mu_phi[i]
    print '--------'
    #for i in range(len(evt_tree.trk_pt)):
      #print "L1 muon",i, " pt, eta, phi, nNeighbor: ", evt_tree.trk_pt[i], evt_tree.trk_eta[i], evt_tree.trk_phi[i], evt_tree.trk_nNeighbor[i]
    for i in range(len(evt_tree.hit_phi)):
      if evt_tree.hit_station[i]==3: print evt_tree.hit_phi[i], evt_tree.hit_neighbor[i], evt_tree.hit_quality[i]
    print '------Next event------'

## ============== Add branch macro ================

outfile = TFile(file_name, "update")

hit_phi_St1 = array( 'f', [0.,0.]) ; hit_phi_St2 = array( 'f', [0.,0.]) ; hit_phi_St3 = array( 'f', [0.,0.]) ; hit_phi_St4 = array( 'f', [0.,0.])
mytree = TTree('tree', 'tree')
#mytree.SetEntries(evt_tree.GetEntries())
mytree.SetEntries(500000)

hit_St1_br = mytree.Branch("hit_phi_St1", hit_phi_St1, 'hit_phi_St1/F')
hit_St2_br = mytree.Branch("hit_phi_St2", hit_phi_St2, 'hit_phi_St2/F')
hit_St3_br = mytree.Branch("hit_phi_St3", hit_phi_St3, 'hit_phi_St3/F')
hit_St4_br = mytree.Branch("hit_phi_St4", hit_phi_St4, 'hit_phi_St4/F')

#for iEvt in range(evt_tree.GetEntries()):
for iEvt in range(500000):
  evt_tree.GetEntry(iEvt)

  for i in range(len(evt_tree.hit_phi)):
    if evt_tree.hit_station[i]==1 and evt_tree.hit_endcap[i]>0: hit_phi_St1[0] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==1 and evt_tree.hit_endcap[i]<0: hit_phi_St1[1] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==2 and evt_tree.hit_endcap[i]>0: hit_phi_St2[0] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==2 and evt_tree.hit_endcap[i]<0: hit_phi_St2[1] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==3 and evt_tree.hit_endcap[i]>0: hit_phi_St3[0] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==3 and evt_tree.hit_endcap[i]<0: hit_phi_St3[1] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==4 and evt_tree.hit_endcap[i]>0: hit_phi_St4[0] = evt_tree.hit_phi[i]
    if evt_tree.hit_station[i]==4 and evt_tree.hit_endcap[i]<0: hit_phi_St4[1] = evt_tree.hit_phi[i]
  

  hit_St1_br.Fill() ; hit_St2_br.Fill() ; hit_St3_br.Fill() ; hit_St4_br.Fill() ;

outfile.Write() ; outfile.Close()


'''
c1 = TCanvas("c1")
evt_tree.Draw("hit_phi>>h1(256,-180.,180.)", "hit_station==1 && hit_neighbor==0 & hit_quality!=-999")
h1=gROOT.FindObject("h1")
c1.Update()
evt_tree2.Draw("hit_phi_St1>>h2(256,-180.,180.)")
h2=gROOT.FindObject("h2")
c1.Update()
h1.Draw() ; h2.SetLineColor(2) ; h2.Draw("same")
raw_input("Enter")
'''