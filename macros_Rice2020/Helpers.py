# -*- coding: utf-8 -*-
from ROOT import *
from ROOT import TStyle
import os
import math

def ANDtwo(cut1,cut2):
    """AND of two TCuts in PyROOT"""
    if cut1.GetTitle() == "":
        return cut2
    if cut2.GetTitle() == "":
        return cut1
    return TCut("(%s) && (%s)"%(cut1.GetTitle(),cut2.GetTitle()))


def ORtwo(cut1,cut2):
    """OR of two TCuts in PyROOT"""
    if cut1.GetTitle() == "":
        return cut2
    if cut2.GetTitle() == "":
        return cut1
    return TCut("(%s) || (%s)"%(cut1.GetTitle(),cut2.GetTitle()))


def AND(*arg):
    """AND of any number of TCuts in PyROOT"""
    length = len(arg)
    if length == 0:
        print "ERROR: invalid number of arguments"
        return
    if length == 1:
        return arg[0]
    if length==2:
        return ANDtwo(arg[0],arg[1])
    if length>2:
        result = arg[0]
        for i in range(1,len(arg)):
            result = ANDtwo(result,arg[i])
        return result


def OR(*arg):
    """OR of any number of TCuts in PyROOT"""
    length = len(arg)
    if length == 0:
        print "ERROR: invalid number of arguments"
        return
    if length == 1:
        return arg[0]
    if length==2:
        return ORtwo(arg[0],arg[1])
    if length>2:
        result = arg[0]
        for i in range(1,len(arg)):
            result = ORtwo(result,arg[i])
        return result

def newCanvas(TT=0.08, BB=0.12, LL=0.12, RR=0.04):
    H_ref = 600;
    W_ref = 800;
    H  = H_ref
    W = W_ref

    # references for T, B, L, R
    T = TT*H_ref
    B = BB*H_ref
    L = LL*W_ref
    R = RR*W_ref

    c = TCanvas("c","c",50,50,W,H)
    c.Clear()
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )

    SetOwnership(c, False)
    return c


#_______________________________________________________________________________
def drawLabel(title, x=0.17, y=0.35, font_size=0.):
    tex = TLatex(x, y,title)
    if font_size > 0.:
      tex.SetTextSize(font_size)
      tex.SetTextSize(0.05)
    tex.SetNDC()
    #      tex.Draw()
    SetOwnership(tex, False)
    return tex


#_______________________________________________________________________________
def drawEtaLabel(minEta, maxEta, x=0.17, y=0.35, font_size=0.):
    tex = TLatex(x, y,"%.2f < |#eta| < %.2f"%(minEta,maxEta))
    if font_size > 0.:
      tex.SetTextSize(font_size)
      tex.SetTextSize(0.05)
      tex.SetNDC()
      tex.Draw()
      return tex


#_______________________________________________________________________________
def drawPuLabel(pu, x=0.17, y=0.35, font_size=0.):
    tex = TLatex(x, y,"<PU> = %d"%(pu))
    if font_size > 0.:
      tex.SetTextSize(font_size)
      tex.SetTextSize(0.05)
      tex.SetNDC()
      tex.Draw()
      return tex


#_______________________________________________________________________________
def draw_eff(t,title, h_bins, to_draw, denom_cut, extra_num_cut,
             color = kBlue, marker_st = 20):
    """Make an efficiency plot"""

    ## total numerator selection cut
    num_cut = AND(denom_cut,extra_num_cut)

    t.Draw(to_draw + ">>num_" + h_bins, num_cut, "goff")
    num = TH1F(gDirectory.Get("num_").Clone("num_"))
    t.Draw(to_draw + ">>denom_" + h_bins, denom_cut, "goff")
    den = TH1F(gDirectory.Get("denom_").Clone("denom_"))

    useTEfficiency = True
    if useTEfficiency:
        eff = TEfficiency(num, den)
    else:
        eff = TGraphAsymmErrors(num, den)

    eff.SetTitle(title)
    eff.SetLineWidth(2)
    eff.SetLineColor(color)
    eff.SetMarkerStyle(marker_st)
    eff.SetMarkerColor(color)
    eff.SetMarkerSize(.5)
    return eff


#_______________________________________________________________________________
def draw_geff(t, title, h_bins, to_draw, den_cut, extra_num_cut,
              opt = "", color = kBlue, marker_st = 1, marker_sz = 1.):
    """Make an efficiency plot"""

    ## total numerator selection cut
    ## the extra brackets around the extra_num_cut are necessary !!
    num_cut = AND(den_cut,extra_num_cut)
    debug = False
    if debug:
        print "Denominator cut", den_cut
        print "Numerator cut", num_cut

    ## PyROOT works a little different than ROOT when you are plotting
    ## histograms directly from tree. Hence, this work-around
    nBins  = int(h_bins[1:-1].split(',')[0])
    minBin = float(h_bins[1:-1].split(',')[1])
    maxBin = float(h_bins[1:-1].split(',')[2])

    num = TH1F("num", "", nBins, minBin, maxBin)
    den = TH1F("den", "", nBins, minBin, maxBin)

    t.Draw(to_draw + ">>num", num_cut, "goff")
    t.Draw(to_draw + ">>den", den_cut, "goff")

    eff = TEfficiency(num, den)

    ## plotting options
    if not "same" in opt:
        num.Reset()
        num.GetYaxis().SetRangeUser(0.0,1.1)
        num.SetStats(0)
        num.SetTitle(title)
        num.Draw()

    eff.SetLineWidth(2)
    eff.SetLineColor(color)
    eff.Draw(opt + " same")
    eff.SetMarkerStyle(marker_st)
    eff.SetMarkerColor(color)
    eff.SetMarkerSize(marker_sz)

    SetOwnership(eff, False)
    return eff

#_______________________________________________________________________________
def draw_res(t, nBins, minBin, maxBin, to_draw, pt_cut):

    htemp = TH1F("htemp", "", nBins, minBin, maxBin)
    t.Draw(to_draw+">>htemp", pt_cut, "goff")

    return htemp

#_______________________________________________________________________________
def draw_multiple(res, title, drawOptions1D, lineColors, texLabel):

    for i in range(len(res)):	
	res[i].SetLineColor(lineColors[i])
	res[i].Scale(1./res[i].Integral(), "WIDTH")
	res[i].Draw("HIST"+drawOptions1D[i])

    for i in range(len(res)):
      tex = TLatex() ; tex.SetTextFont(22) ; tex.SetTextColor(lineColors[i]) ; tex.SetTextSize(0.033) ; tex.SetTextAlign(10)
      tex.DrawLatex( 3, 0.8-(i*0.1), texLabel[i]+" #mu = "+str(truncate(htemp.GetMean(),3))+", #sigma = "+str(truncate(htemp.GetRMS(),3)))
	

    res[0].SetTitle(title)
    return
    
	
#_______________________________________________________________________________
def checkDir(path):
    try: 
        os.mkdir(path)
    except OSError as error:
        "Could not make output directory."

#_______________________________________________________________________________
def truncate(number, digits):
  stepper = 10.0 ** digits
  return float(math.trunc(stepper * number) / stepper)

