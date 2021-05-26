## combination of tdr style and cms-lumi
import ROOT as rt

class CMSStyle():
  ## constructor
  def __init__():
    self.cmsText = "CMS"
    self.cmsTextFont   = 61
    self.writeExtraText = True
    self.extraText   = " Simulation Preliminary"
    self.extraTextFont = 52
    self.lumiTextSize     = 0.6
    self.lumiTextOffset   = 0.2
    self.cmsTextSize      = 0.75
    self.cmsTextOffset    = 0.1
    self.relPosX    = 0.045
    self.relPosY    = 0.035
    self.relExtraDY = 1.2
    self.extraOverCmsTextSize  = 0.76
    self.lumi_13TeV = "20.1 fb^{-1}"
    self.lumi_8TeV  = "19.7 fb^{-1}"
    self.lumi_7TeV  = "5.1 fb^{-1}"
    #lumi_sqrtS = "14 TeV, 200 PU"
    self.lumi_sqrtS = "14 TeV, 0 PU"
    self.drawLogo      = False
    self.iPeriod = 0
    self.iPosX = 0

    if (self.iPosX == 0):
      self.relPosX = 0.12

    self.outOfFrame = True
    if(self.iPosX/10 == 0 ):
      self.outOfFrame = True

    self.alignY_ = 3
    self.alignX_ = 2

    if( self.iPosX/10 == 0 ):
      self.alignX_ = 1
    if( self.iPosX == 0    ):
      self.alignY_ = 1
    if( self.iPosX/10 == 1 ):
      self.alignX_ = 1
    if( self.iPosX/10 == 2 ):
      self.alignX_ = 2
    if( self.iPosX/10 == 3 ):
      self.alignX_ = 3

    self.align_ = 10 * self.alignX_ + self.alignY_

    self.lumiText = ""
    if( iPeriod==1 ):
      self.lumiText += self.lumi_7TeV
      self.lumiText += " (7 TeV)"

    elif ( iPeriod==2 ):
      self.lumiText += self.lumi_8TeV
      self.lumiText += " (8 TeV)"

    elif( iPeriod==3 ):
      self.lumiText = self.lumi_8TeV
      self.lumiText += " (8 TeV)"
      self.lumiText += " + "
      self.lumiText += self.lumi_7TeV
      self.lumiText += " (7 TeV)"

    elif ( iPeriod==4 ):
      self.lumiText += self.lumi_13TeV
      self.lumiText += " (13 TeV)"

    elif ( iPeriod==7 ):
      if( outOfFrame ):
        self.lumiText += "#scale[0.85]{"

    self.lumiText += self.lumi_13TeV
    self.lumiText += " (13 TeV)"
    self.lumiText += " + "
    self.lumiText += self.lumi_8TeV
    self.lumiText += " (8 TeV)"
    self.lumiText += " + "
    self.lumiText += self.lumi_7TeV
    self.lumiText += " (7 TeV)"

    if( outOfFrame):
      self.lumiText += "}"

    elif ( iPeriod==12 ):
      self.lumiText += "8 TeV"

    elif ( iPeriod==0 ):
      self.lumiText += self.lumi_sqrtS

    self.extraTextSize = self.extraOverCmsTextSize * self.cmsTextSize


    tdrStyle =  rt.TStyle("tdrStyle","Style for P-TDR")

    #for the canvas:
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasColor(rt.kWhite)
    tdrStyle.SetCanvasDefH(600) #Height of canvas
    tdrStyle.SetCanvasDefW(600) #Width of canvas
    tdrStyle.SetCanvasDefX(0)   #POsition on screen
    tdrStyle.SetCanvasDefY(0)
    tdrStyle.SetPadBorderMode(0)
    #tdrStyle.SetPadBorderSize(Width_t size = 1)
    tdrStyle.SetPadColor(rt.kWhite)
    tdrStyle.SetPadGridX(False)
    tdrStyle.SetPadGridY(False)
    tdrStyle.SetGridColor(0)
    tdrStyle.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)
    #For the frame:
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)
    #For the histo:
    #tdrStyle.SetHistFillColor(1)
    #tdrStyle.SetHistFillStyle(0)
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)
    #tdrStyle.SetLegoInnerR(Float_t rad = 0.5)
    #tdrStyle.SetNumberContours(Int_t number = 20)
    tdrStyle.SetEndErrorSize(2)
    #tdrStyle.SetErrorMarker(20)
    #tdrStyle.SetErrorX(0.)
    tdrStyle.SetMarkerStyle(20)
    #For the fit/function:
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)
    #For the date:
    tdrStyle.SetOptDate(0)
    # tdrStyle.SetDateX(Float_t x = 0.01)
    # tdrStyle.SetDateY(Float_t y = 0.01)
    # For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
    tdrStyle.SetStatColor(rt.kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)
    # tdrStyle.SetStatStyle(Style_t style = 1001)
    # tdrStyle.SetStatX(Float_t x = 0)
    # tdrStyle.SetStatY(Float_t y = 0)
    # Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.13)
    tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.02)
    # For the Global title:
    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    # tdrStyle.SetTitleH(0) # Set the height of the title box
    # tdrStyle.SetTitleW(0) # Set the width of the title box
    # tdrStyle.SetTitleX(0) # Set the position of the title box
    # tdrStyle.SetTitleY(0.985) # Set the position of the title box
    # tdrStyle.SetTitleStyle(Style_t style = 1001)
    # tdrStyle.SetTitleBorderSize(2)
    # For the axis titles:
    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.06, "XYZ")
    # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
    # tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset
    # For the axis labels:
    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")
    # For the axis:
    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(True)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(510, "XYZ")
    tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(1)
    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)
    # Postscript options:
    tdrStyle.SetPaperSize(20.,20.)
    # tdrStyle.SetLineScalePS(Float_t scale = 3)
    # tdrStyle.SetLineStyleString(Int_t i, const char* text)
    # tdrStyle.SetHeaderPS(const char* header)
    # tdrStyle.SetTitlePS(const char* pstitle)
    # tdrStyle.SetBarOffset(Float_t baroff = 0.5)
    # tdrStyle.SetBarWidth(Float_t barwidth = 0.5)
    # tdrStyle.SetPaintTextFormat(const char* format = "g")
    # tdrStyle.SetPalette(Int_t ncolors = 0, Int_t* colors = 0)
    # tdrStyle.SetTimeOffset(Double_t toffset)
    # tdrStyle.SetHistMinimumZero(kTRUE)
    tdrStyle.SetHatchesLineWidth(5)
    tdrStyle.SetHatchesSpacing(0.05)
    tdrStyle.cd()


  def applyCmsStyle(pad):
    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    e = 0.025

    pad.cd()

    latex = rt.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(rt.kBlack)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(self.lumiTextSize*t)

    latex.DrawLatex(1-r,1-t+self.lumiTextOffset*t,self.lumiText)

    if( self.outOfFrame ):
      latex.SetTextFont(self.cmsTextFont)
      latex.SetTextAlign(11)
      latex.SetTextSize(self.cmsTextSize*t)
      latex.DrawLatex(l,1-t+self.lumiTextOffset*t,self.cmsText)

    pad.cd()

    posX_ = 0
    if( self.iPosX%10<=1 ):
      posX_ =   l + self.relPosX*(1-l-r)
    elif( self.iPosX%10==2 ):
      posX_ =  l + 0.5*(1-l-r)
    elif( self.iPosX%10==3 ):
      posX_ =  1-r - self.relPosX*(1-l-r)

    posY_ = 1-t - relPosY*(1-t-b)

    if( not self.outOfFrame ):
      latex.SetTextFont(self.cmsTextFont)
      latex.SetTextSize(self.cmsTextSize*t)
      latex.SetTextAlign(self.align_)
      latex.DrawLatex(posX_, posY_, self.cmsText)
      if( self.writeExtraText ) :
        latex.SetTextFont(self.extraTextFont)
        latex.SetTextAlign(self.align_)
        latex.SetTextSize(self.extraTextSize*t)
        latex.DrawLatex(posX_, posY_- self.relExtraDY * self.cmsTextSize*t,
                        self.extraText)
    elif( self.writeExtraText ):
      if( self.iPosX==0):
        posX_ =   l +  self.relPosX*(1-l-r)
        posY_ =   1-t+self.lumiTextOffset*t

      latex.SetTextFont(self.extraTextFont)
      latex.SetTextSize(self.extraTextSize*t)
      latex.SetTextAlign(self.align_)
      latex.DrawLatex(posX_, posY_, self.extraText)

    pad.Update()

  def tdrGrid( gridOn):
    tdrStyle.SetPadGridX(gridOn)
    tdrStyle.SetPadGridY(gridOn)

  #fixOverlay: Redraws the axis
  def fixOverlay():
    gPad.RedrawAxis()
