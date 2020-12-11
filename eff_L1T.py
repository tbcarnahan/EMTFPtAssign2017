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
evt_tree  = TChain('FlatNtupleMC/tree')

## ================ Read input files ======================
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
file_name = dir1+"EMTF_MC_NTuple_Run3stubs.root"
print colored('Loading file: '+file_name, 'green')
evt_tree.Add(file_name)


## ================ Define histograms ======================
h_pt_denom = TH1D('h_pt_denom', '', 100, 1., 100.) ; h_pt_numer = TH1D('h_pt_numer', '', 100, 1., 100.)
h_eta_denom = TH1D('h_eta_denom', '', 128, -3., 3.) ; h_eta_numer = TH1D('h_eta_numer', '', 128, -3., 3.)
h_phi_denom = TH1D('h_phi_denom', '', 64, -180., 180.) ; h_phi_numer = TH1D('h_phi_numer', '', 64, -180., 180.)
h_2D_pt_eta_denom = TH2D('h_2D_pt_eta_denom', '', 128, -3, 3, 80, 1., 80.) ; h_2D_pt_eta_numer = TH2D('h_2D_pt_eta_numer', '', 128, -3, 3, 80, 1., 80.)
h_2D_genpt_l1pt = TH2D('h_2D_genpt_l1pt', '', 100, 1., 100., 100, 1., 100.)
h_2D_mode_eta = TH2D('h_2D_mode_eta', '', 64, 1.24, 2.4, 16, 1., 16.)
h_2D_nstubs_eta = TH2D('h_2D_nstubs_eta', '', 64, 1.24, 2.4, 6, 0., 5.)
h_2D_nstubs_pt = TH2D('h_2D_nstubs_pt', '', 64, 1.24, 2.4, 51, 0., 50.)

## ================ Printouts for debugging ======================
if printouts==True:
  for iEvt in range(1000000):
    evt_tree.GetEntry(iEvt)

    if abs(evt_tree.mu_eta[0])<2.4 and abs(evt_tree.mu_eta[0])>2.3:
      if evt_tree.mu_pt[0]<30 and evt_tree.mu_pt[0]>25:
	for i in range(len(evt_tree.mu_pt)):
	  print "Gen muon",i, " pt, eta, phi: ", evt_tree.mu_pt[i], evt_tree.mu_eta[i], evt_tree.mu_phi[i]
	print '--------'
	for i in range(len(evt_tree.trk_pt)):
	  print "L1 muon",i, " pt, eta, phi, quality, nNeighbor: ", evt_tree.trk_pt[i], evt_tree.trk_eta[i], evt_tree.trk_phi[i], evt_tree.trk_qual[i], evt_tree.trk_nNeighbor[i]
	#for i in range(len(evt_tree.hit_phi)):
	  #if evt_tree.hit_station[i]==1: print evt_tree.hit_phi[i], evt_tree.hit_neighbor[i]
	print '------Next event------'


## ================ Event loop ======================
for iEvt in range(300000):
#for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  
  evt_tree.GetEntry(iEvt)

  ME1_p=0;ME2_p=0;ME3_p=0;ME4_p=0
  ME1_n=0;ME2_n=0;ME3_n=0;ME4_n=0
  flag_p=0 ; flag_n=0

  for i in range(len(evt_tree.hit_phi)):
    if evt_tree.hit_endcap[i]>0 and evt_tree.hit_neighbor[i]==0:
      if evt_tree.hit_station[i]==1: ME1_p+=1
      if evt_tree.hit_station[i]==2: ME2_p+=1
      if evt_tree.hit_station[i]==3: ME3_p+=1
      if evt_tree.hit_station[i]==4: ME4_p+=1

    if evt_tree.hit_endcap[i]<0 and evt_tree.hit_neighbor[i]==0:
      if evt_tree.hit_station[i]==1: ME1_n+=1
      if evt_tree.hit_station[i]==2: ME2_n+=1
      if evt_tree.hit_station[i]==3: ME3_n+=1
      if evt_tree.hit_station[i]==4: ME4_n+=1

  ##2 stub requirement
  if (ME1_p * ME2_p)!=0 or (ME1_p * ME3_p)!=0 or (ME1_p * ME4_p)!=0 or (ME2_p * ME3_p)!=0 or (ME2_p * ME4_p)!=0 or (ME3_p * ME4_p)!=0: flag_p=1
  if (ME1_n * ME2_n)!=0 or (ME1_n * ME3_n)!=0 or (ME1_n * ME4_n)!=0 or (ME2_n * ME3_n)!=0 or (ME2_n * ME4_n)!=0 or (ME3_n * ME4_n)!=0: flag_n=1
  
  ##3 stub requirement
  #if (ME1_p * ME2_p * ME3_p)!=0 or (ME1_p * ME3_p * ME4_p)!=0 or (ME1_p * ME2_p * ME4_p)!=0 or (ME2_p * ME3_p * ME4_p)!=0: flag_p+=1
  #if (ME1_n * ME2_n * ME3_n)!=0 or (ME1_n * ME3_n * ME4_n)!=0 or (ME1_n * ME2_n * ME4_n)!=0 or (ME2_n * ME3_n * ME4_n)!=0: flag_n+=1

  #Count number of stubs
  Nstubs_p = ME1_p + ME2_p + ME3_p + ME4_p
  Nstubs_n = ME1_n + ME2_n + ME3_n + ME4_n

  #Fill Nstubs vs X histograms.
  for i in range(len(evt_tree.mu_eta)):
    if evt_tree.mu_eta[i]>0: 
      h_2D_nstubs_pt.Fill(evt_tree.mu_pt[i], Nstubs_p)
      h_2D_nstubs_eta.Fill(abs(evt_tree.mu_eta[i]), Nstubs_p)
    if evt_tree.mu_eta[i]<0:
      h_2D_nstubs_pt.Fill(evt_tree.mu_pt[i], Nstubs_n) 
      h_2D_nstubs_eta.Fill(abs(evt_tree.mu_eta[i]), Nstubs_n)


  #Efficiency plots and other 2D histograms. Can apply mode selection or number of stub selection.
  for j in range(len(evt_tree.trk_pt)):
    for i in range(len(evt_tree.mu_eta)):
      if (abs(evt_tree.mu_eta[i])>1.24 and abs(evt_tree.mu_eta[i])<2.4):
	#if evt_tree.trk_mode[j]==11 or evt_tree.trk_mode[j]==13 or evt_tree.trk_mode[j]==14 or evt_tree.trk_mode[j]==15:
	if evt_tree.trk_eta[j]*evt_tree.mu_eta[i]>0 and evt_tree.trk_nNeighbor[j]==0 and ((evt_tree.mu_eta[i]>0 and flag_p>0) or (evt_tree.mu_eta[i]<0 and flag_n>0)):
	  
	  h_2D_mode_eta.Fill(abs(evt_tree.mu_eta[i]), evt_tree.trk_mode[j])

	  h_pt_denom.Fill(evt_tree.mu_pt[i]) 
	  h_2D_pt_eta_denom.Fill(evt_tree.mu_eta[i], evt_tree.mu_pt[i])
	  h_2D_genpt_l1pt.Fill(evt_tree.mu_pt[i], evt_tree.trk_pt[j])

	  if evt_tree.mu_pt[i]>=25:
	    h_eta_denom.Fill(evt_tree.mu_eta[i])
	    h_phi_denom.Fill(evt_tree.mu_phi[i])

	  if evt_tree.trk_pt[j]>=25.:
	    h_pt_numer.Fill(evt_tree.mu_pt[i])
	    h_2D_pt_eta_numer.Fill(evt_tree.mu_eta[i], evt_tree.mu_pt[i])

	    if evt_tree.mu_pt[i]>=25.:
	      h_eta_numer.Fill(evt_tree.mu_eta[i])
	      h_phi_numer.Fill(evt_tree.mu_phi[i])

	
## ================ Plot/save histograms ======================

#-------------------------------------
#Efficiency plots
#-------------------------------------
c1 = TCanvas("c1")
eff = TEfficiency(h_phi_numer, h_phi_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs #phi^{GEN} (p_{T}^{GEN}, p_{T}^{L1} > 25 GeV) (1.24 < #eta^{GEN} < 2.4) ; #phi^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_phi_pt25.png')
raw_input("Enter")

c1 = TCanvas("c1")
eff = TEfficiency(h_pt_numer, h_pt_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs p_{T}^{GEN} (p_{T}^{L1} > 25 GeV) (1.24 < #eta^{GEN} < 2.4) ; p_{T}^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_pt25.png')
raw_input("Enter")


c1 = TCanvas("c1")
eff = TEfficiency(h_eta_numer, h_eta_denom)
eff.Draw()
eff.SetTitle('EMTF Trigger Efficiency vs #eta^{GEN} (p_{T}^{GEN}, p_{T}^{L1} > 25 GeV) ; #eta^{GEN} ; Trigger Effieicny')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c1.SaveAs('validation_november/eff_eta_pt25.png')
raw_input("Enter")


#-------------------------------------
#True and L1 pT correlation
#-------------------------------------
#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_2D_genpt_l1pt.Draw("colz")
#gStyle.SetOptStat(0)
#gPad.SetLogz()
#h_2D_genpt_l1pt.SetTitle('p_{T}^{L1} vs p_{T}^{GEN})')
#h_2D_genpt_l1pt.GetXaxis().SetTitle('p_{T}^{GEN} (GeV)') ; h_2D_genpt_l1pt.GetYaxis().SetTitle('p_{T}^{L1} (GeV)')
#h_2D_genpt_l1pt.Write()
#c1.SaveAs('validation_november/ptgen_ptl1.png')
##raw_input("Enter")
#c1.Close()


#-------------------------------------
#2D Efficiency (pT and eta)
#-------------------------------------
#c1 = TCanvas("c1")
#h_2D_pt_eta_numer.Divide(h_2D_pt_eta_denom)
#h_2D_pt_eta_numer.Draw("colz")
#h_2D_pt_eta_numer.GetZaxis().SetRangeUser(0.,1.0)
#h_2D_pt_eta_numer.SetTitle('Trigger efficiency 2D p_{T}^{GEN} vs #eta^{GEN} (p_{T}^{L1} > 20 GeV)')
#h_2D_pt_eta_numer.GetXaxis().SetTitle('#eta^{GEN}') ; h_2D_pt_eta_numer.GetYaxis().SetTitle('p_{T}^{GEN}')
#raw_input("Enter")
#c1.Close()


#-------------------------------------
#Nstub and mode correlation plots
#-------------------------------------
'''
c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_2D_nstubs_pt.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_2D_nstubs_pt.SetTitle('Number of stubs vs p_{T}^{GEN}')
h_2D_nstubs_pt.GetXaxis().SetTitle('p_{T}^{GEN}') ; h_2D_nstubs_pt.GetYaxis().SetTitle('N_{stubs}')
h_2D_nstubs_pt.Write()
c1.SaveAs('validation_november/stubs_pt.png')
raw_input("Enter")
c1.Close()

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_2D_nstubs_eta.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_2D_nstubs_eta.SetTitle('Number of stubs vs |#eta^{GEN}|')
h_2D_nstubs_eta.GetXaxis().SetTitle('#eta^{GEN}') ; h_2D_nstubs_eta.GetYaxis().SetTitle('N_{stubs}')
h_2D_nstubs_eta.Write()
c1.SaveAs('validation_november/stubs_eta.png')
raw_input("Enter")
c1.Close()

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_2D_mode_eta.Draw("colz")
gStyle.SetOptStat(0)
gPad.SetLogz()
h_2D_mode_eta.SetTitle('Mode occupancy vs |#eta^{GEN}|')
h_2D_mode_eta.GetXaxis().SetTitle('#eta^{GEN}') ; h_2D_mode_eta.GetYaxis().SetTitle('Track mode')
h_2D_mode_eta.Write()
c1.SaveAs('validation_november/mode_eta.png')
raw_input("Enter")
c1.Close()
'''

