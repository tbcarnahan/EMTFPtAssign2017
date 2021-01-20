## run quiet mode
import sys
sys.argv.append( '-b' )

import ROOT
ROOT.gROOT.SetBatch(1)

import ROOT
from ROOT import *
from Helpers import newCanvas, drawLabel
import tdrstyle
import CMS_lumi

iPeriod = 0

tdrstyle.setTDRStyle()
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
CMS_lumi.lumi_sqrtS = "14 TeV"

iPos = 0
if( iPos==0 ): CMS_lumi.relPosX = 0.12

training_version = 3

targetDirectory = "/uscms_data/d3/dildick/work/Rice_EMTF_Summer2019/CMSSW_10_6_1_patch2/src/Plots_PtResolution_BDT_SD_Run3Studies"

## training versions
# 1) No EMTF_pt as an input, no GEM-CSC bend angle input.
# 2) No EMTF_pt as an input, with GEM-CSC bend angle input.
# 3) With EMTF_pt and GEM-CSC bend angle input.

myFileName = [
    "../PtRegression2018_MODE_15_noBitCompr_noRPC_GEM_BDTTraining1.root",
    "../PtRegression2018_MODE_15_noBitCompr_noRPC_GEM_BDTTraining2.root",
    "../PtRegression2018_MODE_15_noBitCompr_noRPC_GEM_BDTTraining3.root"
]

myFile = ROOT.TFile(myFileName[training_version - 1])
myDirectory = myFile.Get("f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_GEM")
#myDirectory.Print()
myTree = myDirectory.Get("TestTree")
print myTree

gStyle.SetStatStyle(0)
gStyle.SetOptStat(0)

## log2 Pt
c = newCanvas(RR=0.16)
myTree.Draw("BDTG_AWB_Sq : log2(GEN_pt)>>h(100,1,7,100,1,7)","","COLZ")
h = TH2F(gDirectory.Get("h"))
h.SetTitle("CMS Simulation Preliminary")
h.GetXaxis().SetTitle("True Muon Log2(p_{T}^{GEN}) [Log2(GeV)]")
h.GetYaxis().SetTitle("Trained Muon Log2(p_{T}^{BDT}) [Log2(GeV)]")
h.GetYaxis().SetTitleOffset(0.9)
h.Draw("COLZ")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.SaveAs("Training%d/EMTF_BDT_Log2GenPt_vs_Log2BDTPt_Training%d.pdf"%(training_version, training_version))
c.SaveAs("Training%d/EMTF_BDT_Log2GenPt_vs_Log2BDTPt_Training%d.C"%(training_version, training_version))

## Pt with scaling
c = newCanvas(RR=0.16)
myTree.Draw("EMTF_pt/min(1.715, 1.2+0.015*EMTF_pt) : GEN_pt>>h(100,1,100,100,1,100)","( EMTF_pt < 150 )","COLZ")
h = TH2F(gDirectory.Get("h"))
h.SetTitle("CMS Simulation Preliminary")
h.GetXaxis().SetTitle("True Muon p_{T} [GeV]")
h.GetYaxis().SetTitle("EMTF p_{T} [GeV]")
h.GetYaxis().SetTitleOffset(0.9)
h.Draw("COLZ")
CMS_lumi.CMS_lumi(c, iPeriod, iPos)
c.SaveAs("Training%d/EMTF_BDT_GenPt_vs_EMTFPt_Training%d.pdf"%(training_version, training_version))
c.SaveAs("Training%d/EMTF_BDT_GenPt_vs_EMTFPt_Training%d.C"%(training_version, training_version))

gStyle.SetOptStat(0)

## Pt resolution
c = newCanvas(LL=0.16, RR=0.04)
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

myTree.Draw("BDTG_AWB_Sq - log2(GEN_pt)>>h(120,-1.5,1.5)","","hist")
h = TH1F(gDirectory.Get("h"))
h.SetTitle("CMS Simulation Preliminary")
h.GetXaxis().SetTitle("Muon Log2 p_{T} Resolution [Log2(GeV)]")
h.GetYaxis().SetTitle("A.U.")
h.GetYaxis().SetTitleOffset(1.4)
h.SetLineColor(kBlue)
h.SetLineWidth(2)
h.Draw("hist")
#myTree.Draw("log2(EMTF_pt/min(1.715, 1.2+0.015*EMTF_pt)) - log2(GEN_pt)>>hh(120,-1.5,1.5)","","same")
#hh = TH1F(gDirectory.Get("hh"))
#hh.SetLineColor(kRed)
#hh.SetLineWidth(2)
#hh.Draw("histsame")

leg = TLegend(0.45,0.2,.75,0.4, "", "brNDC")
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.05)
leg.AddEntry(h, "BDT","pl")
#leg.AddEntry(hh, "EMTF","pl")
leg.Draw("same")

label1 = drawLabel("#mu: %f"%(h.GetMean()), x=0.22, y=0.8, font_size=0.035)
label2 = drawLabel("#sigma: %f"%(h.GetStdDev()), x=0.22, y=0.85, font_size=0.035)
label1.SetTextColor(kBlue)
label2.SetTextColor(kBlue)
label1.Draw("same")
label2.Draw("same")

#label3 = drawLabel("#mu: %f"%(hh.GetMean()), y=0.7, x=0.22, font_size=0.035)
#label4 = drawLabel("#sigma: %f"%(hh.GetStdDev()), x=0.22, y=0.75, font_size=0.035)
#label3.SetTextColor(kRed)
#label4.SetTextColor(kRed)
#label3.Draw("same")
#label4.Draw("same")

c.SaveAs("Training%d/EMTF_Log2Pt_Resolution_Training%d.pdf"%(training_version, training_version))
c.SaveAs("Training%d/EMTF_Log2Pt_Resolution_Training%d.C"%(training_version, training_version))


## Pt resolution (low pT)
c = newCanvas(LL=0.16, RR=0.04)
CMS_lumi.CMS_lumi(c, iPeriod, iPos)

myTree.Draw("BDTG_AWB_Sq - log2(GEN_pt)>>h(120,-1.5,1.5)","( GEN_pt < 10 )","hist")
h = TH1F(gDirectory.Get("h"))
h.SetTitle("CMS Simulation Preliminary")
h.GetXaxis().SetTitle("Muon Log2 p_{T} Resolution [Log2(GeV)]")
h.GetYaxis().SetTitle("A.U.")
h.GetYaxis().SetTitleOffset(1.4)
h.SetLineColor(kBlue)
h.SetLineWidth(2)
h.Draw("hist")
#myTree.Draw("log2(EMTF_pt/min(1.715, 1.2+0.015*EMTF_pt)) - log2(GEN_pt)>>hh(120,-1.5,1.5)","( GEN_pt < 10 )","same")
#hh = TH1F(gDirectory.Get("hh"))
#hh.SetLineColor(kRed)
#hh.SetLineWidth(2)
#hh.Draw("histsame")

leg = TLegend(0.45,0.2,.75,0.4, "", "brNDC")
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.SetTextSize(0.05)
leg.AddEntry(h, "BDT","pl")
#leg.AddEntry(hh, "EMTF","pl")
leg.Draw("same")

label1 = drawLabel("#mu: %f"%(h.GetMean()), x=0.22, y=0.8, font_size=0.035)
label2 = drawLabel("#sigma: %f"%(h.GetStdDev()), x=0.22, y=0.85, font_size=0.035)
label1.SetTextColor(kBlue)
label2.SetTextColor(kBlue)
label1.Draw("same")
label2.Draw("same")

#label3 = drawLabel("#mu: %f"%(hh.GetMean()), y=0.7, x=0.22, font_size=0.035)
#label4 = drawLabel("#sigma: %f"%(hh.GetStdDev()), x=0.22, y=0.75, font_size=0.035)
#label3.SetTextColor(kRed)
#label4.SetTextColor(kRed)
#label3.Draw("same")
#label4.Draw("same")

c.SaveAs("Training%d/EMTF_Log2Pt_Resolution_GenPtLess10_Training%d.pdf"%(training_version, training_version))
c.SaveAs("Training%d/EMTF_Log2Pt_Resolution_GenPtLess10_Training%d.C"%(training_version, training_version))
