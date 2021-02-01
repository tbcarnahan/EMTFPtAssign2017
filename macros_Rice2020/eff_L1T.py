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
plot_EffVsPt=True ; plot_EffVsEta=False
eta_slices=False ; single_pt=False

if single_pt==True:
  pt_cut = [22]
  pt_str = ["22"]

else:
  pt_cut = [3, 5, 7, 10, 12, 15, 20, 22, 24, 27]
  pt_str = ["3", "5", "7", "10", "12", "15", "20", "22", "24", "27"]

if eta_slices==True:
  eta_min = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
  eta_max = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
  eta_str_min = ["1pt2", "1pt4", "1pt6", "1pt8", "2pt0", "2pt2"]
  eta_str_max = ["1pt4", "1pt6", "1pt8", "2pt0", "2pt2", "2pt4"]

else:  #Whole endcap region.
  eta_min = [1.2]
  eta_max = [2.4]
  eta_str_min = ["1pt2"]
  eta_str_max = ["2pt4"]


## ============== Define TTrees ================
evt_tree = TChain('f_MODE_15_logPtTarg_logPtWgt_noBitCompr_noRPC_noGEM_Run2Tree/TestTree')
evt_tree2 = TChain('f_MODE_15_logPtTarg_logPtWgt_noBitCompr_noRPC_noGEM_Run3Tree_newVarsOn/TestTree')


## ================ Read input files ======================
dir1 = 'root://cmseos.fnal.gov//store/user/mdecaro/condor_output_BDT/'
file_name = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM_Run2Tree.root"
file_name2 = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM_Run3Tree.root"

print colored('Loading file: '+file_name, 'green') ; print colored('Loading file: '+file_name2, 'green')
evt_tree.Add(file_name) ; evt_tree2.Add(file_name2)

## ================ Event loop ======================

for l in range(len(pt_cut)):
  for k in range(len(eta_min)):

    c1 = TCanvas("c1")

    if plot_EffVsPt == True:

      #Run2 and Run3 BDT efficiency vs Pt
      evt_tree2.Draw("GEN_pt>>h_denom(50,1.,50.)", "abs(GEN_eta)>"+str(eta_min[k])+" && abs(GEN_eta)<"+str(eta_max[k]))
      h_denom=gROOT.FindObject("h_denom")
      c1.Update()
      evt_tree2.Draw("GEN_pt>>h_numer(50,1.,50.)", "abs(GEN_eta)>"+str(eta_min[k])+" && abs(GEN_eta)<"+str(eta_max[k])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
      h_numer=gROOT.FindObject("h_numer")
      c1.Update()

      evt_tree.Draw("GEN_pt>>h_denom2(50,1.,50.)", "abs(GEN_eta)>"+str(eta_min[k])+" && abs(GEN_eta)<"+str(eta_max[k]))
      h_denom2=gROOT.FindObject("h_denom2")
      c1.Update()
      evt_tree.Draw("GEN_pt>>h_numer2(50,1.,50.)", "abs(GEN_eta)>"+str(eta_min[k])+" && abs(GEN_eta)<"+str(eta_max[k])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
      h_numer2=gROOT.FindObject("h_numer2")
      c1.Update()

      eff = TEfficiency(h_numer, h_denom) ; eff2 = TEfficiency(h_numer2, h_denom2)
      line = TLine(0, 0.9, 50, 0.9)
      line2 = TLine(pt_cut[l], 0., pt_cut[l], 1.1)
      line.SetLineStyle(7) ; line2.SetLineStyle(7)

      eff.SetMarkerColor(kBlue) ; eff.SetLineColor(kBlue) ; eff.SetMarkerStyle(8)
      eff2.SetMarkerColor(kRed) ; eff2.SetLineColor(kRed) ; eff2.SetMarkerStyle(8)
      eff.Draw("AP") ; eff2.Draw("same")
      line.Draw("same") ; line2.Draw("same")

      la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.035) ; la1.SetTextAlign(10)
      la1.DrawLatex( 35., 0.2, "p_{T}^{L1} > "+str(pt_cut[l])+" GeV")
      la2 = TLatex() ; la2.SetTextFont(22) ; la2.SetTextColor(1) ; la2.SetTextSize(0.035) ; la2.SetTextAlign(10)
      la2.DrawLatex( 35., 0.1, str(eta_min[k])+" < |#eta^{GEN}| < "+str(eta_max[k]))

      leg = TLegend(0.6, 0.33, 0.9, 0.63) ; leg.AddEntry(eff, "Run-3 BDT scaled") ; leg.AddEntry(eff2, "Run-2 BDT scaled") ; leg.SetBorderSize(0) ; leg.Draw("same")
    
      gPad.Update()
      eff.SetTitle(" ; p_{T}^{GEN} (GeV) ; Trigger Efficiency") 
      graph = eff.GetPaintedGraph() ; graph.SetMinimum(0) ;  graph.SetMaximum(1.1)

      c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".png")
      c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".C")
      c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".pdf")
      #raw_input("Enter")
      c1.Close()


    if plot_EffVsEta == True:
     
      #Run2 and Run3 BDT efficiency vs Eta
      evt_tree2.Draw("GEN_eta>>h_denom(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l]))
      h_denom=gROOT.FindObject("h_denom")
      c1.Update()
      evt_tree2.Draw("GEN_eta>>h_numer(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
      h_numer=gROOT.FindObject("h_numer")
      c1.Update()

      evt_tree.Draw("GEN_pt>>h_denom2(50,1.,50.)", "GEN_pt>"+str(pt_cut[l]))
      h_denom2=gROOT.FindObject("h_denom2")
      c1.Update()
      evt_tree.Draw("GEN_pt>>h_numer2(50,1.,50.)", "GEN_pt>"+str(pt_cut[l])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
      h_numer2=gROOT.FindObject("h_numer2")
      c1.Update()

      eff = TEfficiency(h_numer, h_denom) ; eff2 = TEfficiency(h_numer2, h_denom2)

      c1 = TCanvas("c1")
      
      eff.SetMarkerColor(kBlue) ; eff.SetMarkerStyle(8)
      eff2.SetMarkerColor(kRed) ; eff2.SetLineColor(kRed) ; eff2.SetMarkerStyle(8)
      eff.Draw("AP") ; eff2.Draw("same")
    
      gPad.Update()

      eff.SetTitle("EMTF Trigger Efficiency vs #eta^{GEN} (p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV) ; #eta^{GEN} ; Trigger Efficiency") 
    
      c1.SaveAs("plots/bdt_eff/BDTeff_eta_pt"+str(pt_str[l])+".png")
      c1.SaveAs("plots/bdt_eff/BDTeff_eta_pt"+str(pt_str[l])+".C")
      c1.SaveAs("plots/bdt_eff/BDTeff_eta_pt"+str(pt_str[l])+".pdf")
      c1.Close()
