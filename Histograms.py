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


## ============== Event branches================
evt_tree  = TChain('FlatNtupleMC/tree')
out_file  = TFile('Histograms.root','recreate')

## ================ Read input files, define Output file ======================
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'

file_name = dir1+"EMTF_MC_NTuple_SingleMu_20200522.root" 
evt_tree.Add(file_name)


#Initialize histograms
h_1D_GE11ME11 = TH1D('h_1D_GE11ME11', '', 128, -0.17, 0.17)
h_1D_GE11ME11_100 = TH1D('h_1D_GE11ME11_100', '', 64, -0.17, 0.17) #pt < 100 GeV

h_1D_GE11ME11pp = TH1D('h_1D_GE11ME11pp', '', 128, -0.17, 0.17) #+muon in +endcap
h_1D_GE11ME11pn = TH1D('h_1D_GE11ME11pn', '', 128, -0.17, 0.17) #-muon in +endcap
h_1D_GE11ME11np = TH1D('h_1D_GE11ME11np', '', 128, -0.17, 0.17) #+muon in -endcap
h_1D_GE11ME11nn = TH1D('h_1D_GE11ME11nn', '', 128, -0.17, 0.17) #-muon in -endcap

h_1D_GE11ME11_pt5 = TH1D('h_1D_GE11ME11_pt5', '', 128, -0.17, 0.17) #pt < 5 GeV
h_1D_GE11ME11_pt20to30 = TH1D('h_1D_GE11ME11_pt20to30', '', 128, -0.17, 0.17) #20 < pt < 30 GeV


for iEvt in range(2000000):
#for iEvt in range(evt_tree.GetEntries()): #Full dataset is roughly 8 million events 
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  ME1p = 0 ; ME2p = 0 ; ME3p = 0 ; ME11p = 0 ; GE11p = 0 #Phi for hit in positive endcap
  ME1n = 0 ; ME2n = 0 ; ME3n = 0 ; ME11n = 0 ; GE11n = 0 #Phi for hit in negative endcap

  for i in range(len(evt_tree.hit_station)):

    '''
    #if evt_tree.hit_subsector[i] == 1 or evt_tree.hit_subsector[i] == 2:  #hit in ME1
    if evt_tree.hit_isCSC[i] == 1 and evt_tree.hit_station[i] == 1:
      if evt_tree.hit_eta[i]>0: ME1p = evt_tree.hit_phi[i] #Save ME1 hit in positive endcap
      if evt_tree.hit_eta[i]<0: ME1n = evt_tree.hit_phi[i] #Save ME1 hit in negative endcap

    #if evt_tree.hit_subsector[i] == 0 and evt_tree.hit_station[i] == 2:   #hit in ME2
    if evt_tree.hit_isCSC[i] == 1 and evt_tree.hit_station[i] == 2:
      if evt_tree.hit_eta[i]>0: ME2p = evt_tree.hit_phi[i]
      if evt_tree.hit_eta[i]<0: ME2n = evt_tree.hit_phi[i]

    #if evt_tree.hit_subsector[i] == 0 and evt_tree.hit_station[i] == 3:   #hit in ME3
    if evt_tree.hit_isCSC[i] == 1 and evt_tree.hit_station[i] == 3:
      if evt_tree.hit_eta[i]>0: ME3p = evt_tree.hit_phi[i]
      if evt_tree.hit_eta[i]<0: ME3n = evt_tree.hit_phi[i]
    '''

    #if evt_tree.hit_isCSC[i] == 1 and (evt_tree.hit_subsector[i] == 1 or evt_tree.hit_subsector[i] == 2) and evt_tree.hit_ring[i] == 1: #hit in ME1/1
    if evt_tree.hit_isCSC[i] == 1 and evt_tree.hit_station[i] == 1 and evt_tree.hit_ring[i] == 1:
      if evt_tree.hit_eta[i]>0: ME11p = evt_tree.hit_phi[i] #Save ME11 hit in positive endcap
      if evt_tree.hit_eta[i]<0: ME11n = evt_tree.hit_phi[i] #Save ME11 hit in negative endcap

    if evt_tree.hit_isGEM[i] == 1 and evt_tree.hit_station[i] == 1 and evt_tree.hit_ring[i] == 1: #hit in GE11
      if evt_tree.hit_eta[i]>0: GE11p = evt_tree.hit_phi[i] #Save GE11 hit in positive endcap
      if evt_tree.hit_eta[i]<0: GE11n = evt_tree.hit_phi[i] #Save GE11 hit in negative endcap



  #Fill histograms for each charge through each endcap.
  for i in range(len(evt_tree.mu_pt)):
    if evt_tree.mu_eta[i]>0 and evt_tree.mu_charge[i]>0 and GE11p!=0 and ME11p!=0: h_1D_GE11ME11pp.Fill(GE11p-ME11p)
    if evt_tree.mu_eta[i]>0 and evt_tree.mu_charge[i]<0 and GE11p!=0 and ME11p!=0: h_1D_GE11ME11pn.Fill(GE11p-ME11p)
    if evt_tree.mu_eta[i]<0 and evt_tree.mu_charge[i]>0 and GE11n!=0 and ME11n!=0: h_1D_GE11ME11np.Fill(GE11n-ME11n)
    if evt_tree.mu_eta[i]<0 and evt_tree.mu_charge[i]<0 and GE11n!=0 and ME11n!=0: h_1D_GE11ME11nn.Fill(GE11n-ME11n)

    if evt_tree.mu_eta[i]>0 and evt_tree.mu_pt[i]<5 and GE11p!=0 and ME11p!=0: h_1D_GE11ME11_pt5.Fill(GE11p-ME11p)
    if evt_tree.mu_eta[i]<0 and evt_tree.mu_pt[i]<5 and GE11n!=0 and ME11n!=0: h_1D_GE11ME11_pt5.Fill(GE11n-ME11n)
    if evt_tree.mu_eta[i]>0 and evt_tree.mu_pt[i]>20 and evt_tree.mu_pt[i]<30 and GE11p!=0 and ME11p!=0: h_1D_GE11ME11_pt20to30.Fill(GE11p-ME11p)
    if evt_tree.mu_eta[i]<0 and evt_tree.mu_pt[i]>20 and evt_tree.mu_pt[i]<30 and GE11n!=0 and ME11n!=0: h_1D_GE11ME11_pt20to30.Fill(GE11n-ME11n)


#Plot histograms, save to output file.
###############################
###############################
#out_file.cd()

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_1D_GE11ME11.Draw()
#h_1D_GE11ME11.SetTitle('GEM-CSC bending angle (GE11-ME11)')
#raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11pp.Draw()
h_1D_GE11ME11pp.SetTitle('GEM-CSC bending angle (GE11-ME11) (Positive muon in positive endcap)')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11pn.Draw()
h_1D_GE11ME11pn.SetTitle('GEM-CSC bending angle (GE11-ME11) (Negative muon in positive endcap)')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11np.Draw()
h_1D_GE11ME11np.SetTitle('GEM-CSC bending angle (GE11-ME11) (Positive muon in negative endcap)')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11nn.Draw()
h_1D_GE11ME11nn.SetTitle('GEM-CSC bending angle (GE11-ME11) (Negative muon in negative endcap)')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11_pt5.Draw()
h_1D_GE11ME11_pt5.SetTitle('GEM-CSC bending angle (GE11-ME11) (p_{T}^{GEN} < 5 GeV)')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_1D_GE11ME11_pt20to30.Draw()
h_1D_GE11ME11_pt20to30.SetTitle('GEM-CSC bending angle (GE11-ME11) (20 < p_{T}^{GEN} < 30 GeV)')
raw_input("Enter")
