#! /usr/bin/env python

import sys
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT
from optparse import OptionParser,OptionGroup

## Configuration settings
print '------> Setting Environment'
parser = OptionParser()
parser.add_option('--batchMode', dest='batchMode', action='store_true',default = True)
parser.add_option("--eta_slices", dest="eta_slices", action="store_true", default = False)
parser.add_option("--single_pt", dest="single_pt", action="store_true", default = False)
parser.add_option("--addDateTime", dest="addDateTime", action="store", default = True)

parser.add_option("--efficiencies", dest="efficiencies", action="store_true", default = False)
parser.add_option("--EffVsPt", dest="EffVsPt", action="store_true", default = True)
parser.add_option("--EffVsEta", dest="EffVsEta", action="store_true", default = False)

parser.add_option("--resolutions", dest="resolutions", action="store_true", default = True)
parser.add_option("--res1D", dest="res1D", action="store_true", default = True)
parser.add_option("--res1D_diffOverGen", dest="res1D_diffOverGen", action="store_true", default = False)
parser.add_option("--res1D_invDiffOverInvGen", dest="res1D_invDiffOverInvGen", action="store_true", default = False)
parser.add_option("--res1DvsPt", dest="res1DvsPt", action="store_true", default = True)
parser.add_option("--res1DvsEta", dest="res1DvsEta", action="store_true", default = True)
parser.add_option("--res2D", dest="res2D", action="store_true", default = False)

(options, args) = parser.parse_args()

plotDir = "plots/"

## Run in quiet mode
if options.batchMode:
  sys.argv.append('-b')
  gROOT.SetBatch(1)

if options.single_pt:
  pt_cut = [24]
  pt_str = ["24"]
else:
  pt_cut = [3., 5., 7., 10., 12., 15., 20., 22., 24., 27.]
  pt_str = ["3", "5", "7", "10", "12", "15", "20", "22", "24", "27"]

if options.eta_slices:
  eta_min = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
  eta_max = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]
  eta_str_min = ["1pt2", "1pt4", "1pt6", "1pt8", "2pt0", "2pt2"]
  eta_str_max = ["1pt4", "1pt6", "1pt8", "2pt0", "2pt2", "2pt4"]
else:
  #Whole endcap region.
  eta_min = [1.2]
  eta_max = [2.4]
  eta_str_min = ["1pt2"]
  eta_str_max = ["2pt4"]


## ============== Define TTrees ================
evt_tree1 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')
evt_tree2 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_RPC_noGEM/TestTree')
evt_tree3 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')
evt_tree4 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')
evt_tree5 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')
evt_tree6 = TChain('f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_noGEM/TestTree')


## ================ Read input files ======================
print '------> Importing Root Files..'
prefix = "root://cmseos.fnal.gov//store/user/mdecaro/"
dir1 = prefix + 'EMTF_BDT_Train_isRun2_20210321_223914/'
dir2 = prefix + 'EMTF_BDT_Train_isRun2_useRPC_20210312_094714/'
dir3 = prefix + 'EMTF_BDT_Train_isRun3_20210312_094720/'
dir4 = prefix + 'EMTF_BDT_Train_isRun3_useQSBit_20210321_223207/'
dir5 = prefix + 'EMTF_BDT_Train_isRun3_useQSBit_useESBit_20210321_223649/'
dir6 = prefix + 'EMTF_BDT_Train_isRun3_useQSBit_useESBit_useSlopes_20210312_094737/'
file_name1 = dir1+"PtRegressionRun3Prep_MODE_15_noBitCompr_noRPC_noGEM.root"
file_name2 = dir2+"PtRegressionRun3Prep_MODE_15_noBitCompr_RPC_noGEM.root"
file_name3 = dir3+"PtRegressionRun3Prep_MODE_15_noBitCompr_noRPC_noGEM.root"
file_name4 = dir4+"PtRegressionRun3Prep_MODE_15_noBitCompr_noRPC_noGEM.root"
file_name5 = dir5+"PtRegressionRun3Prep_MODE_15_noBitCompr_noRPC_noGEM.root"
file_name6 = dir6+"PtRegressionRun3Prep_MODE_15_noBitCompr_noRPC_noGEM.root"

print colored('Loading file: '+file_name1, 'green')
print colored('Loading file: '+file_name2, 'green')
print colored('Loading file: '+file_name3, 'green')
print colored('Loading file: '+file_name4, 'green')
print colored('Loading file: '+file_name5, 'green')
print colored('Loading file: '+file_name6, 'green')
evt_tree1.Add(file_name1)
evt_tree2.Add(file_name2)
evt_tree3.Add(file_name3)
evt_tree4.Add(file_name4)
evt_tree5.Add(file_name5)
evt_tree6.Add(file_name6)

## ================ Helper functions ======================
def truncate(number, digits):
  stepper = 10.0 ** digits
  return float(math.trunc(stepper * number) / stepper)

def gen_pt_cut(pt_min):
  return "GEN_pt >= {0}".format(pt_min)

def gen_eta_cut(eta_min, eta_max):
  return "abs(GEN_eta) >= {0} && abs(GEN_eta) <= {1}".format(eta_min, eta_max)

def bdt_pt_cut(pt_min):
  return "pow(2, BDTG_AWB_Sq) >= {}".format(pt_min)

def bdt_pt_scaled_cut(pt_min):
  return "pow(2, BDTG_AWB_Sq) >= {}".format(pt_min)
  #((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))

def makePlots(canvas, plotTitle):
  c1.SaveAs(plotDir + plotTitle + ".png")
  c1.SaveAs(plotDir + plotTitle + ".pdf")
  c1.SaveAs(plotDir + plotTitle + ".C")

''' (Work in progress)
evt_tree = [] ; files = []
if isRun2: evt_tree.append(evt_tree1)
if isRun2RPC: evt_tree.append(evt_tree2)
if isRun3: evt_tree.append(evt_tree3)
if isRun3QSBit: evt_tree.append(evt_tree4)
if isRun3QSBitESBit: evt_tree.append(evt_tree5)
if isRun3QSBitESBitSlopes: evt_tree.append(evt_tree6)
'''

## ================ Plotting script ======================
if options.efficiencies:

  for l in range(len(pt_cut)):
    for k in range(len(eta_min)):

      c1 = TCanvas("c1")

      if options.EffVsPt:

	#Run2 and Run3 BDT efficiency vs Pt

	evt_tree1.Draw("GEN_pt>>h_denom1(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom1=gROOT.FindObject("h_denom1")
	c1.Update()
	evt_tree1.Draw("GEN_pt>>h_numer1(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+ "&&" + bdt_pt_cut(pt_cut[l]))
	h_numer1=gROOT.FindObject("h_numer1")
	c1.Update()

	evt_tree2.Draw("GEN_pt>>h_denom2(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom2=gROOT.FindObject("h_denom2")
	c1.Update()
	evt_tree2.Draw("GEN_pt>>h_numer2(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+" && " + bdt_pt_cut(pt_cut[l]))
	h_numer2=gROOT.FindObject("h_numer2")
	c1.Update()

	evt_tree3.Draw("GEN_pt>>h_denom3(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom3=gROOT.FindObject("h_denom3")
	c1.Update()
	evt_tree3.Draw("GEN_pt>>h_numer3(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+" && " + bdt_pt_cut(pt_cut[l]))
	h_numer3=gROOT.FindObject("h_numer3")
	c1.Update()

	evt_tree4.Draw("GEN_pt>>h_denom4(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom4=gROOT.FindObject("h_denom4")
	c1.Update()
	evt_tree4.Draw("GEN_pt>>h_numer4(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+" && " + bdt_pt_cut(pt_cut[l]))
	h_numer4=gROOT.FindObject("h_numer4")
	c1.Update()

	evt_tree5.Draw("GEN_pt>>h_denom5(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom5=gROOT.FindObject("h_denom5")
	c1.Update()
	evt_tree5.Draw("GEN_pt>>h_numer5(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+" && " + bdt_pt_cut(pt_cut[l]))
	h_numer5=gROOT.FindObject("h_numer5")
	c1.Update()

	evt_tree6.Draw("GEN_pt>>h_denom6(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k]))
	h_denom6=gROOT.FindObject("h_denom6")
	c1.Update()
	evt_tree6.Draw("GEN_pt>>h_numer6(50,1.,50.)", gen_eta_cut(eta_min[k], eta_max[k])+" && " + bdt_pt_cut(pt_cut[l]))
	h_numer6=gROOT.FindObject("h_numer6")
	c1.Update()

	eff1 = TEfficiency(h_numer1, h_denom1) ; eff2 = TEfficiency(h_numer2, h_denom2) ; eff3 = TEfficiency(h_numer3, h_denom3)
	eff4 = TEfficiency(h_numer4, h_denom4) ; eff5 = TEfficiency(h_numer5, h_denom5) ; eff6 = TEfficiency(h_numer6, h_denom6)
	line = TLine(0, 0.5, 50, 0.5)
	line2 = TLine(pt_cut[l], 0., pt_cut[l], 1.1)
	line.SetLineStyle(7) ; line2.SetLineStyle(7)

	eff1.SetMarkerColor(kBlue) ; eff1.SetLineColor(kBlue) ; eff1.SetMarkerStyle(8)
	eff2.SetMarkerColor(kRed) ; eff2.SetLineColor(kRed) ; eff2.SetMarkerStyle(8)
	eff3.SetMarkerColor(kGreen+2) ; eff3.SetLineColor(kGreen+2) ; eff3.SetMarkerStyle(8)
	eff4.SetMarkerColor(kBlack) ; eff4.SetLineColor(kBlack) ; eff4.SetMarkerStyle(8)
	eff5.SetMarkerColor(7) ; eff5.SetLineColor(7) ; eff5.SetMarkerStyle(8)
	eff6.SetMarkerColor(40) ; eff6.SetLineColor(40) ; eff6.SetMarkerStyle(8)

	eff1.Draw("AP") ; eff2.Draw("same") ; eff3.Draw("same")
	eff4.Draw("same") ; eff5.Draw("same") ; eff6.Draw("same")
	line.Draw("same") ; line2.Draw("same")

	la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.035) ; la1.SetTextAlign(10)
	la1.DrawLatex( 35., 0.2, "p_{T}^{L1} > "+str(pt_cut[l])+" GeV")
	la2 = TLatex() ; la2.SetTextFont(22) ; la2.SetTextColor(1) ; la2.SetTextSize(0.035) ; la2.SetTextAlign(10)
	la2.DrawLatex( 35., 0.1, str(eta_min[k])+" < |#eta^{GEN}| < "+str(eta_max[k]))

	leg = TLegend(0.6, 0.33, 0.9, 0.63)
	leg.AddEntry(eff1, "Run-2 BDT") ; leg.AddEntry(eff2, "Run-2 BDT RPC") ; leg.AddEntry(eff3, "Run-3 BDT")
	leg.AddEntry(eff4, "Run-3 BDT w/ QSBit") ; leg.AddEntry(eff5, "Run-3 BDT w/ QSBit ESBit") ; leg.AddEntry(eff6, "Run-3 BDT w/ QSBit ESBit Slopes")
	leg.SetBorderSize(0) ; leg.Draw("same")

	gPad.Update()
	eff1.SetTitle(" ; p_{T}^{GEN} (GeV) ; Trigger Efficiency")
	gStyle.SetOptStat(0)
	graph = eff1.GetPaintedGraph() ; graph.SetMinimum(0) ;  graph.SetMaximum(1.1)

        makePlots(c1, "bdt_eff/eta_slices_03222021/BDTeff_pt"+str(pt_str[l])+"_eta"+str(eta_str_min[k])+"to"+str(eta_str_max[k]))


    if options.EffVsEta:

      #Run2 and Run3 BDT efficiency vs Eta
      evt_tree1.Draw("GEN_eta>>h_denom1(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom1=gROOT.FindObject("h_denom1")
      c1.Update()
      evt_tree1.Draw("GEN_eta>>h_numer1(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer1=gROOT.FindObject("h_numer1")
      c1.Update()

      evt_tree2.Draw("GEN_eta>>h_denom2(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom2=gROOT.FindObject("h_denom2")
      c1.Update()
      evt_tree2.Draw("GEN_eta>>h_numer2(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer2=gROOT.FindObject("h_numer2")
      c1.Update()

      evt_tree3.Draw("GEN_eta>>h_denom3(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom3=gROOT.FindObject("h_denom3")
      c1.Update()
      evt_tree3.Draw("GEN_eta>>h_numer3(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer3=gROOT.FindObject("h_numer3")
      c1.Update()

      evt_tree4.Draw("GEN_eta>>h_denom4(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom4=gROOT.FindObject("h_denom4")
      c1.Update()
      evt_tree4.Draw("GEN_eta>>h_numer4(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer4=gROOT.FindObject("h_numer4")
      c1.Update()

      evt_tree5.Draw("GEN_eta>>h_denom5(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom5=gROOT.FindObject("h_denom5")
      c1.Update()
      evt_tree5.Draw("GEN_eta>>h_numer5(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer5=gROOT.FindObject("h_numer5")
      c1.Update()

      evt_tree6.Draw("GEN_eta>>h_denom6(64,-3.,3.)", gen_pt_cut(pt_cut[l]))
      h_denom6=gROOT.FindObject("h_denom6")
      c1.Update()
      evt_tree6.Draw("GEN_eta>>h_numer6(64,-3.,3.)", gen_pt_cut(pt_cut[l])+" && " + bdt_pt_cut(pt_cut[l]))
      h_numer6=gROOT.FindObject("h_numer6")
      c1.Update()

      eff1 = TEfficiency(h_numer1, h_denom1) ; eff2 = TEfficiency(h_numer2, h_denom2) ; eff3 = TEfficiency(h_numer3, h_denom3)
      eff4 = TEfficiency(h_numer4, h_denom4) ; eff5 = TEfficiency(h_numer5, h_denom5) ; eff6 = TEfficiency(h_numer6, h_denom6)

      eff1.SetMarkerColor(kBlue) ; eff1.SetLineColor(kBlue) ; eff1.SetMarkerStyle(8)
      eff2.SetMarkerColor(kRed) ; eff2.SetLineColor(kRed) ; eff2.SetMarkerStyle(8)
      eff3.SetMarkerColor(kGreen+2) ; eff3.SetLineColor(kGreen+2) ; eff3.SetMarkerStyle(8)
      eff4.SetMarkerColor(kBlack) ; eff4.SetLineColor(kBlack) ; eff4.SetMarkerStyle(8)
      eff5.SetMarkerColor(7) ; eff5.SetLineColor(7) ; eff5.SetMarkerStyle(8)
      eff6.SetMarkerColor(40) ; eff6.SetLineColor(40) ; eff6.SetMarkerStyle(8)

      eff1.Draw("AP") ; eff2.Draw("same") ; eff3.Draw("same")
      eff4.Draw("same") ; eff5.Draw("same") ; eff6.Draw("same")

      la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.033) ; la1.SetTextAlign(10)
      #Note that the position of the label in the following line is hard-coded onto the axis (easier way to do this?)
      la1.DrawLatex( -0.6, 0.65, "p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")

      leg = TLegend(0.40, 0.26, 0.67, 0.53) ;
      leg.AddEntry(eff1, "Run-2 BDT") ; leg.AddEntry(eff2, "Run-2 BDT RPC") ; leg.AddEntry(eff3, "Run-3 BDT")
      leg.AddEntry(eff4, "Run-3 BDT w/ QSBit") ; leg.AddEntry(eff5, "Run-3 BDT w/ QSBit ESBit") ; leg.AddEntry(eff6, "Run-3 BDT w/ QSBit ESBit Slopes")
      leg.SetBorderSize(0) ; leg.Draw("same")

      gPad.Update()
      eff1.SetTitle(" ; #eta^{GEN} ; Trigger Efficiency")
      gStyle.SetOptStat(0)
      graph = eff1.GetPaintedGraph() ; graph.SetMinimum(0) ;  graph.SetMaximum(1.003)

      makePlot(c1, "bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l]) )


if options.resolutions:

  if options.res1D:

    if options.res1D_diffOverGen:

      lat_scale = [270e3, 220e3, 171e3, 140e3, 120e3, 100e3, 79e3, 74e3, 65e3, 57e3]
      lat_scale_diff = [4e4, 4e4, 3e4, 2.5e4, 2e4, 2e4, 1.5e4, 1.2e4, 1e4, 1e4]

      for l in range(len(pt_cut)):

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-2.,2.)", gen_pt_cut(pt_cut[l]))
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-2.,2.)", gen_pt_cut(pt_cut[l]))
	evt_tree3.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp3(64,-2.,2.)", gen_pt_cut(pt_cut[l]))

	htemp=gROOT.FindObject("htemp") ; htemp2=gROOT.FindObject("htemp2") ; htemp3=gROOT.FindObject("htemp3")
	htemp.SetLineColor(kRed) ; htemp2.SetLineColor(kGreen+2) ; htemp3.SetLineColor(kBlue)
	htemp.Draw() ; htemp2.Draw("same") ; htemp3.Draw("same")

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
        makePlot(c1,  "resolutions/ptres1D_DiffOverGen_pt"+str(pt_str[l]))

    if options.res1D_invDiffOverInvGen:

      for l in range(len(pt_cut)):

	c1 = TCanvas("c1")
	evt_tree.Draw("(((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp(64,-20.,20.)", gen_pt_cut(pt_cut[l]))
	evt_tree2.Draw("(((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp2(64,-20.,20.)", gen_pt_cut(pt_cut[l]))
	evt_tree3.Draw("(((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp3(64,-20.,20.)", gen_pt_cut(pt_cut[l]))

	htemp=gROOT.FindObject("htemp") ; htemp2=gROOT.FindObject("htemp2") ; htemp3=gROOT.FindObject("htemp3")
	htemp.SetLineColor(kRed) ; htemp2.SetLineColor(kGreen+2) ; htemp2.SetLineColor(kBlue)
	htemp.Draw() ; htemp2.Draw("same") ; htemp3.Draw("same")

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
        makePlot(c1, "resolutions/ptres1D_invDiffOverInvGen_pt"+str(pt_str[l]))

    if options.res1DvsPt and options.single_pt: print "Error: Must set single_pt to false in order to plot resolutions vs Pt."
    if options.res1DvsPt and not options.single_pt:

      ## ============== Inverse Pt Diff Over Inverse GEN ================

      res1 = [] ; res2 = [] ; res3 = [] ; res4 = [] ; res5 = [] ; res6 = []
      res1Err = [] ; res2Err = [] ; res3Err = [] ; res4Err = [] ; res5Err = [] ; res6Err = []
      zeros=[]

      for l in range(len(pt_cut)):

	evt_tree1.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp1(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp1 = gPad.GetPrimitive("htemp1") ; htemp1.Draw()
	res1.append(htemp1.GetRMS()) ; res1Err.append(htemp1.GetRMSError())
	c1.Close()

	evt_tree2.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp2(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res2.append(htemp2.GetRMS()) ; res2Err.append(htemp2.GetRMSError())
	c1.Close()

	evt_tree3.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp3(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp3 = gPad.GetPrimitive("htemp3") ; htemp3.Draw()
	res3.append(htemp3.GetRMS()) ; res3Err.append(htemp3.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree4.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp4(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp4 = gPad.GetPrimitive("htemp4") ; htemp4.Draw()
	res4.append(htemp4.GetRMS()) ; res4Err.append(htemp4.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree5.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp5(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp5 = gPad.GetPrimitive("htemp5") ; htemp5.Draw()
	res5.append(htemp5.GetRMS()) ; res5Err.append(htemp5.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree6.Draw("((1./GEN_pt) - (1./(2**(BDTG_AWB_Sq))))/(1./GEN_pt)>>htemp6(64,-20.,20.)", bdt_pt_cut(pt_cut[l]))
	htemp6 = gPad.GetPrimitive("htemp6") ; htemp6.Draw()
	res6.append(htemp6.GetRMS()) ; res6Err.append(htemp6.GetRMSError())
	c1.Close()

	zeros.append(0.)


      c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
      g1 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res1), np.array(zeros) , np.array(res1Err))
      g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
      g2 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res2), np.array(zeros) , np.array(res2Err))
      g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)
      g3 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res3), np.array(zeros) , np.array(res3Err))
      g3.SetMarkerStyle(8) ; g3.SetMarkerSize(1) ; g3.SetMarkerColor(kGreen+2)
      g4 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res4), np.array(zeros) , np.array(res4Err))
      g4.SetMarkerStyle(8) ; g4.SetMarkerSize(1) ; g4.SetMarkerColor(kBlack)
      g5 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res5), np.array(zeros) , np.array(res5Err))
      g5.SetMarkerStyle(8) ; g5.SetMarkerSize(1) ; g5.SetMarkerColor(7)
      g6 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res6), np.array(zeros) , np.array(res6Err))
      g6.SetMarkerStyle(8) ; g6.SetMarkerSize(1) ; g6.SetMarkerColor(40)

      mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Add(g3) ; mg.Add(g4) ; mg.Add(g5) ; mg.Add(g6) ; mg.Draw('ap')
      mg.GetXaxis().SetTitle('p_{T}^{GEN}')
      mg.GetYaxis().SetTitle('#sigma ((p_{T,GEN}^{-1} - p_{T,L1}^{-1}) / p_{T,GEN}^{-1})')

      #leg = TLegend(0.13, 0.66, 0.45, 0.87) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g3, "Run-3 BDT (HS precision dPhi)") ; leg.AddEntry(g1, "Run-3 BDT (ES precision dPhi)") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      makePlot(c1, "resolutions/res_vs_pt_invDiffOverInvGen_enhancedDPhi_slopeRemoved")

      ## ============== Pt Diff Over GEN ================

      res1 = [] ; res2 = [] ; res3 = [] ; res4 = [] ; res5 = [] ; res6 = []
      res1Err = [] ; res2Err = [] ; res3Err = [] ; res4Err = [] ; res5Err = [] ; res6Err = []
      zeros=[]

      for l in range(len(pt_cut)):

	evt_tree1.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp1(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp1 = gPad.GetPrimitive("htemp1") ; htemp1.Draw()
	res1.append(htemp1.GetRMS()) ; res1Err.append(htemp1.GetRMSError())
	c1.Close()

	evt_tree2.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp2(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res2.append(htemp2.GetRMS()) ; res2Err.append(htemp2.GetRMSError())
	c1.Close()

	evt_tree3.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp3(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp3 = gPad.GetPrimitive("htemp3") ; htemp3.Draw()
	res3.append(htemp3.GetRMS()) ; res3Err.append(htemp3.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree4.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp4(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp4 = gPad.GetPrimitive("htemp4") ; htemp4.Draw()
	res4.append(htemp4.GetRMS()) ; res4Err.append(htemp4.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree5.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp5(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp5 = gPad.GetPrimitive("htemp5") ; htemp5.Draw()
	res5.append(htemp5.GetRMS()) ; res5Err.append(htemp5.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree6.Draw("(GEN_pt - (2**(BDTG_AWB_Sq)))/(GEN_pt)>>htemp6(64,-3.,3.)", bdt_pt_cut(pt_cut[l]))
	htemp6 = gPad.GetPrimitive("htemp6") ; htemp6.Draw()
	res6.append(htemp6.GetRMS()) ; res6Err.append(htemp6.GetRMSError())
	c1.Close()

	zeros.append(0.)

      c1 = TCanvas( 'c1', 'test scatter', 200, 10, 700, 500)
      g1 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res1), np.array(zeros) , np.array(res1Err))
      g1.SetMarkerStyle(8) ; g1.SetMarkerSize(1) ; g1.SetMarkerColor(kBlue)
      g2 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res2), np.array(zeros) , np.array(res2Err))
      g2.SetMarkerStyle(8) ; g2.SetMarkerSize(1) ; g2.SetMarkerColor(kRed)
      g3 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res3), np.array(zeros) , np.array(res3Err))
      g3.SetMarkerStyle(8) ; g3.SetMarkerSize(1) ; g3.SetMarkerColor(kGreen+2)
      g4 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res4), np.array(zeros) , np.array(res4Err))
      g4.SetMarkerStyle(8) ; g4.SetMarkerSize(1) ; g4.SetMarkerColor(kBlack)
      g5 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res5), np.array(zeros) , np.array(res5Err))
      g5.SetMarkerStyle(8) ; g5.SetMarkerSize(1) ; g5.SetMarkerColor(7)
      g6 = TGraphErrors(len(pt_cut), np.array(pt_cut), np.array(res6), np.array(zeros) , np.array(res6Err))
      g6.SetMarkerStyle(8) ; g6.SetMarkerSize(1) ; g6.SetMarkerColor(40)

      mg = TMultiGraph() ; mg.Add(g1) ; mg.Add(g2) ; mg.Add(g3) ; mg.Add(g4) ; mg.Add(g5) ; mg.Add(g6) ; mg.Draw('ap')
      mg.GetXaxis().SetTitle('p_{T}^{GEN}')
      mg.GetYaxis().SetTitle('#sigma ((p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN})')

      #leg = TLegend(0.13, 0.15, 0.55, 0.47) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g3, "Run-3 BDT (HS precision dPhi)") ; leg.AddEntry(g1, "Run-3 BDT (ES precision dPhi)") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      makePlot(c1, "resolutions/res_vs_pt_diffOverGen_nonEnhanced")

  if options.res1DvsEta:

    eta_min1 = [-2.4, -2.2, -2.0, -1.8, -1.6, -1.4]
    eta_min2 = [1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
    eta_max1 = [-2.2, -2.0, -1.8, -1.6, -1.4, -1.2]
    eta_max2 = [1.4, 1.6, 1.8, 2.0, 2.2, 2.4]

    ## ============== Inverse Pt Diff Over Inverse GEN ================

    for k in range(len(pt_cut)):

      res = [] ; res2 = [] ; resErr = [] ; res2Err = [] ; zeros=[]

      for l in range(len(eta_min1)):

	c1 = TCanvas("c1")
	evt_tree2.Draw("((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
	res.append(htemp.GetRMS()) ; resErr.append(htemp.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree2.Draw("((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp2(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res.append(htemp2.GetRMS()) ; resErr.append(htemp2.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp3(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp3 = gPad.GetPrimitive("htemp3") ; htemp3.Draw()
	res2.append(htemp3.GetRMS()) ; res2Err.append(htemp3.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("((1./GEN_pt) - (1./(1.2 * (2**(BDTG_AWB_Sq)))))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))))/(1./GEN_pt)>>htemp4(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
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
      mg.GetYaxis().SetTitle('#sigma ((p_{T}^{GEN} - p_{T}^{L1})^{-1} / (p_{T}^{GEN})^{-1})')

      lat_scale = [0.87, 0.91, 0.935, 0.965, 0.985, 1.01, 1.08, 1.11, 1.15, 1.215]
      la = TLatex() ; la.SetTextFont(22) ; la.SetTextColor(kBlack) ; la.SetTextSize(0.031) ; la.SetTextAlign(10)
      la.DrawLatex( -0.62, lat_scale[k], "Mode 15, p_{T}^{L1} > "+str(int(pt_cut[k]))+" GeV")

      leg = TLegend(0.40, 0.61, 0.62, 0.85) ; leg.AddEntry(g2, "Run-2 BDT") ; leg.AddEntry(g1, "Run-3 BDT") ; leg.SetBorderSize(0) ; leg.Draw("same")

      c1.Update()
      makePlot(c1, "resolutions/res_vs_eta_InvDiffOverInvGen_pt"+str(pt_str[k]))

    ## ============== Pt Diff Over GEN ================

    for k in range(len(pt_cut)):

      res = [] ; res2 = [] ; resErr = [] ; res2Err = [] ; zeros=[]

      for l in range(len(eta_min1)):

	c1 = TCanvas("c1")
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp = gPad.GetPrimitive("htemp") ; htemp.Draw()
	res.append(htemp.GetRMS()) ; resErr.append(htemp.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree2.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp2(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
	htemp2 = gPad.GetPrimitive("htemp2") ; htemp2.Draw()
	res.append(htemp2.GetRMS()) ; resErr.append(htemp2.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp3(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min1[l])+" && GEN_eta<"+str(eta_max1[l]))
	htemp3 = gPad.GetPrimitive("htemp3") ; htemp3.Draw()
	res2.append(htemp3.GetRMS()) ; res2Err.append(htemp3.GetRMSError())
	c1.Close()

	c1 = TCanvas("c1")
	evt_tree.Draw("(GEN_pt - (1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq)))))/(GEN_pt)>>htemp4(64,-3.,3.)", gen_pt_cut(pt_cut[k])+" && GEN_eta>"+str(eta_min2[l])+" && GEN_eta<"+str(eta_max2[l]))
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
      makePlot(c1, "resolutions/res_vs_eta_diffOverGen_pt"+str(pt_str[k]))


  if False:#:options.res2D:

    c1 = TCanvas("c1")
    line = TLine(0, 0, 5.7, 5.7) ; line.SetLineColor(kRed) ; line.SetLineStyle(7)

    #Run-2 BDT
    evt_tree.Draw("log2((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))):log2(GEN_pt)>>htemp(100,0,5.7,100,0,6.5)", "", "COLZ")
    htemp = gPad.GetPrimitive("htemp")
    htemp.SetTitle("Mode 15 CSC-only Run-2 BDT, uncompressed (test) vs log2(p_{T}^{GEN})")
    htemp.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp.GetYaxis().SetTitle("Run-2 Scaled trigger log2(p_{T}^{BDT})")
    line.Draw("same")
    gPad.SetLogz() ; gPad.Update() ; gStyle.SetOptStat(0)
    makePlot(c1, "resolutions/ptres2D_Run2BDT")

    #Run-3 BDT
    evt_tree2.Draw("log2((1.2 * (2**(BDTG_AWB_Sq)))/(1 - (0.004 * (2**(BDTG_AWB_Sq))))):log2(GEN_pt)>>htemp2(100,0,5.7,100,0,6.5)", "", "COLZ")
    htemp2 = gPad.GetPrimitive("htemp2")
    htemp2.SetTitle("Mode 15 CSC-only Run-3 BDT, uncompressed (test) vs log2(p_{T}^{GEN})")
    htemp2.GetXaxis().SetTitle("log2(p_{T}^{GEN})") ; htemp2.GetYaxis().SetTitle("Run-3 Scaled trigger log2(p_{T}^{BDT})")
    line.Draw("same")
    gPad.SetLogz() ; gPad.Update() ; gStyle.SetOptStat(0)
    makePlot(c1, "resolutions/ptres2D_Run3BDT")
