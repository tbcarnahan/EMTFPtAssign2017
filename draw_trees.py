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

## ================ Read input files ==============
dir1 = '/uscms/home/mdecaro/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/'
file_name = dir1+"EMTF_MC_NTuple_20201106.root"
print colored('Loading file: '+file_name, 'green')


## ============== Read in the tree ================
evt_tree = TChain('FlatNtupleMC/tree')
evt_tree.Add(file_name)


## ============== Plotting macro ==================
'''
#Print out the list of all branches in the TTree
for b in evt_tree.GetListOfBranches():
  print ("branch:",b.GetName())
'''


#If you want to draw a single branch, for example the true muon pT:
'''
c1 = TCanvas("c1")
evt_tree.Draw("mu_pt")
c1.SaveAs('plots/mu_pt.png')  #Save your plot into a folder named 'plots' (mkdir this folder first)
'''


#If you want to draw and save -every- branch in the tree:
#Note that this might not be a good idea if you want to apply selections to certain branches.
'''
for b in evt_tree.GetListOfBranches():
  c1 = TCanvas("c1")
  evt_tree.Draw(b.GetName())
  c1.SaveAs('plots/'+b.GetName()+'.png')
'''


'''
#You can apply simple selections to whatever you plot. The selection is the second argument in tree.Draw()
#Our muons go up to 1000 GeV, but let's try only plotting up to 100 GeV
c1 = TCanvas("c1")
evt_tree.Draw("mu_pt", "(mu_pt < 100)")
raw_input("Press Enter to continue")

#Or plot the distribution of eta for true muons less than 10 GeV
c1 = TCanvas("c1")
evt_tree.Draw("mu_eta", "(mu_pt < 10)")
raw_input("Press Enter to continue")

#Or the distribution of hit_eta for CSC hits in ME1/1
c1 = TCanvas("c1")
evt_tree.Draw("hit_eta", "(hit_isCSC==1 && hit_station==1 && hit_ring==1)")
raw_input("Press Enter to continue")
'''


'''
#If you don't like the default draw options (title, x-title, y-title,...)
#Here is a way to adjust them. There isn't a simple option to do this, but you can define a 'dummy' histogram over your canvas that has a different title or axes.
c1 = TCanvas("c1")
evt_tree.Draw("mu_pt")
htemp = gPad.GetPrimitive("htemp")
htemp.SetTitle("Generated muon p_{T}") #Plot title
htemp.GetXaxis().SetTitle("p_{T} (GeV)") #X-axis title, can do same for y-axis
gPad.Update()
raw_input("Press Enter to continue")
'''