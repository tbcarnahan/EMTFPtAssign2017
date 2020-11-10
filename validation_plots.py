# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

## ================ Settings=======================
printouts_Run2=False
printouts_Run3=False


## ================ Read input files ==============
print '------> Importing Root File'
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
#file_name = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM.root" #BDT output file
file_name = dir1+"EMTF_MC_NTuple_Run2stubs.root" #Input file w/ Run2 stubs
file_name2 = dir1+"EMTF_MC_NTuple_20201106.root" #Input file w/ Run3 stubs
print colored('Loading file: '+file_name, 'green')
print colored('Loading file: '+file_name2, 'green')


## ============= Read in the TTrees ===============
#evt_tree = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')
evt_tree = TChain('FlatNtupleMC/tree') #Input NTuple tree
evt_tree.Add(file_name)
evt_tree2 = TChain('FlatNtupleMC/tree') #Input NTuple tree
evt_tree2.Add(file_name2)


## ========= Printouts for debugging ==============

if printouts_Run2==True:
  for iEvt in range(10000):
    evt_tree.GetEntry(iEvt)
    for i in range(len(evt_tree.mu_pt)):
      print "Gen muon",i, " pt, eta, phi: ", evt_tree.mu_pt[i], evt_tree.mu_eta[i], evt_tree.mu_phi[i]
    print '--------'
    for i in range(len(evt_tree.trk_pt)):
      print "L1 muon",i, " pt, eta, phi, nNeighbor: ", evt_tree.trk_pt[i], evt_tree.trk_eta[i], evt_tree.trk_phi[i], evt_tree.trk_nNeighbor[i]
    print '------Next event------'
    
## ============== Plotting macro ==================

#Trigger efficiencies (How often do you trigger on a muon with pT > X)
c1 = TCanvas("c1")

#Using Run-2 stubs
evt_tree.Draw("mu_pt>>h_denom(64,0.,50.)")
h_denom=gROOT.FindObject("h_denom")
c1.Update()
evt_tree.Draw("mu_pt>>h_numer(64,0.,50.)", "trk_pt>20. && (mu_eta[0]*trk_eta>0 || mu_eta[1]*trk_eta>0) && trk_nNeighbor==0")
h_numer=gROOT.FindObject("h_numer")
c1.Update()

##Using Run-3 stubs
evt_tree2.Draw("mu_pt>>h_denom2(64,0.,50.)")
h_denom2=gROOT.FindObject("h_denom2")
c1.Update()
evt_tree2.Draw("mu_pt>>h_numer2(64,0.,50.)", "trk_pt>20. && (mu_eta[0]*trk_eta>0 || mu_eta[1]*trk_eta>0) && trk_nNeighbor==0")
h_numer2=gROOT.FindObject("h_numer2")
c1.Update()

#Divide numer/denom histograms and plot efficiencies on the same canvas.
h_numer.Divide(h_denom) ; h_numer2.Divide(h_denom2)
h_numer.SetTitle("Trigger efficiency (p_{T}^{L1} > 20 GeV)")
h_numer.GetXaxis().SetTitle("p_{T} (GeV)")
gStyle.SetOptStat(0)
h_numer.Draw() ; h_numer2.SetLineColor(2) ; h_numer2.Draw("same")
c1.SaveAs("validation_november/efficiency_pt20.png")
raw_input("Enter")
c1.Close()


##Using TEfficiency instead:
#eff = TEfficiency(h_numer, h_denom)
#eff.Draw()
##eff.SetTitle('ME1/1 Trigger Efficiency vs p_{T}^{GEN} (1.6 < |#eta^{GEN}| < 2.1)')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
##c57.SaveAs("validation_november/eff_pt_csc.png")
#raw_input("Enter")


'''
#Pt resolutions (Make sure you're using BDT output file.)
c1 = TCanvas("c1")
evt_tree.Draw("BDTG_AWB_Sq:log(GEN_pt)", "", "COLZ")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{BDT}) vs log2(p_{T}^{GEN})")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("log2(p_{T}^{BDT})")
htemp.SetAxisRange(0.,11., "Y")
gPad.Update()
c1.SaveAs("validation_november/ptres2D_log2gen_bdt.png")

#Plot the difference of log2(gen_pt) - BDT pt
c1 = TCanvas("c1")
evt_tree.Draw("log(GEN_pt) - BDTG_AWB_Sq", "")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{GEN}) - log2(p_{T}^{BDT})")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}))")
gPad.Update()
c1.SaveAs("validation_november/ptres1D_log2genpt_minus_bdtpt.png")


#With pt cuts
#2D pt resolution (BDT pt vs log2(gen_pt))
c1 = TCanvas("c1")
evt_tree.Draw("BDTG_AWB_Sq:log(GEN_pt)", "GEN_pt<10", "COLZ")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{BDT}) vs log2(p_{T}^{GEN}) (p_{T}^{GEN} < 10)")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("log2(p_{T}^{BDT})")
htemp.SetAxisRange(0.,11., "Y")
gPad.Update()
c1.SaveAs("validation_november/ptres2D_log2gen_bdt_cutpt10.png")

#Plot the difference of log2(gen_pt) - BDT pt
c1 = TCanvas("c1")
evt_tree.Draw("log(GEN_pt) - BDTG_AWB_Sq", "GEN_pt<10")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}) (p_{T}^{GEN} < 10)")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}))")
gPad.Update()
c1.SaveAs("validation_november/ptres1D_log2genpt_minus_bdtpt_cutpt10.png")
'''


#An example of filling a branch to TH1D object.
'''
c1 = TCanvas("c1")
evt_tree.Draw("hit_phi>>h1(64,-180.,180.)", "hit_station==1 && hit_isCSC==1 && hit_endcap>0" && hit_neighbor==0")
h1=gROOT.FindObject("h1")
c1.Update()
'''