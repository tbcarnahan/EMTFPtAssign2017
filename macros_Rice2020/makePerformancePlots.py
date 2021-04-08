#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
from ROOT import *
import numpy as np
from array import *
from termcolor import colored
from ROOT import gROOT
from optparse import OptionParser,OptionGroup
from Helpers import *

## Configuration settings
parser = OptionParser()
parser.add_option('--batchMode', dest='batchMode', action='store_true',default = False)
parser.add_option("--eta_slices", dest="eta_slices", action="store_true", default = False)
parser.add_option("--single_pt", dest="single_pt", action="store_true", default = False)
parser.add_option("--addDateTime", dest="addDateTime", action="store", default = True)

parser.add_option("--efficiencies", dest="efficiencies", action="store_true", default = False)
parser.add_option("--EffVsPt", dest="EffVsPt", action="store_true", default = False)
parser.add_option("--EffVsEta", dest="EffVsEta", action="store_true", default = False)

parser.add_option("--resolutions", dest="resolutions", action="store_true", default = False)
parser.add_option("--res1D", dest="res1D", action="store_true", default = False)
parser.add_option("--res1DvsPt", dest="res1DvsPt", action="store_true", default = False)
parser.add_option("--res1DvsEta", dest="res1DvsEta", action="store_true", default = False)
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
  eta_min = [2.1]
  eta_max = [2.4]
  eta_str_min = ["1pt2"]
  eta_str_max = ["2pt4"]


## Data
#prefix = "root://cmseos.fnal.gov//store/user/dildick/"
prefix = "root://cmseos.fnal.gov//store/user/mdecaro/"
fileName = "PtRegressionRun3Prep_MODE_15_noBitCompr.root"
trainings= [
  #'EMTF_BDT_Train_Test3DPhi_eta1.2to1.55_isRun2_Selection0x1c_20210406_122416/',
  #'EMTF_BDT_Train_Test3DPhi_eta1.2to1.55_isRun3_Selection0x1c_20210406_122517/',
  #'EMTF_BDT_Train_Test3DPhi_eta1.2to1.55_isRun3_useQSBit_Selection0x1c_20210406_122618/',
  #'EMTF_BDT_Train_Test3DPhi_eta1.2to1.55_isRun3_useQSBit_useESBit_Selection0x1c_20210406_122719/',

  'EMTF_BDT_Train_Test3DPhi_eta2.1to2.4_isRun2_Selection0x1c_20210406_122820/',
  'EMTF_BDT_Train_Test3DPhi_eta2.1to2.4_isRun3_Selection0x1c_20210406_122920/',
  'EMTF_BDT_Train_Test3DPhi_eta2.1to2.4_isRun3_useQSBit_Selection0x1c_20210406_123021/',
  'EMTF_BDT_Train_Test3DPhi_eta2.1to2.4_isRun3_useQSBit_useESBit_Selection0x1c_20210406_123918/'
]

treeName = "f_MODE_15_logPtTarg_invPtWgt_noBitCompr/TestTree"

evt_trees = []
for p in trainings:
  ttree = TChain(treeName)
  fName = "{}{}{}".format(prefix,p,fileName)
  print("Reading file: {}".format(fName))
  ttree.Add(fName)
  evt_trees.append(ttree)

markerColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
lineColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
markerStyles = [8,8,8,8]#,8,8,8,8]
drawOptions = ["AP", "same", "same", "same"]#, "same", "same", "same", "same"]
drawOptions1D = ["", "same", "same", "same"]#, "same", "same", "same", "same"]
legendEntries = ["Run-2", "Run-3", "Run-3 QSBit", "Run-3 QSBit ESBit"]

draw_res_axis_label = ["(p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN}", "(p_{T,GEN}^{-1} - p_{T,L1}^{-1}) / p_{T,GEN}^{-1}"]
draw_res_option = ["(GEN_pt - pow(2, BDTG_AWB_Sq))/GEN_pt", "(((1./GEN_pt) - (1./pow(2, BDTG_AWB_Sq)))/(1./GEN_pt))"] 
draw_res_label = ["diffOverGen", "invDiffOverInvGen"]
res_type = ["mu", "sigma"]

## ================ Helper functions ======================
def gen_pt_cut(pt_min):
  return TCut("GEN_pt >= {0}".format(pt_min))

def gen_eta_cut(eta_min, eta_max):
  return TCut("GEN_eta >= {0} && GEN_eta <= {1}".format(eta_min, eta_max))

def bdt_pt_cut(pt_min):
  return TCut("pow(2, BDTG_AWB_Sq) >= {}".format(pt_min))

def bdt_pt_scaled_cut(pt_min):
  return TCut("(1.2 * pow(2,BDTG_AWB_Sq)))/(1 - (0.004 * pow(2,BDTG_AWB_Sq))) >= {}".format(pt_min))

def makePlots(canvas, plotTitle):
  c1.SaveAs(plotDir + plotTitle + ".png")
  c1.SaveAs(plotDir + plotTitle + ".pdf")
  c1.SaveAs(plotDir + plotTitle + ".C")

## ================ Plotting script ======================
if options.efficiencies:

  for l in range(len(pt_cut)):
    for k in range(len(eta_min)):

      c1 = TCanvas("c1")

      if options.EffVsPt:

	leg = TLegend(0.6, 0.33, 0.9, 0.63)
	leg.SetBorderSize(0)
	gStyle.SetOptStat(0)

	#Run2 and Run3 BDT efficiency vs Pt
        effs = []
        for ee in range(0,4):
          eff = draw_eff(evt_trees[ee], "; p_{T}^{GEN} (GeV) ; Trigger Efficiency", "(50,1.,50.)", "GEN_pt",
                         gen_eta_cut(eta_min[k], eta_max[k]), bdt_pt_cut(pt_cut[l]))
          eff.SetMarkerColor(markerColors[ee])
          eff.SetLineColor(lineColors[ee])
          eff.SetMarkerStyle(markerStyles[ee])
          eff.Draw(drawOptions[ee])
          effs.append(eff)
          leg.AddEntry(effs[ee], legendEntries[ee])
          #graph = eff.GetPaintedGraph()
          #graph.SetMinimum(0)
          #graph.SetMaximum(1.1)
          eff.Draw("same")
        """
        line = TLine(0, 0.5, 50, 0.5)
	line2 = TLine(pt_cut[l], 0., pt_cut[l], 1.1)
	line.SetLineStyle(7) ; line2.SetLineStyle(7)
        line.Draw("same") ; line2.Draw("same")

	la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.035) ; la1.SetTextAlign(10)
	la1.DrawLatex( 35., 0.2, "p_{T}^{L1} > "+str(pt_cut[l])+" GeV")
	la2 = TLatex() ; la2.SetTextFont(22) ; la2.SetTextColor(1) ; la2.SetTextSize(0.035) ; la2.SetTextAlign(10)
	la2.DrawLatex( 35., 0.1, str(eta_min[k])+" < |#eta^{GEN}| < "+str(eta_max[k]))
        """

        leg.Draw("same")

        checkDir('./plots') ; checkDir('./plots/bdt_eff')
        makePlots(c1, "bdt_eff/BDT_eff_SD_pt{}_eta{}to{}".format(pt_str[l], eta_str_min[k], eta_str_max[k]))


    if options.EffVsEta:

      #Run2 and Run3 BDT efficiency vs Eta
      binning = "(64,-3.,3.)"
      effs = []

      for ee in range(0,4):
        eff = draw_eff(evt_trees[ee], " ; #eta^{GEN} ; Trigger Efficiency", binning, "GEN_eta", gen_pt_cut(pt_cut[l]), bdt_pt_cut(pt_cut[l]))
        eff.SetMarkerColor(markerColors[ee])
        eff.SetLineColor(lineColors[ee])
        eff.SetMarkerStyle(markerStyles[ee])
        eff.Draw(drawOptions[ee])
        effs.append(eff)

      la1 = TLatex() ; la1.SetTextFont(22) ; la1.SetTextColor(1) ; la1.SetTextSize(0.033) ; la1.SetTextAlign(10)
      #Note that the position of the label in the following line is hard-coded onto the axis (easier way to do this?)
      la1.DrawLatex( -0.6, 0.65, "p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")

      leg = TLegend(0.40, 0.26, 0.67, 0.53) ;
      for ee in range(0,4):
        leg.AddEntry(effs[ee], legendEntries[ee])
      leg.SetBorderSize(0)
      leg.Draw("same")

      gPad.Update()
      eff.SetTitle(" ; #eta^{GEN} ; Trigger Efficiency")
      gStyle.SetOptStat(0)
      graph = eff.GetPaintedGraph() ; graph.SetMinimum(0) ;  graph.SetMaximum(1.003)

      checkDir('./plots') ; checkDir('./plots/bdt_eff') ; checkDir('./plots/bdt_eff/eta')
      makePlots(c1, "bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l]) )
     


if options.resolutions:

  if options.res1D:

    for k in range(len(draw_res_option)):

      for l in range(len(pt_cut)):

	resolutions = []

	for ee in range(0,4):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k] , bdt_pt_cut(pt_cut[l]) )
	  resolutions.append(res)

	checkDir('./plots') ; checkDir('./plots/resolutions')

	c1 = TCanvas("c1")
	draw_multiple(resolutions, " ; "+draw_res_axis_label[k]+" ; ", drawOptions1D, lineColors, legendEntries, pt_cut[l]) 
	makePlots(c1,  "resolutions/ptres1D_"+draw_res_label[k]+"_pt"+str(pt_str[l]) )
	c1.Close()

    
  if options.res1DvsPt and options.single_pt: print "Error: Must set single_pt to false in order to plot resolutions vs Pt."
  if options.res1DvsPt and not options.single_pt:

    mu_res = np.empty((len(evt_trees),len(pt_cut)))
    mu_res_err = np.empty((len(evt_trees),len(pt_cut)))
    sigma_res = np.empty((len(evt_trees),len(pt_cut)))
    sigma_res_err = np.empty((len(evt_trees),len(pt_cut)))
    xErrors = np.zeros((len(evt_trees),len(pt_cut)))

    for k in range(len(draw_res_option)):

      for l in range(len(pt_cut)):

	for ee in range(0,4):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt_cut(pt_cut[l]) )
	  
	  mu_res[ee][l] = res.GetMean()
	  mu_res_err[ee][l] = res.GetMeanError()
	  sigma_res[ee][l] = res.GetRMS()
	  sigma_res_err[ee][l] = res.GetRMSError()

      draw_multi_resVsPt(len(evt_trees), mu_res, mu_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#mu '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsPt(len(evt_trees), sigma_res, sigma_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#sigma '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[1])

      
  
  if options.res1DvsEta:

    for k in range(len(draw_res_option)):

      #The plotter has trouble between bins -1.2 to 1.2, so the resolutions in the negative and positive endcaps are drawn seperately and then plotted together.
      eta_range = []
      nbins = int(round(abs((float(eta_min[0]) -  float(eta_max[0]) ) / 0.1)))

      for i in range(nbins+1):	
	eta_range.append(round(-1*float(eta_max[0]) + 0.1*i,1))
      for i in range(nbins+1):
	eta_range.append(round(float(eta_min[0]) + 0.1*i,1))

      #2x2 arrays to hold the mean and width (and errors) of the pt resolutions.
      mu_res = np.zeros((len(evt_trees),len(eta_range)-2))
      mu_res_err = np.zeros((len(evt_trees),len(eta_range)-2))
      sigma_res = np.zeros((len(evt_trees),len(eta_range)-2))
      sigma_res_err = np.zeros((len(evt_trees),len(eta_range)-2))
      xErrors = np.zeros((len(evt_trees),len(eta_range)-2))

      for l in range(len(pt_cut)):

	for i in range(len(eta_range)-2):

	  for ee in range(0,4):
	    if i<len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt_cut(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i], eta_range[i+1]) )
	    if i>=len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt_cut(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i+1], eta_range[i+2]) )

	    mu_res[ee][i] = res.GetMean()
	    mu_res_err[ee][i] = res.GetMeanError()
	    sigma_res[ee][i] = res.GetRMS()
	    sigma_res_err[ee][i] = res.GetRMSError()

      #Remove the bins at the edge of the endcaps that won't be plotted.
      eta_range.remove(-1*eta_min[0])
      eta_range.remove(eta_min[0])

      draw_multi_resVsEta(len(evt_trees), mu_res, mu_res_err, xErrors, '#eta^{GEN}', '#mu '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsEta(len(evt_trees), sigma_res, sigma_res_err, xErrors, '#eta^{GEN}', '#sigma '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[1])
      

  '''
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
'''
