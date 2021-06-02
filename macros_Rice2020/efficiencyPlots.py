#! /usr/bin/env python
# -*- coding: utf-8 -*-

from termcolor import colored
from tdrstyle import *
from CMS_lumi import *
from helpers import *
from ROOT import *


def efficiencyVsPt_PtCutEtaSlice(emtfMode, plotter, ptCutIndex, etaSliceIndex):
  ptCut = plotter.options.emtfPtCuts[ptCutIndex]
  etaMin = plotter.options.etaMins[etaSliceIndex]
  etaMax = plotter.options.etaMaxs[etaSliceIndex]
  etaMinStr = str(etaMin).replace('.','p')
  etaMaxStr = str(etaMax).replace('.','p')

  if plotter.options.verbosity >= 3:
    print(colored("\tpT cut: {}, eta_min: {}, eta_max: {}".format(ptCut, etaMin, etaMax), 'green'))

  c1 = newCanvas()
  leg = TLegend(0.45, 0.23, 0.90, 0.50, "", "brNDC")
  leg.SetHeader("p_{T}^{GEN}, p_{T}^{L1} #geq %d GeV"%ptCut)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.04)
  gStyle.SetOptStat(0)

  #Run2 and Run3 BDT efficiency vs Pt
  effs = []
  for ee in range(0,len(plotter.eventTrees)):
    eff = draw_eff(plotter.eventTrees[ee], "; p_{T}^{GEN} (GeV) ; Trigger Efficiency", "(50,1.,50.)", "GEN_pt",
                   gen_eta_cut(etaMin, etaMax),
                   bdt_pt_scaled_Run3(ptCut))
    eff.SetMarkerColor(plotter.emtfColors[ee])
    eff.SetLineColor(plotter.emtfColors[ee])
    eff.SetMarkerStyle(8)
    eff.Draw(plotter.emtfDrawOptions[ee])
    effs.append(eff)
    leg.AddEntry(effs[ee], plotter.legendEntries[ee], "pl")

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
  line2 = TLine(ptCut, 0., ptCut, 1.1)
  line.SetLineStyle(7)
  line2.SetLineStyle(7)
  line.Draw("same")
  line2.Draw("same")

  c1.Modified()
  c1.Update()
  CMS_lumi.CMS_lumi(c1, plotter.iPeriod, plotter.iPos)

  makePlots(c1, plotter.plotDir, "BDT_eff_pt_mode{}_pt{}_eta{}to{}".format(emtfMode, ptCut, etaMinStr, etaMaxStr))


def efficiencyVsEta_PtCut(emtfMode, plotter, ptCutIndex):
  ptCut = plotter.options.emtfPtCuts[ptCutIndex]

  if plotter.options.verbosity >= 3:
    print(colored("\tpT cut: {}".format(ptCut), 'green'))

  #Run2 and Run3 BDT efficiency vs Eta
  binning = "(64,-3.,3.)"
  effs = []

  c1 = newCanvas()
  leg = TLegend(0.35, 0.2, 0.6, 0.5);
  leg.SetHeader("p_{T}^{GEN}, p_{T}^{L1} #geq %d GeV"%ptCut)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.04)
  gStyle.SetOptStat(0)

  for ee in range(0,len(plotter.eventTrees)):
    eff = draw_eff(plotter.eventTrees[ee], " ; #eta^{GEN} ; Trigger Efficiency", binning, "GEN_eta", gen_pt_cut(ptCut), bdt_pt_scaled_Run3(ptCut))
    eff.SetMarkerColor(plotter.emtfColors[ee])
    eff.SetLineColor(plotter.emtfColors[ee])
    eff.SetMarkerStyle(8)
    eff.Draw(plotter.emtfDrawOptions[ee])
    effs.append(eff)
    leg.AddEntry(effs[ee], plotter.legendEntries[ee], "pl")

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

  c1.Modified()
  c1.Update()
  CMS_lumi.CMS_lumi(c1, plotter.iPeriod, plotter.iPos)

  makePlots(c1, plotter.plotDir, "BDT_eff_eta_mode{}_pt{}".format(emtfMode, ptCut))


def efficiencyVsPhi_PtCut(emtfMode, plotter, ptCutIndex):
  ptCut = plotter.options.emtfPtCuts[ptCutIndex]
  etaMin = 1.25
  etaMax = 2.4
  etaMinStr = str(etaMin).replace('.','p')
  etaMaxStr = str(etaMax).replace('.','p')

  if plotter.options.verbosity >= 3:
    print(colored("\tpT cut: {}, eta_min: {}, eta_max: {}".format(ptCut, etaMin, etaMax), 'green'))

  #Run2 and Run3 BDT efficiency vs Phi
  binning = "(64,-3.,3.)"
  effs = []

  c1 = newCanvas()
  leg = TLegend(0.35, 0.2, 0.6, 0.5, "", "brNDC");
  leg.SetHeader("p_{T}^{GEN}, p_{T}^{L1} #geq %d GeV"%ptCut)
  leg.SetBorderSize(0)
  leg.SetFillStyle(0)
  leg.SetFillColor(0)
  leg.SetTextSize(0.04)
  gStyle.SetOptStat(0)

  for ee in range(0,len(plotter.eventTrees)):
    eff = draw_eff(plotter.eventTrees[ee], " ; #phi^{GEN} ; Trigger Efficiency",
                   binning, "GEN_phi", gen_pt_cut(ptCut), bdt_pt_scaled_Run3(ptCut))
    eff.SetMarkerColor(plotter.emtfColors[ee])
    eff.SetLineColor(plotter.emtfColors[ee])
    eff.SetMarkerStyle(8)
    eff.Draw(plotter.emtfDrawOptions[ee])
    effs.append(eff)
    leg.AddEntry(effs[ee], plotter.legendEntries[ee], "pl")

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

  c1.Modified()
  c1.Update()
  CMS_lumi.CMS_lumi(c1, plotter.iPeriod, plotter.iPos)

  makePlots(c1, plotter.plotDir, "BDT_eff_phi_mode{}_pt{}".format(emtfMode, ptCut))


def efficiencyVsPt(plotter):
  if plotter.options.verbosity >= 2:
    print(colored("Producing efficiency vs pT plots for mode {}".format(plotter.emtfMode), 'green'))

  for l in range(0,len(plotter.options.emtfPtCuts)):
    for k in range(0,len(plotter.options.etaMins)):
      efficiencyVsPt_PtCutEtaSlice(plotter.emtfMode, plotter, l, k)


def efficiencyVsEta(plotter):
  if plotter.options.verbosity >= 2:
    print(colored("Producing efficiency vs eta plots for mode {}".format(plotter.emtfMode), 'green'))

  for l in range(0,len(plotter.options.emtfPtCuts)):
    efficiencyVsEta_PtCut(plotter.emtfMode, plotter, l)


def efficiencyVsPhi(plotter):
  if plotter.options.verbosity >= 2:
    print(colored("Producing efficiency vs phi plots for mode {}".format(plotter.emtfMode), 'green'))

  for l in range(0,len(plotter.options.emtfPtCuts)):
    efficiencyVsPhi_PtCut(plotter.emtfMode, plotter, l)


def plotEfficienciesSingleMode(plotter):

  if plotter.options.effVsPt:
    efficiencyVsPt(plotter)

  if plotter.options.effVsEta:
    efficiencyVsEta(plotter)

  if plotter.options.effVsPhi:
    efficiencyVsPhi(plotter)
