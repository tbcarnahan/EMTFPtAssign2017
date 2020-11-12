# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

print '------> Importing Root File'

## Configuration settings
MAX_EVT  = -1 ## Maximum number of events to process
PRT_EVT  = 10000 ## Print every Nth event
printouts=False

## ============== Event branches ================
evt_tree  = TChain('FlatNtupleMC/tree') ; evt_tree2  = TChain('FlatNtupleMC/tree')

## ================ Read input files ======================
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'

file_name = dir1+"EMTF_MC_NTuple_Run2stubs.root"
file_name2 = dir1+"EMTF_MC_NTuple_Run3stubs.root"
print colored('Loading file: '+file_name, 'green')
print colored('Loading file: '+file_name2, 'green')

evt_tree.Add(file_name)
evt_tree2.Add(file_name2)


## ================ Define histograms ======================
h_pt_denom = TH1D('h_pt_denom', '', 64, 0., 80.)
h_pt_numer = TH1D('h_pt_numer', '', 64, 0., 80.)
h_pt_denom2 = TH1D('h_pt_denom2', '', 64, 0., 80.)
h_pt_numer2 = TH1D('h_pt_numer2', '', 64, 0., 80.)

h_eta_denom = TH1D('h_eta_denom', '', 32, -3., 3.)
h_eta_numer = TH1D('h_eta_numer', '', 32, -3., 3.)
h_eta_denom2 = TH1D('h_eta_denom2', '', 32, -3., 3.)
h_eta_numer2 = TH1D('h_eta_numer2', '', 32, -3., 3.)


## ================ Printouts for debugging ======================
if printouts==True:
  for iEvt in range(10000):
    evt_tree.GetEntry(iEvt)
    for i in range(len(evt_tree.mu_pt)):
      print "Gen muon",i, " pt, eta, phi: ", evt_tree.mu_pt[i], evt_tree.mu_eta[i], evt_tree.mu_phi[i]
    print '--------'
    for i in range(len(evt_tree.trk_pt)):
      print "L1 muon",i, " pt, eta, phi, quality, nNeighbor: ", evt_tree.trk_pt[i], evt_tree.trk_eta[i], evt_tree.trk_phi[i], evt_tree.trk_quality[i], evt_tree.trk_nNeighbor[i]
    #for i in range(len(evt_tree.hit_phi)):
      #if evt_tree.hit_station[i]==1: print evt_tree.hit_phi[i], evt_tree.hit_neighbor[i]
    print '------Next event------'


## ================ Event loop ======================
for iEvt in range(500000):
#for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt) ; evt_tree2.GetEntry(iEvt)

  for i in range(len(evt_tree.mu_pt)):
    #Fill histogram denominators
    if abs(evt_tree.mu_eta[i])>1.0 and abs(evt_tree.mu_eta[i])<2.5: h_pt_denom.Fill(evt_tree.mu_pt[i])  
    if abs(evt_tree2.mu_eta[i])>1.0 and abs(evt_tree2.mu_eta[i])<2.5: h_pt_denom2.Fill(evt_tree2.mu_pt[i])  

    if evt_tree.mu_pt[i]>20: h_eta_denom.Fill(evt_tree.mu_eta[i])
    if evt_tree2.mu_pt[i]>20: h_eta_denom2.Fill(evt_tree2.mu_eta[i])

    #Fill histogram numerators by looking for a Level-1 match.
    for j in range(len(evt_tree.trk_pt)):

      #To match, check for same endcap and ignore duplicates.
      if evt_tree.mu_eta[i]*evt_tree.trk_eta[j]>0 and abs(evt_tree.mu_eta[i])>1.0 and abs(evt_tree.mu_eta[i])<2.5:
	if evt_tree.trk_pt[j]>20. and evt_tree.trk_nNeighbor[j]==0: h_pt_numer.Fill(evt_tree.mu_pt[i])
	if evt_tree.trk_pt[j]>20. and evt_tree.mu_pt[i]>20. and evt_tree.trk_nNeighbor[j]==0: h_eta_numer.Fill(evt_tree.mu_eta[i])

    for j in range(len(evt_tree2.trk_pt)):
      if evt_tree2.mu_eta[i]*evt_tree2.trk_eta[j]>0 and abs(evt_tree2.mu_eta[i])>1.0 and abs(evt_tree2.mu_eta[i])<2.5:
	if evt_tree2.trk_pt[j]>20. and evt_tree2.trk_nNeighbor[j]==0: h_pt_numer2.Fill(evt_tree2.mu_pt[i])
	if evt_tree2.trk_pt[j]>20. and evt_tree2.mu_pt[i]>20. and evt_tree2.trk_nNeighbor[j]==0: h_eta_numer2.Fill(evt_tree2.mu_eta[i])

	
## ================ Plot/save histograms ======================

c1 = TCanvas("c1")
h_eta_numer.Divide(h_eta_denom) ; h_eta_numer2.Divide(h_eta_denom2)
h_eta_numer.SetTitle("Trigger efficiency (p_{T}^{L1}, p_{T}^{GEN} > 20 GeV)")
h_eta_numer.GetXaxis().SetTitle("#eta")
gStyle.SetOptStat(0)
h_eta_numer.Draw() ; h_eta_numer2.SetLineColor(2) ; h_eta_numer2.Draw("same")
raw_input("Enter")
c1.SaveAs('validation_november/eff_eta_pt20.png')
c1.Close()

c1 = TCanvas("c1")
h_pt_numer.Divide(h_pt_denom) ; h_pt_numer2.Divide(h_pt_denom2)
h_pt_numer.SetTitle("Trigger efficiency (p_{T}^{L1} > 20 GeV)")
h_pt_numer.GetXaxis().SetTitle("p_{T}^{GEN} (GeV)")
gStyle.SetOptStat(0)
h_pt_numer.Draw() ; h_pt_numer2.SetLineColor(2) ; h_pt_numer2.Draw("same")
raw_input("Enter")
c1.SaveAs('validation_november/eff_pt20.png')
c1.Close()

