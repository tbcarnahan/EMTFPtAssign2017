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
efficiencies=False ; EffVsPt=False ; EffVsEta=False ; eta_slices=False ; single_pt=False
resolutions=True ; res2D=False ; res1D=True ; res1D_diffOverGen=False ; res1D_invDiffOverInvGen=False ; res1DvsPt=False ; res1DvsEta=True

if single_pt==True:
  pt_cut = [22] ; pt_str = ["22"]

else:
  pt_cut = [3., 5., 7., 10., 12., 15., 20., 22., 24., 27.]
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


## ================ Helper functions ======================
def truncate(number, digits):
  stepper = 10.0 ** digits
  return float(math.trunc(stepper * number) / stepper)


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

    if res1D_diffOverGen==True:

      lat_scale = [270e3, 220e3, 171e3, 140e3, 120e3, 100e3, 79e3, 74e3, 65e3, 57e3]
      lat_scale_diff = [4e4, 4e4, 3e4, 2.5e4, 2e4, 2e4, 1.5e4, 1.2e4, 1e4, 1e4]

      for l in range(len(pt_cut)):
    
	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-2.,2.)", "GEN_pt>"+str(pt_cut[l]))
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-2.,2.)", "GEN_pt>"+str(pt_cut[l]))
	
	htemp=gROOT.FindObject("htemp") ; htemp2=gROOT.FindObject("htemp2")
	htemp.SetLineColor(kRed) ; htemp2.SetLineColor(kBlue)
	htemp.Draw() ; htemp2.Draw("same")

	la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(kRed) ; la1.SetTextSize(0.033) ; la1.SetTextAlign(10)
	la1.DrawLatex( 0.60, lat_scale[l], "Run-2 #mu = "+str(truncate(htemp.GetMean(),3))+", #sigma = "+str(truncate(htemp.GetRMS(),3)))
	la2 = TLatex() ; la2.SetTextFont(22) ; la2.SetTextColor(kBlue) ; la2.SetTextSize(0.033) ; la2.SetTextAlign(10)
	la2.DrawLatex( 0.60, lat_scale[l]-lat_scale_diff[l], "Run-3 #mu = "+str(truncate(htemp2.GetMean(),3))+", #sigma = "+str(truncate(htemp2.GetRMS(),3)))
	la3 = TLatex() ; la3.SetTextFont(22) ; la3.SetTextColor(kBlack) ; la3.SetTextSize(0.033) ; la3.SetTextAlign(10)
	la3.DrawLatex( 0.60, lat_scale[l]-2*lat_scale_diff[l], "Mode 15, p_{T}^{L1} > "+str(int(pt_cut[l]))+" GeV")

	leg = TLegend(0.61, 0.65, 0.80, 0.87) ; leg.AddEntry(htemp, "Run-2 BDT") ; leg.AddEntry(htemp2, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")
      
	htemp = gPad.GetPrimitive("htemp")
	htemp.SetTitle("")
	htemp.GetXaxis().SetTitle("(p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN}")
	gStyle.SetOptStat(0) ; gPad.Update()
	c1.SaveAs("plots/resolutions/ptres1D_DiffOverGen_pt"+str(pt_str[l])+".png")
	c1.SaveAs("plots/resolutions/ptres1D_DiffOverGen_pt"+str(pt_str[l])+".C")
	c1.SaveAs("plots/resolutions/ptres1D_DiffOverGen_pt"+str(pt_str[l])+".pdf")
	#raw_input("Enter")
	c1.Close()

    if res1D_invDiffOverInvGen==True:

      for l in range(len(pt_cut)):

	c1 = TCanvas("c1")
	evt_tree.Draw("(1./(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp(64,-20.,20.)", "GEN_pt>"+str(pt_cut[l]))
	evt_tree2.Draw("(1./(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp2(64,-20.,20.)", "GEN_pt>"+str(pt_cut[l]))
	
	htemp=gROOT.FindObject("htemp") ; htemp2=gROOT.FindObject("htemp2")
	htemp.SetLineColor(kRed) ; htemp2.SetLineColor(kBlue)
	htemp.Draw() ; htemp2.Draw("same")

	lat_scale = [275e3, 245e3, 210e3, 180e3, 160e3, 145e3, 105e3, 96e3, 85e3, 70e3]
	lat_scale_diff = [4.2e4, 4e4, 3.3e4, 2.5e4, 2.5e4, 2e4, 1.7e4, 1.6e4, 1.4e4, 1.2e4]
	la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(kRed) ; la1.SetTextSize(0.031) ; la1.SetTextAlign(10)
	la1.DrawLatex( 6.5, lat_scale[l], "Run-2 #mu = "+str(truncate(htemp.GetMean(),3))+", #sigma = "+str(truncate(htemp.GetRMS(),3)))
	la2 = TLatex() ; la2.SetTextFont(22) ; la2.SetTextColor(kBlue) ; la2.SetTextSize(0.031) ; la2.SetTextAlign(10)
	la2.DrawLatex( 6.5, lat_scale[l]-lat_scale_diff[l], "Run-3 #mu = "+str(truncate(htemp2.GetMean(),3))+", #sigma = "+str(truncate(htemp2.GetRMS(),3)))
	la3 = TLatex() ; la3.SetTextFont(22) ; la3.SetTextColor(kBlack) ; la3.SetTextSize(0.031) ; la3.SetTextAlign(10)
	la3.DrawLatex( 6.5, lat_scale[l]-2*lat_scale_diff[l], "Mode 15, p_{T}^{L1} > "+str(int(pt_cut[l]))+" GeV")
	

	leg = TLegend(0.62, 0.65, 0.81, 0.87) ; leg.AddEntry(htemp, "Run-2 BDT") ; leg.AddEntry(htemp2, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")
	
	htemp = gPad.GetPrimitive("htemp")
	htemp.SetTitle("")
	htemp.GetXaxis().SetTitle("(p_{T}^{GEN} - p_{T}^{L1})^{-1} / (p_{T}^{GEN})^{-1}")
	gStyle.SetOptStat(0) ; gPad.Update()
	c1.SaveAs("plots/resolutions/ptres1D_invDiffOverInvGen_pt"+str(pt_str[l])+".png")
	c1.SaveAs("plots/resolutions/ptres1D_invDiffOverInvGen_pt"+str(pt_str[l])+".C")
	c1.SaveAs("plots/resolutions/ptres1D_invDiffOverInvGen_pt"+str(pt_str[l])+".pdf")
	#raw_input("Enter")
	c1.Close()

    if res1DvsPt==True:

      ## ============== Inverse Pt Diff Over Inverse GEN ================

      res = [] ; res2 = [] ; resErr = [] ; res2Err = [] ; zeros=[]

      for l in range(len(pt_cut)):
	c1 = TCanvas("c1")
	evt_tree2.Draw("(1./(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp(64,-20.,20.)", "GEN_pt>"+str(pt_cut[l]))
	htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
	res.append(htemp.GetRMS()) ; resErr.append(htemp.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(1./(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp2(64,-20.,20.)", "GEN_pt>"+str(pt_cut[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res2.append(htemp2.GetRMS()) ; res2Err.append(htemp2.GetRMSError())
	c1.Close()

	zeros.append(0.)

      c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
      g1 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res), np.array(zeros) , np.array(resErr))
      g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
      g2 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res2), np.array(zeros) , np.array(res2Err))
      g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)

      mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Draw('ap')
      mg.GetXaxis().SetTitle('p_{T}^{GEN}')
      mg.GetYaxis().SetTitle('#sigma ((p_{T}^{GEN} - p_{T}^{L1})^{-1} / (p_{T}^{GEN})^{-1})')

      leg = TLegend(0.15, 0.65, 0.34, 0.87) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g1, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      c1.SaveAs("plots/resolutions/res_vs_pt_invDiffOverInvGen.png")
      c1.SaveAs("plots/resolutions/res_vs_pt_invDiffOverInvGen.C")
      c1.SaveAs("plots/resolutions/res_vs_pt_invDiffOverInvGen.pdf")
      #raw_input("Enter")
      c1.Close()

      ## ============== Pt Diff Over GEN ================

      res = [] ; res2 = [] ; resErr = [] ; res2Err = [] ; zeros=[]

      for l in range(len(pt_cut)):
	c1 = TCanvas("c1")
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l]))
	htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
	res.append(htemp.GetRMS()) ; resErr.append(htemp.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-3.,3.)", "GEN_pt>"+str(pt_cut[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res2.append(htemp2.GetRMS()) ; res2Err.append(htemp2.GetRMSError())
	c1.Close()

	zeros.append(0.)

      c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
      g1 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res), np.array(zeros) , np.array(resErr))
      g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
      g2 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res2), np.array(zeros) , np.array(res2Err))
      g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)

      mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Draw('ap')
      mg.GetXaxis().SetTitle('p_{T}^{GEN}')
      mg.GetYaxis().SetTitle('#sigma ((p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN})')

      leg = TLegend(0.67, 0.65, 0.86, 0.87) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g1, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.png")
      c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.C")
      c1.SaveAs("plots/resolutions/res_vs_pt_diffOverGen.pdf")
      #raw_input("Enter")
      c1.Close()

  if res1DvsEta==True:

    eta_min1 = [-2.4, -2.2, -2.0, -1.8, -1.6, -1.4] ; eta_min2 = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
    eta_max1 = [-2.2, -2.0, -1.8, -1.6, -1.4, -1.2] ; eta_max2 = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
    
    for k in range(len(pt_cut)):

      res = [] ; res2 = [] ; resErr = [] ; res2Err = [] ; zeros=[]
      
      for l in range(len(eta_min1)):

	c1 = TCanvas("c1")
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-3.,3.)", "GEN_pt>"+str(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
	res.append(htemp.GetRMS()) ; resErr.append(htemp.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-3.,3.)", "GEN_pt>"+str(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res.append(htemp2.GetRMS()) ; resErr.append(htemp2.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp3(64,-3.,3.)", "GEN_pt>"+str(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp3 = gPad.GetPrimitive("htemp3") ; htemp3.Draw()
	res2.append(htemp3.GetRMS()) ; res2Err.append(htemp3.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp4(64,-3.,3.)", "GEN_pt>"+str(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
	htemp4 = gPad.GetPrimitive("htemp4") ; htemp4.Draw()
	res2.append(htemp4.GetRMS()) ; res2Err.append(htemp4.GetRMSError())
	c1.Close()

	zeros.append(0.) ; zeros.append(0.)

      eta = [-2.4, -2.2, -2.0, -1.8, -1.6, -1.4, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
      c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
      g1 = TGraphErrors(len(eta), np.array(eta), np.array(res), np.array(zeros) , np.array(resErr))
      g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
      g2 = TGraphErrors(len(eta), np.array(eta), np.array(res2), np.array(zeros) , np.array(res2Err))
      g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)

      mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Draw('ap')
      mg.GetXaxis().SetTitle('#eta^{GEN}')
      mg.GetYaxis().SetTitle('#sigma ((p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN})')

      lat_scale = [.33, .34, .34, .34, .34, .325, .295, .28, .27, .253]
      la = TLatex() ; la.SetTextFont(22) ; la.SetTextColor(kBlack) ; la.SetTextSize(0.031) ; la.SetTextAlign(10)
      la.DrawLatex( -0.62, lat_scale[k], "Mode 15, p_{T}^{L1} > "+str(int(pt_cut[k]))+" GeV")


      leg = TLegend(0.40, 0.61, 0.62, 0.85) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g1, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      c1.SaveAs("plots/resolutions/res_vs_eta_diffOverGen_pt"+str(pt_str[k])+".png")
      c1.SaveAs("plots/resolutions/res_vs_eta_diffOverGen_pt"+str(pt_str[k])+".C")
      c1.SaveAs("plots/resolutions/res_vs_eta_diffOverGen_pt"+str(pt_str[k])+".pdf")
      #raw_input("Enter")
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
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT.C")
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT.png")
    c1.SaveAs("plots/resolutions/ptres2D_Run2BDT.pdf")
    #raw_input("Enter")

    #Run-3 BDT
    evt_tree2.Draw("log2((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))):log2(GEN_pt)>>htemp2(100,0,5.7,100,0,6.5)", "", "COLZ")
    htemp2 = gPad.GetPrimitive("htemp2")
    htemp2.SetTitle("Mode 15 CSC-only Run-3 BDT, uncompressed (test) vs log2(p_{T}^{GEN})")
    htemp2.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp2.GetYaxis().SetTitle("Run-3 Scaled trigger log2(p_{T}^{BDT})")
    line.Draw("same")
    gPad.SetLogz() ; gPad.Update() ; gStyle.SetOptStat(0)
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT.C")
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT.png")
    c1.SaveAs("plots/resolutions/ptres2D_Run3BDT.pdf")
    #raw_input("Enter")