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


## ============== Event branches================
evt_tree  = TChain('MuonNtuplizer/FlatTree')
out_file  = TFile('Histograms.root','recreate')

## ================ Read input files, define Output file ======================
dir1 = '/uscms_data/d3/dildick/work/NewCSCTriggerPatterns/CMSSW_11_2_0_pre5/src/'
file_name = dir1+"out_ana_phase2.forMatthew.root"
evt_tree.Add(file_name)

h_sDx_even = TH1D('h_sDx_p_even', '', 32, -2, 8)
h_sDx_odd = TH1D('h_sDx_p_odd', '', 32, 1, 14)

h_dPad_before_even = TH1D('h_dPad_before_even', '', 32, -12, 12)
h_dPad_before_odd = TH1D('h_dPad_before_odd', '', 32, -30, 30)
h_dPad_after_even = TH1D('h_dPad_after_even', '', 32, -12, 12)
h_dPad_after_odd = TH1D('h_dPad_after_odd', '', 32, -30, 30)

h_eta_denom = TH1D('h_eta_denom', '', 64, 1.6, 2.1)
h_eta_numer_csc = TH1D('h_eta_numer_csc', '', 64, 1.6, 2.1)
h_eta_numer_gempad = TH1D('h_eta_numer_gempad', '', 64, 1.6, 2.1)
h_eta_numer_gemcopad = TH1D('h_eta_numer_gemcopad', '', 64, 1.6, 2.1)

h_pt_denom = TH1D('h_pt_denom', '', 128, 9.9, 10.1)
h_pt_numer_csc = TH1D('h_pt_numer_csc', '', 128, 9.9, 10.1)
h_pt_numer_gempad = TH1D('h_pt_numer_gempad', '', 128, 9.9, 10.1)
h_pt_numer_gemcopad = TH1D('h_pt_numer_gemcopad', '', 128, 9.9, 10.1)

#for iEvt in range(2000000):
for iEvt in range(evt_tree.GetEntries()):
  if MAX_EVT > 0 and iEvt > MAX_EVT: break
  if iEvt % PRT_EVT is 0: print 'Event #', iEvt
  evt_tree.GetEntry(iEvt)

  chamber0 = -1 ; chamber1 = -1
  strip0 = -1 ; strip1 = -1; pad0 = -1 ; pad1 = -1

  
  #Code for efficiency plots
  if len(evt_tree.gen_tpid)==2: 
    
    #First muon (tpid == 0)
    for i in range(len(evt_tree.gen_tpid)):
      h_eta_denom.Fill(abs(evt_tree.gen_eta[i]))
      if abs(evt_tree.gen_eta[i])>1.6 and abs(evt_tree.gen_eta[i])<2.1: h_pt_denom.Fill(evt_tree.gen_pt[i])

    for i in range(len(evt_tree.lct_tpid)):
      if evt_tree.lct_tpid[i]==0 and evt_tree.lct_station[i]==1 and evt_tree.lct_ring[i]==1: 
	chamber0 = evt_tree.lct_chamber[i] ; pattern0 = evt_tree.lct_pattern[i] ; strip0 = evt_tree.lct_hs[i]
	if evt_tree.gen_tpid[0]==0: 
	  h_eta_numer_csc.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_csc.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==0: 
	  h_eta_numer_csc.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_csc.Fill(evt_tree.gen_pt[1])
	  break
	  
    for i in range(len(evt_tree.gem_pad_tpid)):
      if evt_tree.gem_pad_tpid[i]==0 and evt_tree.gem_pad_station[i]==1:
	if evt_tree.gen_tpid[0]==0: 
	  h_eta_numer_gempad.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_gempad.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==0: 
	  h_eta_numer_gempad.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_gempad.Fill(evt_tree.gen_pt[1])
	  break

    for i in range(len(evt_tree.gem_copad_tpid)):
      if evt_tree.gem_copad_tpid[i]==0 and evt_tree.gem_copad_station[i]==1:
	if evt_tree.gen_tpid[0]==0:
	  h_eta_numer_gemcopad.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_gemcopad.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==0: 
	  h_eta_numer_gemcopad.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_gemcopad.Fill(evt_tree.gen_pt[1])
	  break

    for i in range(len(evt_tree.gem_copad_tpid)):
      if evt_tree.gem_copad_chamber[i]==chamber0 and evt_tree.gem_copad_tpid[i]==0 and evt_tree.gem_copad_station[i]==1: 
	pad0 = evt_tree.gem_copad_pad[i]

    #print '------------'
    #Second muon (tpid ==1)
    for i in range(len(evt_tree.lct_tpid)):
      if evt_tree.lct_tpid[i]==1 and evt_tree.lct_station[i]==1 and evt_tree.lct_ring[i]==1: 
	chamber1 = evt_tree.lct_chamber[i] ; pattern1 = evt_tree.lct_pattern[i] ; strip1 = evt_tree.lct_hs[i]
	if evt_tree.gen_tpid[0]==1: 
	  h_eta_numer_csc.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_csc.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==1: 
	  h_eta_numer_csc.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_csc.Fill(evt_tree.gen_pt[1])
	  break

    for i in range(len(evt_tree.gem_pad_tpid)):
      if evt_tree.gem_pad_tpid[i]==1 and evt_tree.gem_pad_station[i]==1:
	if evt_tree.gen_tpid[0]==1: 
	  h_eta_numer_gempad.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_gempad.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==1: 
	  h_eta_numer_gempad.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_gempad.Fill(evt_tree.gen_pt[1])
	  break
    
    for i in range(len(evt_tree.gem_copad_tpid)):
      if evt_tree.gem_copad_tpid[i]==1 and evt_tree.gem_copad_station[i]==1:
	if evt_tree.gen_tpid[0]==1: 
	  h_eta_numer_gemcopad.Fill(abs(evt_tree.gen_eta[0]))
	  if abs(evt_tree.gen_eta[0])>1.6 and abs(evt_tree.gen_eta[0])<2.1: h_pt_numer_gemcopad.Fill(evt_tree.gen_pt[0])
	  break
	if evt_tree.gen_tpid[1]==1: 
	  h_eta_numer_gemcopad.Fill(abs(evt_tree.gen_eta[1]))
	  if abs(evt_tree.gen_eta[1])>1.6 and abs(evt_tree.gen_eta[1])<2.1: h_pt_numer_gemcopad.Fill(evt_tree.gen_pt[1])
	  break

    for i in range(len(evt_tree.gem_copad_tpid)):
      if evt_tree.gem_copad_chamber[i]==chamber1 and evt_tree.gem_copad_tpid[i]==1 and evt_tree.gem_copad_station[i]==1: 
	pad1 = evt_tree.gem_copad_pad[i]

    
  
  '''
  #dPad (before propagation and after)
  for i in range(len(evt_tree.lct_tpid)):
    if evt_tree.lct_pattern[i] == 8 and evt_tree.lct_station[i]==1 and evt_tree.lct_ring[i]==1:   
      if evt_tree.lct_tpid[i]==0: 
	chamber0 = evt_tree.lct_chamber[i] ; strip0 = evt_tree.lct_hs[i]
  
      if evt_tree.lct_tpid[i]==1: 
	chamber1 = evt_tree.lct_chamber[i] ; strip1 = evt_tree.lct_hs[i]

  for i in range(len(evt_tree.gem_copad_tpid)):
    if evt_tree.gem_copad_tpid[i]==0 and evt_tree.gem_copad_station[i]==1:
      pad0 = evt_tree.gem_copad_pad[i]
    
    if evt_tree.gem_copad_tpid[i]==1 and evt_tree.gem_copad_station[i]==1:
      pad1 = evt_tree.gem_copad_pad[i]

  if strip0!=-1 and pad0!=-1 and chamber0%2==0: h_dPad_before_even.Fill(pad0 - (strip0/0.67))
  if strip1!=-1 and pad1!=-1 and chamber1%2==0: h_dPad_before_even.Fill(pad1 - (strip1/0.67))
  if strip0!=-1 and pad0!=-1 and chamber0%2!=0: h_dPad_before_odd.Fill(pad0 - (strip0/0.67))
  if strip1!=-1 and pad1!=-1 and chamber1%2!=0: h_dPad_before_odd.Fill(pad1 - (strip1/0.67))

  #p10 even: min slope*dX = 0 ; max slope*dX = 6    odd: min = 0 ; max = 8
  if strip0 !=-1 and pad0!=-1 and chamber0%2==0: 
    a = (strip0 - 2)/0.67 ; b = (strip0 + 8)/0.67 ; c = (strip0/0.67)
    if abs(a - pad0)<abs(b - pad0) and abs(a - pad0)<abs(c - pad0): h_dPad_after_even.Fill(a - pad0)
    if abs(b - pad0)<abs(a - pad0) and abs(b - pad0)<abs(c - pad0): h_dPad_after_even.Fill(b - pad0)
    if abs(c - pad0)<abs(a - pad0) and abs(c - pad0)<abs(b - pad0): h_dPad_after_even.Fill(c - pad0)
 
  if strip1 !=-1 and pad1!=-1 and chamber0%2==0: 
    a = (strip1 - 2)/0.67 ; b = (strip1 + 8)/0.67 ; c = (strip1/0.67)
    if abs(a - pad1)<abs(b - pad1) and abs(a - pad1)<abs(c - pad1): h_dPad_after_even.Fill(a - pad1)
    if abs(b - pad1)<abs(a - pad1) and abs(b - pad1)<abs(c - pad1): h_dPad_after_even.Fill(b - pad1)
    if abs(c - pad1)<abs(a - pad1) and abs(c - pad1)<abs(b - pad1): h_dPad_after_even.Fill(c - pad1)

  if strip0 !=-1 and pad0!=-1 and chamber0%2!=0: 
    a = (strip0 - 1)/0.67 ; b = (strip0 + 12)/0.67 ; c = (strip0/0.67)
    if abs(a - pad0)<abs(b - pad0) and abs(a - pad0)<abs(c - pad0): h_dPad_after_odd.Fill(a - pad0)
    if abs(b - pad0)<abs(a - pad0) and abs(b - pad0)<abs(c - pad0): h_dPad_after_odd.Fill(b - pad0)
    if abs(c - pad0)<abs(a - pad0) and abs(c - pad0)<abs(b - pad0): h_dPad_after_odd.Fill(c - pad0)
 
  if strip1 !=-1 and pad1!=-1 and chamber0%2!=0: 
    a = (strip1 - 1)/0.67 ; b = (strip1 + 12)/0.67 ; c = (strip1/0.67)
    if abs(a - pad1)<abs(b - pad1) and abs(a - pad1)<abs(c - pad1): h_dPad_after_odd.Fill(a - pad1)
    if abs(b - pad1)<abs(a - pad1) and abs(b - pad1)<abs(c - pad1): h_dPad_after_odd.Fill(b - pad1)
    if abs(c - pad1)<abs(a - pad1) and abs(c - pad1)<abs(b - pad1): h_dPad_after_odd.Fill(c - pad1)
  '''
  #-------------------------
  '''
  #Even chambers
  if pattern0 == 10 and chamber0%2==0 and pad0!=-1:
    h_sDx_p_even.Fill((pad0*0.67) - strip0)

  if pattern1 == 10 and chamber1%2==0 and pad1!=-1:
    h_sDx_p_even.Fill((pad1*0.67) -strip1)

  #Odd chambers
  if pattern0 == 10 and chamber0%2!=0 and pad0!=-1: 
    h_sDx_p_odd.Fill((192-pad0)*0.67 - strip0)

  if pattern1 == 10 and chamber1%2!=0 and pad1!=-1: 
    h_sDx_p_odd.Fill((192-pad1)*0.67 - strip1)
  '''

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_sDx_even.Draw()
#h_sDx_even.SetTitle('slope*dX (pattern=10, even chambers)')
#c1.SaveAs('validation_september/h_sDx_p10_even.png')
#raw_input("Enter")

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_sDx_odd.Draw()
#h_sDx_odd.SetTitle('slope*dX (pattern=10, odd chambers)')
#c1.SaveAs('validation_september/h_sDx_p10_odd.png')
#raw_input("Enter")

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_dPad_before_even.Draw()
#h_dPad_before_even.SetTitle('Pad difference before propagation (pattern=10, even chambers)')
#c1.SaveAs('validation_september/h_dPad_p10_before_even.png')
#raw_input("Enter")

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_dPad_before_odd.Draw()
#h_dPad_before_odd.SetTitle('Pad difference before propagation (pattern=10, odd chambers)')
#c1.SaveAs('validation_september/h_dPad_p10_before_odd.png')
#raw_input("Enter")

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_dPad_after_even.Draw()
#h_dPad_after_even.SetTitle('Pad difference after propagation (pattern=10, even chambers)')
#c1.SaveAs('validation_september/h_dPad_p10_after_even.png')
#raw_input("Enter")

#c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
#h_dPad_after_odd.Draw()
#h_dPad_after_odd.SetTitle('Pad difference after propagation (pattern=10, odd chambers)')
#c1.SaveAs('validation_september/h_dPad_p10_after_odd.png')
#raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPad_before_even.Draw()
h_dPad_after_even.SetLineColor(kRed)
h_dPad_after_even.Draw("same")
h_dPad_before_even.SetTitle('Pad difference before/after propagation (pattern=8, even chambers)')
c1.SaveAs('validation_september/h_dPad_p8_even.png')
raw_input("Enter")

c1 = TCanvas( 'c1', '', 200, 10, 700, 500)
h_dPad_before_odd.Draw()
h_dPad_after_odd.SetLineColor(kRed)
h_dPad_after_odd.Draw("same")
h_dPad_before_odd.SetTitle('Pad difference before/after propagation (pattern=8, odd chambers)')
h_dPad_before_odd.SetMaximum(45)
c1.SaveAs('validation_september/h_dPad_p8_odd.png')
raw_input("Enter")

'''
#------------------------------------
#efficiency plots

#c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c57.SetGrid()
#eff = TEfficiency(h_pt_numer_csc, h_pt_denom)
#eff.Draw()
#eff.SetTitle('ME1/1 Trigger Efficiency vs p_{T}^{GEN} (1.6 < |#eta^{GEN}| < 2.1)')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#c57.SaveAs("validation_september/eff_pt_csc.png")
#raw_input("Enter")
#c57.Close()

#c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c57.SetGrid()
#eff = TEfficiency(h_pt_numer_gempad, h_pt_denom)
#eff.Draw()
#eff.SetTitle('GEM Pad Trigger Efficiency vs p_{T}^{GEN} (1.6 < |#eta^{GEN}| < 2.1)')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#c57.SaveAs("validation_september/eff_pt_pad.png")
#raw_input("Enter")
#c57.Close()

#c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
#c57.SetGrid()
#eff = TEfficiency(h_pt_numer_gemcopad, h_pt_denom)
#eff.Draw()
#eff.SetTitle('GEM Copad Trigger Efficiency vs p_{T}^{GEN} (1.6 < |#eta^{GEN}| < 2.1)')
#gPad.Update()
#graph = eff.GetPaintedGraph()
#graph.SetMinimum(0)
#graph.SetMaximum(1)
#c57.SaveAs("validation_september/eff_pt_copad.png")
#raw_input("Enter")
#c57.Close()

c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
c57.SetGrid()
eff = TEfficiency(h_eta_numer_csc, h_eta_denom)
eff.Draw()
eff.SetTitle('ME1/1 Trigger Efficiency vs |#eta^{GEN}|')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c57.SaveAs("validation_september/eff_eta_csc.png")
raw_input("Enter")
c57.Close()

c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
c57.SetGrid()
eff = TEfficiency(h_eta_numer_gempad, h_eta_denom)
eff.Draw()
eff.SetTitle('GEM Pad Trigger Efficiency vs |#eta^{GEN}|')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c57.SaveAs("validation_september/eff_eta_pad.png")
raw_input("Enter")
c57.Close()

c57 = TCanvas( 'c1', 'eff', 200, 10, 700, 500)
c57.SetGrid()
eff = TEfficiency(h_eta_numer_gemcopad, h_eta_denom)
eff.Draw()
eff.SetTitle('GEM Copad Trigger Efficiency vs |#eta^{GEN}|')
gPad.Update()
graph = eff.GetPaintedGraph()
graph.SetMinimum(0)
graph.SetMaximum(1)
c57.SaveAs("validation_september/eff_eta_copad.png")
raw_input("Enter")
c57.Close()

'''