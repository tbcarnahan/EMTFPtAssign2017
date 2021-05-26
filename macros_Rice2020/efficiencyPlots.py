#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
import numpy as np
from array import *
from termcolor import colored
from optparse import OptionParser,OptionGroup

def efficiencyVsPt():
  print("Producing efficiency vs pT plots")
  pass

def efficiencyVsEta():
  print("Producing efficiency vs eta plots")
  pass

def efficiencyVsPhi():
  print("Producing efficiency vs phi plots")
  pass

def plotEfficiencies(options):
  if options.effVsPt:
    efficiencyVsPt()

  if options.effVsEta:
    efficiencyVsPt()

  if options.effVsPhi:
    efficiencyVsPhi()

"""
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

      makePlots(c1, plotDir, "BDT_eff_SD_pt{}_eta{}to{}".format(pt_str[l], eta_str_min[k], eta_str_max[k]))


if options.effVsEta:

  for l in range(len(pt_cut)):
    #Run2 and Run3 BDT efficiency vs Eta
    binning = "(64,-3.,3.)"
    effs = []

    c1 = newCanvas()
    for ee in range(0,len(trainings)):
      eff = draw_eff(evt_trees[ee], " ; #eta^{GEN} ; Trigger Efficiency", binning, "GEN_eta", gen_pt_cut(pt_cut[l]), bdt_pt_scaled_Run3(pt_cut[l]))
      eff.SetMarkerColor(markerColors[ee])
      eff.SetLineColor(lineColors[ee])
      eff.SetMarkerStyle(markerStyles[ee])
      eff.Draw(drawOptions[ee])
      effs.append(eff)

    leg = TLegend(0.35, 0.2, 0.6, 0.5);
    leg.SetHeader("p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.04)
    for ee in range(0,len(trainings)):
      leg.AddEntry(effs[ee], legendEntries[ee], "pl")
      leg.Draw("same")

    gPad.Update()
    gStyle.SetOptStat(0)
    graph = eff.GetPaintedGraph()
    graph.SetMinimum(0)
    graph.SetMaximum(1.1)
    graph.GetXaxis().SetLabelSize(0.05)
    graph.GetYaxis().SetLabelSize(0.05)
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)

    c1.Modified()
    c1.Update()
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)

    makePlots(c1, plotDir, "BDTeff_eta_pt"+str(pt_str[l]) )


if options.effVsPhi:

  for l in range(len(pt_cut)):
    #Run2 and Run3 BDT efficiency vs Phi
    binning = "(64,-3.2,3.2)"
    effs = []

    c1 = newCanvas()
    for ee in range(0,len(trainings)):
      eff = draw_eff(evt_trees[ee], " ; #phi^{GEN} ; Trigger Efficiency", binning, "GEN_phi", gen_pt_cut(pt_cut[l]), bdt_pt_scaled_Run3(pt_cut[l]))
      eff.SetMarkerColor(markerColors[ee])
      eff.SetLineColor(lineColors[ee])
      eff.SetMarkerStyle(markerStyles[ee])
      eff.Draw(drawOptions[ee])
      effs.append(eff)

    leg = TLegend(0.35, 0.2, 0.6, 0.5);
    leg.SetHeader("p_{T}^{GEN}, p_{T}^{L1} > "+str(pt_cut[l])+" GeV")
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetTextSize(0.04)
    for ee in range(0,len(trainings)):
      leg.AddEntry(effs[ee], legendEntries[ee], "pl")
      leg.Draw("same")

    gPad.Update()
    gStyle.SetOptStat(0)
    graph = eff.GetPaintedGraph()
    graph.SetMinimum(0)
    graph.SetMaximum(1.1)
    graph.GetXaxis().SetLabelSize(0.05)
    graph.GetYaxis().SetLabelSize(0.05)
    graph.GetXaxis().SetTitleSize(0.05)
    graph.GetYaxis().SetTitleSize(0.05)

    c1.Modified()
    c1.Update()
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)

    makePlots(c1, plotDir, "BDTeff_phi_pt"+str(pt_str[l]) )
"""
