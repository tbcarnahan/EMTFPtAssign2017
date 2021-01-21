# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

## run quiet mode
sys.argv.append( '-b' )
gROOT.SetBatch(1)

## ================ Read input files ==============
print '------> Importing Root File'
#dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
dir1 = 'root://cmsxrootd.fnal.gov//store/user/mdecaro/condor_output_BDT/'
file_name = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM_Run3Tree.root"

print colored('Loading file: '+file_name, 'green')


## ============= Read in the TTrees ===============
evt_tree = TChain('f_MODE_15_logPtTarg_logPtWgt_noBitCompr_noRPC_noGEM_Run3Tree_newVarsOn/TestTree') ; evt_tree.Add(file_name)

## ============== Plotting macro ==================


#BDT efficiency
c1 = TCanvas("c1")
evt_tree.Draw("GEN_pt>>h_denom(64,1.,50.)","abs(GEN_eta) > 1.2 && abs(GEN_eta) < 2.4")
h_denom=gROOT.FindObject("h_denom")
c1.Update()
evt_tree.Draw("GEN_pt>>h_numer(64,1.,50.)", "2**(BDTG_AWB_Sq)>24 && abs(GEN_eta) > 1.2 && abs(GEN_eta) < 2.4")
h_numer=gROOT.FindObject("h_numer")
c1.Update()
h_numer.Divide(h_denom)
h_numer.SetTitle("BDT efficiency (p_{T}^{BDT} > 24 GeV)")
h_numer.GetXaxis().SetTitle("p_{T} (GeV)")
h_numer.Draw()
c1.SaveAs("BDTefficiency_pt24.png")



'''
#Pt resolutions (Make sure you're using BDT output file.)
c1 = TCanvas("c1")
evt_tree.Draw("BDTG_AWB_Sq:log2(GEN_pt)>>htemp(100,0,6,100,0,6)", "", "COLZ")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("Mode 15 CSC-only BDT, uncompressed log2(test) vs log2 p_{T}^{GEN}")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("Unscaled trigger log2 p_{T} (GeV)")
htemp.SetAxisRange(0.,100., "Y")
gPad.SetLogz()
gPad.Update()
gStyle.SetOptStat(0)
c1.SaveAs("plots/validation_january/ptres2D_log2gen_Run2BDT.png")
'''


'''
#Plot the difference of log2(gen_pt) - BDT pt
c1 = TCanvas("c1")
evt_tree.Draw("log(GEN_pt) - BDTG_AWB_Sq", "")
evt_tree2.Draw("log(GEN_pt) - BDTG_AWB_Sq", "", "SAME")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{GEN}) - log2(p_{T}^{BDT})")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}))")
gPad.Update()
c1.SaveAs("plots/validation_january/ptres1D_log2genpt_compare.png")
'''

'''
#With pt cuts
#2D pt resolution (BDT pt vs log2(gen_pt))
c1 = TCanvas("c1")
evt_tree.Draw("BDTG_AWB_Sq:log(GEN_pt)", "GEN_pt<10", "COLZ")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{BDT}) vs log2(p_{T}^{GEN}) (p_{T}^{GEN} < 10)")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("log2(p_{T}^{BDT})")
htemp.SetAxisRange(0.,11., "Y")
gPad.Update()
c1.SaveAs("plots/validation_december/ptres2D_log2gen_bdt_cutpt10.png")

#Plot the difference of log2(gen_pt) - BDT pt
c1 = TCanvas("c1")
evt_tree.Draw("log(GEN_pt) - BDTG_AWB_Sq", "GEN_pt<10")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("p_{T} resolution: log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}) (p_{T}^{GEN} < 10)")
htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN}) - log2(p_{T}^{BDT}))")
gPad.Update()
c1.SaveAs("plots/validation_december/ptres1D_log2genpt_minus_bdtpt_cutpt10.png")



#An example of filling a branch to TH1D object.
c1 = TCanvas("c1")
evt_tree.Draw("hit_phi>>h1(64,-180.,180.)", "hit_station==1 && hit_isCSC==1 && hit_endcap>0" && hit_neighbor==0")
h1=gROOT.FindObject("h1")
c1.Update()
'''
