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
from trainingDict import trainingDict
from tdrstyle import *
import CMS_lumi as CMS_lumi

iPeriod = 0
iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

## Configuration settings
parser = OptionParser()
parser.add_option('--batchMode', dest='batchMode', action='store_true',default = True)
parser.add_option("--eta_slices", dest="eta_slices", action="store_true", default = False)
parser.add_option("--single_pt", dest="single_pt", action="store_true", default = True)
parser.add_option("--addDateTime", dest="addDateTime", action="store", default = True)

parser.add_option("--effVsPt", dest="effVsPt", action="store_true", default = False)
parser.add_option("--effVsEta", dest="effVsEta", action="store_true", default = False)
parser.add_option("--effVsPhi", dest="effVsPhi", action="store_true", default = False)

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

mode = 7
pt_scaling_A = [1.3, 1.3, 1.3]
pt_scaling_B = [0.004, 0.004, 0.004]

if options.single_pt:
  pt_cut = [22]
  pt_str = ["22"]
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
  eta_min = [1.25]
  eta_max = [2.4]
  eta_str_min = ["1pt25"]
  eta_str_max = ["2pt4"]


## Data

trainings= [
  'Run2_Mode15_Compressed',
  'Run3_V1p0_Mode15_Compressed',
  'Run3_V1p1_Mode15_Compressed',
  'Run3_V1p2_Mode15_Compressed'
]

treeName = "f_logPtTarg_invPtWgt/TestTree"

evt_trees = []
for p in trainings:
  ttree = TChain(treeName)
  print("Reading file: {}".format(trainingDict[p][0]))
  ttree.Add(trainingDict[p][0])
  evt_trees.append(ttree)

legendEntries = []
for p in trainings:
  legendEntries.append(trainingDict[p][1])

markerColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
lineColors = [kBlue, kRed, kGreen+2, kBlack, kBlue, kRed, kGreen+2, kBlack]#, 7, 40]
markerStyles = [8,8,8,8,8]#,8,8]
drawOptions = ["AP", "same", "same", "same", "same"]#, "same", "same", "same", "same"]
drawOptions1D = ["", "same"]#, "same", "same", "same", "same"]
outFileString = ["Run2_dPhi12_23_34","Run3_dPhi12_23_34"]#, "Run3_bend1_bitCompr"]#"Run3QSBit", "Run3QSBitESBit"]

draw_res_axis_label = ["(p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN}", "(p_{T,GEN}^{-1} - p_{T,L1}^{-1}) / p_{T,GEN}^{-1}"]
draw_res_option = ["(GEN_pt - pow(2, BDTG_AWB_Sq))/GEN_pt", "(((1./GEN_pt) - (1./pow(2, BDTG_AWB_Sq)))/(1./GEN_pt))"]
draw_res_label = ["diffOverGen", "invDiffOverInvGen"]
res_type = ["mu", "sigma"]

## ================ Helper functions ======================
def gen_pt_cut(pt_min):
  return TCut("GEN_pt >= {0}".format(pt_min))

def gen_eta_cut(eta_min, eta_max):
  return TCut("GEN_eta >= {0} && GEN_eta <= {1}".format(eta_min, eta_max))

def mode_cut(mode):
  return TCut("TRK_mode == {0}".format(mode))

def bdt_pt_cut(pt_min):
  return TCut("pow(2, BDTG_AWB_Sq) >= {}".format(pt_min))

def bdt_pt_scaled(pt_scaling_A, pt_scaling_B, pt_min):
  return TCut("(({0} * pow(2,BDTG_AWB_Sq))/(1 - ({1} * pow(2,BDTG_AWB_Sq)))) >= {2}".format(pt_scaling_A, pt_scaling_B, pt_min))

def bdt_pt_scaled_Run2(pt_min):
  return bdt_pt_scaled(1.2, 0.015, pt_min)

def bdt_pt_scaled_Run3(pt_min):
  return bdt_pt_scaled(1.3, 0.004, pt_min)

def makePlots(canvas, plotTitle):
  c1.SaveAs(plotDir + plotTitle + ".png")
  c1.SaveAs(plotDir + plotTitle + ".pdf")
  c1.SaveAs(plotDir + plotTitle + ".C")

setTDRStyle()

## ================ Plotting script ======================
if options.effVsPt:

  for l in range(len(pt_cut)):
    for k in range(len(eta_min)):

      c1 = newCanvas()

      leg = TLegend(0.45, 0.23, 0.90, 0.50, "", "brNDC")
      leg.SetBorderSize(0)
      leg.SetFillStyle(0)
      leg.SetFillColor(0)
      leg.SetTextSize(0.04)
      gStyle.SetOptStat(0)

      #Run2 and Run3 BDT efficiency vs Pt
      effs = []
      for ee in range(0,len(trainings)):
        eff = draw_eff(evt_trees[ee], "; p_{T}^{GEN} (GeV) ; Trigger Efficiency", "(50,1.,50.)", "GEN_pt",
                       gen_eta_cut(eta_min[k], eta_max[k]), bdt_pt_scaled_Run3(pt_cut[l]))
        eff.SetMarkerColor(markerColors[ee])
        eff.SetLineColor(lineColors[ee])
        eff.SetMarkerStyle(markerStyles[ee])
        eff.Draw(drawOptions[ee])
        effs.append(eff)

        leg.AddEntry(effs[ee], legendEntries[ee], "pl")
        eff.Draw("same")

        gPad.Update()
        graph = eff.GetPaintedGraph()
        graph.SetMinimum(0)
        graph.SetMaximum(1.1)
        graph.GetXaxis().SetLabelSize(0.05)
        graph.GetYaxis().SetLabelSize(0.05)
        graph.GetXaxis().SetTitleSize(0.05)
        graph.GetYaxis().SetTitleSize(0.05)
        gPad.Update()

      leg.Draw("same")

      line = TLine(0, 0.9, 50, 0.9)
      line2 = TLine(pt_cut[l], 0., pt_cut[l], 1.1)
      line.SetLineStyle(7)
      line2.SetLineStyle(7)
      line.Draw("same")
      line2.Draw("same")

      tex = TLatex()
      tex.SetTextColor(kBlack)
      #tex.SetTextFont(22)
      tex.SetTextSize(0.05)
      tex.DrawLatex( 35, 0.09, "p_{T}^{L1} > "+str(int(pt_cut[l]))+" GeV")

      c1.Modified()
      c1.Update()
      CMS_lumi.CMS_lumi(c1, iPeriod, iPos)

      checkDir('./plots')
      checkDir('./plots/bdt_eff')
      makePlots(c1, "bdt_eff/BDT_eff_SD_pt{}_eta{}to{}".format(pt_str[l], eta_str_min[k], eta_str_max[k]))


if options.effVsEta:

  #Run2 and Run3 BDT efficiency vs Eta
  binning = "(64,-3.,3.)"
  effs = []

  c1 = newCanvas()
  for ee in range(0,2):
    eff = draw_eff(evt_trees[ee], " ; #eta^{GEN} ; Trigger Efficiency", binning, "GEN_eta", gen_pt_cut(pt_cut[l]), bdt_pt_scaled_Run2(pt_cut[l]))
    eff.SetMarkerColor(markerColors[ee])
    eff.SetLineColor(lineColors[ee])
    eff.SetMarkerStyle(markerStyles[ee])
    eff.Draw(drawOptions[ee])
    effs.append(eff)

    la1 = TLatex()
    la1.SetTextFont(22)
    la1.SetTextColor(1)
    la1.SetTextSize(0.033)
    la1.SetTextAlign(10)
    #Note that the position of the label in the following line is hard-coded onto the axis (easier way to do this?)
    la1.DrawLatex( -0.6, 0.65, "p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")

    leg = TLegend(0.40, 0.26, 0.67, 0.53) ;
    for ee in range(0,4):
      leg.AddEntry(effs[ee], legendEntries[ee])
      leg.SetBorderSize(0)
      leg.SetFillStyle(0)
      leg.SetTextSize(0.05)
      leg.Draw("same")

    gPad.Update()
    eff.SetTitle(" ; #eta^{GEN} ; Trigger Efficiency")
    gStyle.SetOptStat(0)
    graph = eff.GetPaintedGraph()
    graph.SetMinimum(0)
    graph.SetMaximum(1.1)

    checkDir('./plots')
    checkDir('./plots/bdt_eff')
    checkDir('./plots/bdt_eff/eta')
    makePlots(c1, "bdt_eff/eta/BDTeff_eta_pt"+str(pt_str[l]) )



if options.resolutions:

  if options.res1D:

    for k in range(len(draw_res_option)):

      for l in range(len(pt_cut)):

	resolutions = []

	for ee in range(0,2):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k] , bdt_pt(pt_cut[l]) )
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

	for ee in range(0,2):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]) )

	  mu_res[ee][l] = res.GetMean()
	  mu_res_err[ee][l] = res.GetMeanError()
	  sigma_res[ee][l] = res.GetRMS()
	  sigma_res_err[ee][l] = res.GetRMSError()

      draw_multi_resVsPt(len(evt_trees), mu_res, mu_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#mu '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsPt(len(evt_trees), sigma_res, sigma_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#sigma '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[1])



  if options.res1DvsEta:

    for k in range(len(draw_res_option)):

      #Define the eta range from the negative+positive endcap in a single array.
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

	  for ee in range(0,len(trainings)):
	    #Add a check to skip the bin at the boundary between endcaps (-1.2 to 1.2).
	    if i<len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i], eta_range[i+1]) )
	    if i>=len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i+1], eta_range[i+2]) )

	    mu_res[ee][i] = res.GetMean()
	    mu_res_err[ee][i] = res.GetMeanError()
	    sigma_res[ee][i] = res.GetRMS()
	    sigma_res_err[ee][i] = res.GetRMSError()

      #Remove the bins at the endcaps boundries that won't be plotted.
      eta_range.remove(-1*eta_min[0])
      eta_range.remove(eta_min[0])

      draw_multi_resVsEta(len(evt_trees), mu_res, mu_res_err, xErrors, '#eta^{GEN}', '#mu '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsEta(len(evt_trees), sigma_res, sigma_res_err, xErrors, '#eta^{GEN}', '#sigma '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[1])



  if options.res2D:

    for ee in range(0,len(trainings)):

      draw_res2D(evt_trees[ee], 100, 0, 5.7, 100, 0, 5.5, "BDTG_AWB_Sq:log2(GEN_pt)", legendEntries[ee], outFileString[ee])
