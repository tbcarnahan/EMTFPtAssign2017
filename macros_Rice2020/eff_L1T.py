# -*- coding: utf-8 -*-
print '------> Setting Environment'

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT

## Run in quiet mode
sys.argv.append('-b')
gROOT.SetBatch(1)


## Configuration settings
efficiencies=True ; EffVsPt=False ; EffVsEta=True ; eta_slices=False ; single_pt=False
resolutions=False ; res2D=False ; res1D=False

if single_pt==True:
  pt_cut = [22] ; pt_str = ["22"]

else:
  pt_cut = [3, 5, 7, 10, 12, 15, 20, 22, 24, 27]
  pt_str = ["3", "5", "7", "10", "12", "15", "20", "22", "24", "27"]

if eta_slices==True:
  eta_min = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
  eta_max = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
  eta_str_min = ["1pt2", "1pt4", "1pt6", "1pt8", "2pt0", "2pt2"]
  eta_str_max = ["1pt4", "1pt6", "1pt8", "2pt0", "2pt2", "2pt4"]

else:  #Whole endcap region.
  eta_min = [1.2] ; eta_max = [2.4]
  eta_str_min = ["1pt2"] ; eta_str_max = ["2pt4"]


## ============== Define TTrees ================
evt_tree = TChain('f_MODE_15_logPtTarg_logPtWgt_noBitCompr_noRPC_noGEM_Run2Tree/TestTree')
evt_tree2 = TChain('f_MODE_15_logPtTarg_logPtWgt_noBitCompr_noRPC_noGEM_Run3Tree_newVarsOn/TestTree')


## ================ Read input files ======================
print '------> Importing Root Files..'
dir1 = 'root://cmseos.fnal.gov//store/user/mdecaro/condor_output_BDT/'
file_name = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM_Run2Tree.root"
file_name2 = dir1+"PtRegression2018_MODE_15_noBitCompr_noRPC_noGEM_Run3Tree.root"

print colored('Loading file: '+file_name, 'green') ; print colored('Loading file: '+file_name2, 'green')
evt_tree.Add(file_name) ; evt_tree2.Add(file_name2)

## ================ Plotting script ======================

if efficiencies==True:

  for l in range(len(pt_cut)):
    for k in range(len(eta_min)):

      c1 = TCanvas("c1")

      if EffVsPt == True:

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

	leg = TLegend(0.6, 0.33, 0.9, 0.63) ; leg.AddEntry(eff2, "Run-2 BDT scaled") ; leg.AddEntry(eff, "Run-3 BDT scaled") ; leg.SetBorderSize(0) ; leg.Draw("same")
      
	gPad.Update()
	eff.SetTitle(" ; p_{T}^{GEN} (GeV) ; Trigger Efficiency") 
	graph = eff.GetPaintedGraph() ; graph.SetMinimum(0) ;  graph.SetMaximum(1.1)

	c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".png")
	c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".C")
	c1.SaveAs("plots/bdt_eff/eta_slices/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k])+".pdf")
	c1.Close()


      if EffVsEta == True:
      
	#Run2 and Run3 BDT efficiency vs Eta
	evt_tree2.Draw("GEN_eta>>h_denom(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l]))
	h_denom=gROOT.FindObject("h_denom")
	c1.Update()
	evt_tree2.Draw("GEN_eta>>h_numer(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
	h_numer=gROOT.FindObject("h_numer")
	c1.Update()

	evt_tree.Draw("GEN_eta>>h_denom2(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l]))
	h_denom2=gROOT.FindObject("h_denom2")
	c1.Update()
	evt_tree.Draw("GEN_eta>>h_numer2(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l])+" && ((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))>"+str(pt_cut[l]))
	h_numer2=gROOT.FindObject("h_numer2")
	c1.Update()

	eff = TEfficiency(h_numer, h_denom) ; eff2 = TEfficiency(h_numer2, h_denom2)	
	eff.SetMarkerColor(kBlue) ; eff.SetLineColor(kBlue) ; eff.SetMarkerStyle(8)
	eff2.SetMarkerColor(kRed) ; eff2.SetLineColor(kRed) ; eff2.SetMarkerStyle(8)
	eff.Draw("AP") ; eff2.Draw("same")

	la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.033) ; la1.SetTextAlign(10)
	la1.DrawLatex( -0.6, 0.923, "p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")

	leg = TLegend(0.40, 0.26, 0.67, 0.53) ; leg.AddEntry(eff2, "Run-2 BDT scaled") ; leg.AddEntry(eff, "Run-3 BDT scaled") ; leg.SetBorderSize(0) ; leg.Draw("same")
      
	gPad.Update()
	eff.SetTitle(" ; #eta^{GEN} ; Trigger Efficiency")
	graph = eff.GetPaintedGraph() ; graph.SetMinimum(0.915) ;  graph.SetMaximum(1.003)
	c1.SaveAs("plots/bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l])+".png")
	c1.SaveAs("plots/bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l])+".C")
	c1.SaveAs("plots/bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l])+".pdf")
	#raw_input("Enter")
	c1.Close()


if resolutions==True:

  if res1D==True:

    pt_low = [] ; pt_hi = [] ; res = [] ; res2 = []
    for i in range(1,49):
      pt_low.append(float(i)) ; pt_hi.append(float(i+1))

    for l in range(len(pt_low)):
      c1 = TCanvas("c1")
      evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-3.,3.)", "GEN_pt>"+str(pt_low[l])+" && GEN_pt<"+str(pt_hi[l]))
      htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
      res.append(htemp.GetRMS())
      c1.Close()

      c1 = TCanvas("c1")
      evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-3.,3.)", "GEN_pt>"+str(pt_low[l])+" && GEN_pt<"+str(pt_hi[l]))
      htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
      res2.append(htemp2.GetRMS())
      c1.Close()

    c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
    g1 = TGraph(len(pt_low), np.array(pt_low), np.array(res))
    g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
    g2 = TGraph(len(pt_low), np.array(pt_low), np.array(res2))
    g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)

    mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Draw('ap')
    mg.GetXaxis().SetTitle('(p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN}')
    mg.GetYaxis().SetTitle('#sigma')

    c1.Update()
    c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.png")
    c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.C")
    c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.pdf")
    c1.Close()


  if res2D==True:

    c1 = TCanvas("c1")
    line = TLine(0, 0, 5.7, 5.7) ; line.SetLineColor(kRed) ; line.SetLineStyle(7)
    
    #Run-2 BDT
    evt_tree.Draw("log2((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))):log2(GEN_pt)>>htemp(100,0,5.7,100,0,6.5)", "", "COLZ")
    htemp = gPad.GetPrimitive("htemp")
    htemp.SetTitle("Mode 15 CSC-only Run-2 BDT, uncompressed (test) vs log2(p_{T}^{GEN})")
    htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("Run-2 Scaled trigger log2(p_{T}^{BDT})")
    line.Draw("same")
    gPad.SetLogz() ; gPad.Update() ; gStyle.SetOptStat(0)
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT_scaled.C")
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT_scaled.png")
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT_scaled.pdf")

    #Run-3 BDT
    evt_tree2.Draw("log2((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))):log2(GEN_pt)>>htemp2(100,0,5.7,100,0,6.5)", "", "COLZ")
    htemp2 = gPad.GetPrimitive("htemp2")
    htemp2.SetTitle("Mode 15 CSC-only Run-3 BDT, uncompressed (test) vs log2(p_{T}^{GEN})")
    htemp2.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp2.GetYaxis().SetTitle("Run-3 Scaled trigger log2(p_{T}^{BDT})")
    line.Draw("same")
    gPad.SetLogz() ; gPad.Update() ; gStyle.SetOptStat(0)
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT_scaled.C")
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT_scaled.png")
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT_scaled.pdf")