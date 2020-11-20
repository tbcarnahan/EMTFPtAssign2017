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

## ============== Event Tree ================
evt_tree  = TChain('FlatNtupleMC/tree')

## ================ Read input file ======================
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/' 
file_name = dir1+"EMTF_MC_NTuple_Run3stubs.root"
evt_tree.Add(file_name)

## ============== Initialise histograms ================
h_patterns_ME1 = TH1D('h_patterns_ME1', '', 11, 0, 11)
h_patterns_ME2 = TH1D('h_patterns_ME2', '', 11, 0, 11)
h_patterns_ME3 = TH1D('h_patterns_ME3', '', 11, 0, 11)
h_patterns_ME4 = TH1D('h_patterns_ME4', '', 11, 0, 11)

h_dPhi12 = TH1D('h_dPhi12', '', 64, -0.15, 0.15)
h_dPhi23 = TH1D('h_dPhi23', '', 64, -0.15, 0.15)
h_dPhi34 = TH1D('h_dPhi34', '', 64, -0.15, 0.15)
h_dTheta12 = TH1D('h_dTheta12', '', 64, -0.1, 0.1)
h_dTheta23 = TH1D('h_dTheta23', '', 64, -0.1, 0.1)
h_dTheta34 = TH1D('h_dTheta34', '', 64, -0.1, 0.1)

h_dPhi12_dPhi23 = TH2D('h_dPhi12_dPhi23', '', 32, -0.005, 0.005, 32, -0.005, 0.005)
h_dPhi12_dPhi34 = TH2D('h_dPhi12_dPhi34', '', 32, -0.005, 0.005, 32, -0.005, 0.005)
h_dPhi23_dPhi34 = TH2D('h_dPhi23_dPhi34', '', 32, -0.005, 0.005, 32, -0.005, 0.005)

h_dPhi12_pt = TH2D('h_dPhi12_pt', '', 64, 1, 50, 64, -0.15, 0.15)
h_dPhi23_pt = TH2D('h_dPhi23_pt', '', 64, 1, 50, 64, -0.15, 0.15)
h_dPhi34_pt = TH2D('h_dPhi34_pt', '', 64, 1, 50, 64, -0.15, 0.15)
h_dTheta12_pt = TH2D('h_dTheta12_pt', '', 64, 1, 50, 64, -0.15, 0.15)
h_dTheta23_pt = TH2D('h_dTheta23_pt', '', 64, 1, 50, 64, -0.15, 0.15)
h_dTheta34_pt = TH2D('h_dTheta34_pt', '', 64, 1, 50, 64, -0.15, 0.15)

h_dPhi12_patternME1 = TH2D('h_dPhi12_patternME1', '', 11, 0, 11, 32, -0.15, 0.15)
h_dPhi12_patternME2 = TH2D('h_dPhi12_patternME2', '', 11, 0, 11, 32, -0.15, 0.15)
h_dPhi23_patternME2 = TH2D('h_dPhi23_patternME2', '', 11, 0, 11, 32, -0.15, 0.15)
h_dPhi23_patternME3 = TH2D('h_dPhi23_patternME3', '', 11, 0, 11, 32, -0.15, 0.15)
h_dPhi34_patternME3 = TH2D('h_dPhi34_patternME3', '', 11, 0, 11, 32, -0.15, 0.15)
h_dPhi34_patternME4 = TH2D('h_dPhi34_patternME4', '', 11, 0, 11, 32, -0.15, 0.15)

## ============== Event loop ================

for iEvt in range(2000000):
#for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  #A macro that picks out specific station LCT info and fill histograms.
  for j in range(len(evt_tree.mu_pt)):
    ME1_phi=0 ; ME2_phi=0 ; ME3_phi=0 ; ME4_phi=0
    #pattern_ME1=0 ; pattern_ME2=0 ; pattern_ME3=0 ; pattern_ME4=0
    #ME1_theta=0 ; ME2_theta=0 ; ME3heta_p=0 ; ME4heta_p=0
    
    for i in range(len(evt_tree.hit_station)):
      #If running over low pT muons, uncomment pT cut.
      if evt_tree.hit_neighbor[i]==0 and evt_tree.hit_isCSC[i]==1 and evt_tree.hit_eta[i]*evt_tree.mu_eta[j]>0:# and evt_tree.mu_pt[j]<=15:

	#Phi-position values
	if evt_tree.hit_station[i]==1: ME1_phi = evt_tree.hit_phi[i]
	if evt_tree.hit_station[i]==2: ME2_phi = evt_tree.hit_phi[i]
	if evt_tree.hit_station[i]==3: ME3_phi = evt_tree.hit_phi[i]
	if evt_tree.hit_station[i]==4: ME4_phi = evt_tree.hit_phi[i]

	'''
	#Theta-position values
	if evt_tree.hit_station[i]==1: ME1_theta = evt_tree.hit_theta[i]
	if evt_tree.hit_station[i]==2: ME2_theta = evt_tree.hit_theta[i]
	if evt_tree.hit_station[i]==3: ME3_theta = evt_tree.hit_theta[i]
	if evt_tree.hit_station[i]==4: ME4_theta = evt_tree.hit_theta[i]
	
	#Patterns
	if evt_tree.hit_station[i]==1: pattern_ME1=evt_tree.hit_pattern[i]
	if evt_tree.hit_station[i]==2: pattern_ME2=evt_tree.hit_pattern[i]
	if evt_tree.hit_station[i]==3: pattern_ME3=evt_tree.hit_pattern[i]
	if evt_tree.hit_station[i]==4: pattern_ME4=evt_tree.hit_pattern[i]
	'''

    #2D correlations for phi-position bendings
    if (ME1_phi * ME2_phi * ME3_phi)!=0: h_dPhi12_dPhi23.Fill((ME2_phi - ME3_phi)*np.pi/180., (ME1_phi - ME2_phi)*np.pi/180.)
    if (ME2_phi * ME3_phi * ME4_phi)!=0: h_dPhi23_dPhi34.Fill((ME3_phi - ME4_phi)*np.pi/180., (ME2_phi - ME3_phi)*np.pi/180.)
    if (ME1_phi * ME2_phi * ME3_phi * ME4_phi_p)!=0: h_dPhi12_dPhi34.Fill((ME3_phi - ME4_phi)*np.pi/180., (ME1_phi - ME2_phi)*np.pi/180.)

    '''
    #2D correlations for phi-postion vs patterns
    if (ME1_phi * ME2_phi * pattern_ME1)!=0: h_dPhi12_patternME1.Fill(pattern_ME1, (ME1_phi - ME2_phi)*np.pi/180.)
    if (ME1_phi * ME2_phi * pattern_ME2)!=0: h_dPhi12_patternME2.Fill(pattern_ME2, (ME1_phi - ME2_phi)*np.pi/180.)
    if (ME2_phi * ME3_phi * pattern_ME2)!=0: h_dPhi23_patternME2.Fill(pattern_ME2, (ME2_phi - ME3_phi)*np.pi/180.)
    if (ME2_phi * ME3_phi * pattern_ME3)!=0: h_dPhi23_patternME3.Fill(pattern_ME3, (ME2_phi - ME3_phi)*np.pi/180.)
    if (ME3_phi * ME4_phi * pattern_ME3)!=0: h_dPhi34_patternME3.Fill(pattern_ME3, (ME3_phi - ME4_phi)*np.pi/180.)
    if (ME3_phi * ME4_phi * pattern_ME4)!=0: h_dPhi34_patternME4.Fill(pattern_ME4, (ME3_phi - ME4_phi)*np.pi/180.)

    #Fill dPhi bendings into 1D histograms.
    if (ME1_phi * ME2_phi)!=0: h_dPhi12.Fill((ME1_phi - ME2_phi)*np.pi/180.)
    if (ME2_phi * ME3_phi)!=0: h_dPhi23.Fill((ME2_phi - ME3_phi)*np.pi/180.)
    if (ME3_phi_* ME4_phi)!=0: h_dPhi34.Fill((ME3_phi - ME4_phi)*np.pi/180.)

    #dTheta bendings 1D histograms.
    if (ME1_theta * ME2_theta)!=0: h_dTheta12.Fill((ME1_theta - ME2_theta)*np.pi/180.)
    if (ME2_theta * ME3_theta)!=0: h_dTheta23.Fill((ME2_theta - ME3_theta)*np.pi/180.)
    if (ME3_theta * ME4_theta)!=0: h_dTheta34.Fill((ME3_theta - ME4_theta)*np.pi/180.)

    #Phi-position bending vs pT 2D histograms.
    if (ME1_phi * ME2_phi)!=0: h_dPhi12_pt.Fill(evt_tree.mu_pt[j], (ME1_phi - ME2_phi)*np.pi/180.)
    if (ME2_phi * ME3_phi)!=0: h_dPhi23_pt.Fill(evt_tree.mu_pt[j], (ME2_phi - ME3_phi)*np.pi/180.)
    if (ME3_phi * ME4_phi)!=0: h_dPhi34_pt.Fill(evt_tree.mu_pt[j], (ME3_phi - ME4_phi)*np.pi/180.)
  
    #Theta-position bending vs pT 2D histogram
    if (ME1_theta * ME2_theta)!=0: h_dTheta12_pt.Fill(evt_tree.mu_pt[j], (ME1_theta - ME2_theta)*np.pi/180.)
    if (ME2_theta * ME3_theta)!=0: h_dTheta23_pt.Fill(evt_tree.mu_pt[j], (ME2_theta - ME3_theta)*np.pi/180.)
    if (ME3_theta * ME4_theta)!=0: h_dTheta34_pt.Fill(evt_tree.mu_pt[j], (ME3_theta - ME4_theta)*np.pi/180.)
    '''


#-------------------------------------
#2D correlations of phi-position bendings
#-------------------------------------
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPhi12_dPhi23.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_dPhi12_dPhi23.SetTitle('dPhi_{12} vs dPhi_{23}')
h_dPhi12_dPhi23.GetXaxis().SetTitle('dPhi_{23} (radians)') ; h_dPhi12_dPhi23.GetYaxis().SetTitle('dPhi_{12} (radians)')
h_dPhi12_dPhi23.Write()
c1.SaveAs('validation_november/dPhi12_dPhi23.png')
#raw_input("Enter")
c1.Close()

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPhi12_dPhi34.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_dPhi12_dPhi34.SetTitle('dPhi_{12} vs dPhi_{34}')
h_dPhi12_dPhi34.GetXaxis().SetTitle('dPhi_{34} (radians)') ; h_dPhi12_dPhi34.GetYaxis().SetTitle('dPhi_{12} (radians)')
h_dPhi12_dPhi34.Write()
c1.SaveAs('validation_november/dPhi12_dPhi34.png')
#raw_input("Enter")
c1.Close()

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPhi23_dPhi34.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_dPhi23_dPhi34.SetTitle('dPhi_{23} vs dPhi_{34}')
h_dPhi23_dPhi34.GetXaxis().SetTitle('dPhi_{34} (radians)') ; h_dPhi23_dPhi34.GetYaxis().SetTitle('dPhi_{23} (radians)')
h_dPhi23_dPhi34.Write()
c1.SaveAs('validation_november/dPhi23_dPhi34.png')
#raw_input("Enter")
c1.Close()


'''
#-------------------------------------
#2D correlation of phi-position bending and pattern
#-------------------------------------
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPhi12_patternME1.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_dPhi12_patternME1.SetTitle('dPhi_{12} vs ME1 CLCT Pattern')
h_dPhi12_patternME1.GetXaxis().SetTitle('Pattern') ; h_dPhi12_patternME1.GetYaxis().SetTitle('dPhi_{12} (radians)')
h_dPhi12_patternME1.Write()
c1.SaveAs('validation_november/dPhi12_patternME1_pt15.png')
#raw_input("Enter")
c1.Close()


#-------------------------------------
#2D Correlations of dPhi position bend and pT.
#-------------------------------------
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPhi12_pt.Draw("colz")
gStyle.SetOptStat(0)
h_dPhi12_pt.SetTitle('dPhi_{12} vs p_{T}^{GEN}')
h_dPhi12_pt.GetXaxis().SetTitle('p_{T} (GeV)') ; h_dPhi12_pt.GetYaxis().SetTitle('dPhi_{12} (radians)')
h_dPhi12_pt.SetOption("colz")
h_dPhi12_pt.Write()
c1.SaveAs('validation_november/dPhi12_pt.png')
#raw_input("Enter")



#-------------------------------------
#2D Correlation of dTheta and pT.
#-------------------------------------
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dTheta12_pt.Draw("colz")
gStyle.SetOptStat(0)
h_dTheta12_pt.SetTitle('dTheta_{12} vs p_{T}^{GEN}')
h_dTheta12_pt.GetXaxis().SetTitle('p_{T} (GeV)') ; h_dTheta12_pt.GetYaxis().SetTitle('dTheta_{12} (radians)')
h_dTheta12_pt.SetOption("colz")
h_dTheta12_pt.Write()
c1.SaveAs('validation_november/dTheta12_pt.png')
#raw_input("Enter")



#-------------------------------------
#1D Histograms
#-------------------------------------
#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_dTheta12.Draw()
#h_dTheta12.SetTitle('dTheta_{12} (radians)')
#c1.SaveAs('validation_november/dTheta12.png')
#raw_input("Enter")


#Plots for CLCT patterns per ME station
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_patterns_ME1.Draw()
h_patterns_ME1.SetTitle('ME1 CLCT pattern occupany (p_{T}^{GEN} < 5 GeV)')
c1.SaveAs('validation_november/patterns_ME1_pt5.png')
#raw_input("Enter")

'''
