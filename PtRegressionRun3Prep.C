//////////////////////////////////////////////////////////////////
///   pT Regression with Run-3 MC for 2022 EMTF pT assignment  ///
///                   Sven Dildick                             ///
///  Adapted from PtRegression_Apr_2017.C                      ///
//////////////////////////////////////////////////////////////////
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>
#include <list>

#include "TChain.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TObjString.h"
#include "TSystem.h"
#include "TROOT.h"

#include "TMVA/Tools.h"
#include "TMVA/Factory.h"
#include "TMVA/DataLoader.h"
#include "TMVA/TMVARegGui.h"
#include "TMVA/MethodBase.h"

// Extra tools
#include "interface/MVA_helper.h"
#include "src/TrackBuilder.cc"
#include "src/PtLutVarCalc.cc"

// Configuration settings
#include "configs/PtRegression2018/Standard.h" // Constants
#include "configs/PtRegression2018/General.h"  // Settings for all modes
#include "configs/PtRegression2018/User.h"     // User specific setting
#include "configs/PtRegression2018/Modes.h"    // Mode specific settign

//=====================================================
//Make sure it's up-to-date
//Also Ntuple format/index etc changed b/t 2017 and 2018
//Possibly cause error
//=====================================================
#include "configs/PtRegression2018/Read_FlatNtuple.h"

//////////////////////////////////
///  Main executable function  ///
//////////////////////////////////

using namespace TMVA;

void PtRegressionRun3Prep(TString user = "",
                          TString myMethodList = "",
                          unsigned emtfMode = 15,
                          float minPt = 1.,
                          float maxPt = 1000.,
                          float minPtTrain = 1.,
                          float maxPtTrain = 256.,
                          float minEta = 1.25,
                          float maxEta = 2.4,
                          unsigned long trainVarsSelection = 0,
                          unsigned long trainVarsSize = 0,
                          bool isRun2 = true,
                          bool useOneQuartPrecision = false,
                          bool useOneEighthPrecision = false,
                          bool useBitCompression = false,
                          int nEvents = -1,
                          bool verbose = false) {

  // Expert options
  // Run-2 overrides all options
  if (isRun2) {
    useOneQuartPrecision = false;
    useOneEighthPrecision = false;
  }
  // check if 1/4 is on
  if (useOneEighthPrecision)
    useOneQuartPrecision = true;

  // FIXME, check if the useGEM bit is set
  bool useGEM = false;
  std::cout << "Running PtRegressionRun3Prep with options:\n"
            << " - emtfMode: " << emtfMode << "\n"
            << " - minPt: " << minPt << "\n"
            << " - maxPt: " << maxPt << "\n"
            << " - minPtTrain: " << minPtTrain << "\n"
            << " - maxPtTrain: " << maxPtTrain << "\n"
            << " - minEta: " << minEta << "\n"
            << " - maxEta: " << maxEta << "\n"
            << " - trainVarsSelection: " << trainVarsSelection << "\n"
            << " - isRun2: " << isRun2 << "\n"
            << " - useOneQuartPrecision: " << useOneQuartPrecision << "\n"
            << " - useOneEighthPrecision: " << useOneEighthPrecision << "\n"
            << " - useGEM: " << useGEM << "\n"
            << " - useBitCompression: " << useBitCompression << "\n"
            << std::endl;

  // This loads the library
  TMVA::Tools::Instance();

  // Default MVA methods to be trained + tested
  std::map<std::string,int> Use;

  /////////////////////////
  ///  USER choose MVA  ///
  /////////////////////////
  //=================================
  // Neural Network
  Use["MLP"]             = 0;

  // Support Vector Machine
  Use["SVM"]             = 0;

  // Boosted Decision Trees
  Use["BDTG_AWB"]                = 0;
  Use["BDTG_AWB_Hub"]            = 0;
  Use["BDTG_AWB_Sq"]             = 1;
  //==================================

  std::cout << std::endl;
  std::cout << "==> Start PtRegressionRun3Prep" << std::endl;

  // Select methods (don't look at this code - not of interest)
  std::vector<TString> mlist;
  if (myMethodList != "") {
    for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

    mlist = gTools().SplitString( myMethodList, ',' );
    for (UInt_t i=0; i<mlist.size(); i++) {
      std::string regMethod(mlist[i]);

      if (Use.find(regMethod) == Use.end()) {
        std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
        for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
        std::cout << std::endl;
        return;
      }
      Use[regMethod] = 1;
    }
  }

  //===================
  //Preparation phase
  //===================
  // Configure settings for this mode and user
  PtRegression2018_cfg::ConfigureMode( emtfMode );
  PtRegression2018_cfg::ConfigureUser( user );

  // Create a new root output file
  TString out_file_str;
  TString bit_str = (useBitCompression ? "bitCompr" : "noBitCompr");

  out_file_str.Form( "%s/%s_MODE_%d_%s.root",
                     OUT_DIR_NAME.Data(), OUT_FILE_NAME.Data(),
                     emtfMode, bit_str.Data());

  TFile* out_file = TFile::Open( out_file_str, "RECREATE" );

  // Initialize empty file to access each file in the list
  TFile *file_tmp(0);

  // List of input files
  std::vector<TString> SM_in_file_names;//SingleMu
  std::vector<TString> ZB_in_file_names;//Zerobias
  TString SM_file_name;
  TString ZB_file_name;

  for (int i = 0; i < SingleMu_files.size(); i++) {
    SM_file_name.Form( "%s%s", EOS_DIR_NAME.Data(), SingleMu_files[i].Data() );
    std::cout << "Adding file " << SM_file_name.Data() << std::endl;
    SM_in_file_names.push_back(SM_file_name.Data());
  }
  for (int i = 0; i < USEZerobias; i++) {
    ZB_file_name.Form( "%s/%s/%s", EOS_DIR_NAME.Data(), in_dir.Data(), ZeroBias_files[i].Data() );
    std::cout << "Adding file " << ZB_file_name.Data() << std::endl;
    ZB_in_file_names.push_back(ZB_file_name.Data());
  }

  // Open all input files
  for (unsigned i = 0; i < SM_in_file_names.size(); i++) {
    if ( !gSystem->AccessPathName(SM_in_file_names.at(i)) )
      file_tmp = TFile::Open( SM_in_file_names.at(i) ); // Check if file exists
    if (!file_tmp) {
      std::cout << "ERROR: could not open data file " << SM_in_file_names.at(i) << std::endl;
      return;
    }
  }

  for (unsigned i = 0; i < ZB_in_file_names.size(); i++) {
    if ( !gSystem->AccessPathName(ZB_in_file_names.at(i)) )
      file_tmp = TFile::Open( ZB_in_file_names.at(i) ); // Check if file exists
    if (!file_tmp) {
      std::cout << "ERROR: could not open data file " << ZB_in_file_names.at(i) << std::endl;
      return;
    }
  }

  // Add tree from the input files to the TChain
  std::vector<TChain*> in_chains;
  TString treeString = "FlatNtupleMC/tree";
  if (isRun2) {
    treeString = "FlatNtupleMCRun2/tree";
  }

  std::cout << treeString << std::endl;

  TChain *SM_in_chain = new TChain(treeString);
  TChain *ZB_in_chain = new TChain(treeString);
  for (int i = 0; i < SM_in_file_names.size(); i++) {
    SM_in_chain->Add( SM_in_file_names.at(i) );
  }
  for (int i = 0; i < ZB_in_file_names.size(); i++) {
    ZB_in_chain->Add( ZB_in_file_names.at(i) );
  }


  std::cout << "SM_in_chain entries " << SM_in_chain->GetEntries() << std::endl;
  std::cout << "ZB_in_chain entries " << ZB_in_chain->GetEntries() << std::endl;
  InitializeMaps();
  SetBranchAddresses(SM_in_chain);
  SetBranchAddresses(ZB_in_chain);
  in_chains.push_back(SM_in_chain);
  in_chains.push_back(ZB_in_chain);


  //////////////////////////////////////////////////////////////////////////
  ///  Factories: Use different sets of variables, target, weights, etc. ///
  //////////////////////////////////////////////////////////////////////////
  TString fact_set = "!V:!Silent:Color:DrawProgressBar:AnalysisType=Regression";
  std::vector<TString> var_names; // Holds names of variables for a given factory and permutation
  std::vector<Double_t> var_vals; // Holds values of variables for a given factory and permutation
  TMVA::Factory* nullF = new TMVA::Factory("NULL", out_file, fact_set); // Placeholder factory
  TMVA::DataLoader* nullL = new TMVA::DataLoader("NULL");// Placeholder loader

  // Tuple is defined by the factory and dataloader,  followed by a name,
  // var name and value vectors, and hex bit masks for input variables.
  // Each hex bit represents four variables, e.g. 0x1 would select only the 1st variable,
  // 0xf the 1st 4, 0xff the 1st 8, 0xa the 2nd and 4th, 0xf1 the 1st and 5th-8th, etc.
  std::vector< std::tuple<TMVA::Factory*, TMVA::DataLoader*, TString, std::vector<TString>, std::vector<Double_t>, unsigned long>  > factories;

  for (unsigned iTarg = 0; iTarg < TARG_VARS.size(); iTarg++) {
    for (unsigned iWgt = 0; iWgt < EVT_WGTS.size(); iWgt++) {

      TString factName;  // "Targ" and "Wgt" components not arbitrary - correspond to specific options later on
      factName.Form( "f_MODE_%d_%sTarg_%sWgt_%s",
                     emtfMode, TARG_VARS.at(iTarg).Data(), EVT_WGTS.at(iWgt).Data(),
                     bit_str.Data());

      // the selection is now done in the Python configuration, not here!
      factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, trainVarsSelection) );
    }
  }

  // Initialize factories and dataloaders
  for (unsigned iFact = 0; iFact < factories.size(); iFact++) {
    std::get<0>(factories.at(iFact)) = new TMVA::Factory( std::get<2>(factories.at(iFact)), out_file, fact_set );
    std::get<1>(factories.at(iFact)) = new TMVA::DataLoader( std::get<2>(factories.at(iFact)) );
  }

  // Defined in interface/MVA_helper.h
  std::vector<MVA_var> in_vars;   // All input variables
  std::vector<MVA_var> targ_vars; // All target variables (should only define 1, unless using MLP)
  std::vector<MVA_var> spec_vars; // All spectator variables
  std::vector<MVA_var> all_vars;  // All variables

  /////////////////////////
  ///  Input variables  ///
  /////////////////////////

  /// this block needs to match exactly the "allowedTrainingVars" block!!!

  // block 1
  in_vars.push_back( MVA_var( "theta",     "Track #theta",          "int", 'I', -88 ) ); // 0x0000 0001
  in_vars.push_back( MVA_var( "St1_ring2", "St 1 hit in ring 2",    "int", 'I', -88 ) ); // 0x0000 0002
  in_vars.push_back( MVA_var( "dPhi_12",   "#phi(2) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0004
  in_vars.push_back( MVA_var( "dPhi_23",   "#phi(3) - #phi(2)",     "int", 'I', -88 ) ); // 0x0000 0008

  // block 2
  in_vars.push_back( MVA_var( "dPhi_34",   "#phi(4) - #phi(3)",     "int", 'I', -88 ) ); // 0x0000 0010
  in_vars.push_back( MVA_var( "dPhi_13",   "#phi(3) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0020
  in_vars.push_back( MVA_var( "dPhi_14",   "#phi(4) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0040
  in_vars.push_back( MVA_var( "dPhi_24",   "#phi(4) - #phi(2)",     "int", 'I', -88 ) ); // 0x0000 0080

  // block 3
  in_vars.push_back( MVA_var( "FR_1",      "St 1 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0100
  in_vars.push_back( MVA_var( "FR_2",      "St 2 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0200
  in_vars.push_back( MVA_var( "FR_3",      "St 3 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0400
  in_vars.push_back( MVA_var( "FR_4",      "St 4 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0800

  // block 4
  in_vars.push_back( MVA_var( "bend_1",    "St 1 LCT bending",      "int", 'I', -88 ) ); // 0x0000 1000
  in_vars.push_back( MVA_var( "bend_2",    "St 2 LCT bending",      "int", 'I', -88 ) ); // 0x0000 2000
  in_vars.push_back( MVA_var( "bend_3",    "St 3 LCT bending",      "int", 'I', -88 ) ); // 0x0000 4000
  in_vars.push_back( MVA_var( "bend_4",    "St 4 LCT bending",      "int", 'I', -88 ) ); // 0x0000 8000

  // block 5
  in_vars.push_back( MVA_var( "dPhiSum4",  "#Sigmad#phi (6)",       "int", 'I', -88 ) ); // 0x0001 0000
  in_vars.push_back( MVA_var( "dPhiSum4A", "#Sigma|d#phi| (6)",     "int", 'I', -88 ) ); // 0x0002 0000
  in_vars.push_back( MVA_var( "dPhiSum3",  "#Sigmad#phi (3)",       "int", 'I', -88 ) ); // 0x0004 0000
  in_vars.push_back( MVA_var( "dPhiSum3A", "#Sigma|d#phi| (3)",     "int", 'I', -88 ) ); // 0x0008 0000

  // block 6
  in_vars.push_back( MVA_var( "outStPhi",  "#phi outlier St",       "int", 'I', -88 ) ); // 0x0010 0000
  in_vars.push_back( MVA_var( "filler",    "Filler",                "int", 'I', -88 ) ); // 0x0020 0000
  in_vars.push_back( MVA_var( "dTh_12",    "#theta(2) - #theta(1)", "int", 'I', -88 ) ); // 0x0040 0000
  in_vars.push_back( MVA_var( "dTh_23",    "#theta(3) - #theta(2)", "int", 'I', -88 ) ); // 0x0080 0000

  // block 7
  in_vars.push_back( MVA_var( "dTh_34",    "#theta(4) - #theta(3)", "int", 'I', -88 ) ); // 0x0100 0000
  in_vars.push_back( MVA_var( "dTh_13",    "#theta(3) - #theta(1)", "int", 'I', -88 ) ); // 0x0200 0000
  in_vars.push_back( MVA_var( "dTh_14",    "#theta(4) - #theta(1)", "int", 'I', -88 ) ); // 0x0400 0000
  in_vars.push_back( MVA_var( "dTh_24",    "#theta(4) - #theta(2)", "int", 'I', -88 ) ); // 0x0800 0000

  // block 8
  in_vars.push_back( MVA_var( "RPC_1",   "St 1 hit is RPC",       "int", 'I', -88 ) ); // 0x1000 0000
  in_vars.push_back( MVA_var( "RPC_2",   "St 2 hit is RPC",       "int", 'I', -88 ) ); // 0x2000 0000
  in_vars.push_back( MVA_var( "RPC_3",   "St 3 hit is RPC",       "int", 'I', -88 ) ); // 0x4000 0000
  in_vars.push_back( MVA_var( "RPC_4",   "St 4 hit is RPC",       "int", 'I', -88 ) ); // 0x8000 0000

  // block 9
  in_vars.push_back( MVA_var( "slope_1",    "St 1 LCT slope",      "int", 'I', -88 ) ); // 0x0000 1000
  in_vars.push_back( MVA_var( "slope_2",    "St 2 LCT slope",      "int", 'I', -88 ) ); // 0x0000 2000
  in_vars.push_back( MVA_var( "slope_3",    "St 3 LCT slope",      "int", 'I', -88 ) ); // 0x0000 4000
  in_vars.push_back( MVA_var( "slope_4",    "St 4 LCT slope",      "int", 'I', -88 ) ); // 0x0000 8000

  // block 10
  in_vars.push_back( MVA_var( "dSlope_12",    "slope(2) - slope(1)", "int", 'I', -88 ) ); // 0x0040 0000
  in_vars.push_back( MVA_var( "dSlope_23",    "slope(3) - slope(2)", "int", 'I', -88 ) ); // 0x0080 0000
  in_vars.push_back( MVA_var( "dSlope_34",    "slope(4) - slope(3)", "int", 'I', -88 ) ); // 0x0100 0000
  in_vars.push_back( MVA_var( "dSlope_13",    "slope(3) - slope(1)", "int", 'I', -88 ) ); // 0x0200 0000

  // block 11
  in_vars.push_back( MVA_var( "dSlope_14",    "slope(4) - slope(1)", "int", 'I', -88 ) ); // 0x0400 0000
  in_vars.push_back( MVA_var( "dSlope_24",    "slope(4) - slope(2)", "int", 'I', -88 ) ); // 0x0800 0000
  in_vars.push_back( MVA_var( "dPhi_GE11_ME11", "#phi(GE11) - #phi(ME11)", "", 'I', -88 ) ); // 0x1 0000 0000
  in_vars.push_back( MVA_var( "GEM_1",   "St 1 hit is GEM",       "int", 'I', -88 ) ); // 0x1 0000 0000

  // block 12
  in_vars.push_back( MVA_var( "dSlopeSum4",  "#SigmadSlope (6)",       "int", 'I', -88 ) ); // 0x0001 0000
  in_vars.push_back( MVA_var( "dSlopeSum4A", "#Sigma|dSlope| (6)",     "int", 'I', -88 ) ); // 0x0002 0000
  in_vars.push_back( MVA_var( "dSlopeSum3",  "#SigmadSlope (3)",       "int", 'I', -88 ) ); // 0x0001 0000
  in_vars.push_back( MVA_var( "dSlopeSum3A", "#Sigma|dSlope| (3)",     "int", 'I', -88 ) ); // 0x0002 0000

  // block 13
  in_vars.push_back( MVA_var( "outStSlope",  "slope outlier St",       "int", 'I', -88 ) ); // 0x0010 0000
  in_vars.push_back( MVA_var( "Ph1Slope1MinusPh2",  "Phi1 + Slope12 - Ph2",       "int", 'I', -88 ) ); // 0x0010 0000
  in_vars.push_back( MVA_var( "Ph2Slope2MinusPh3",  "Phi2 + Slope23 - Ph3",       "int", 'I', -88 ) ); // 0x0010 0000
  in_vars.push_back( MVA_var( "Ph3Slope3MinusPh4",  "Phi3 + Slope34 - Ph4",       "int", 'I', -88 ) ); // 0x0010 0000

  ////////////////////////////////////////////////////////////
  //  Target variable: true muon pT, or 1/pT, or log2(pT)  ///
  ////////////////////////////////////////////////////////////
  targ_vars.push_back( MVA_var( "GEN_pt_trg",      "GEN p_{T} for trigger",               "GeV",      'F', -99 ) );
  targ_vars.push_back( MVA_var( "inv_GEN_pt_trg",  "1 / GEN muon p_{T} for trigger",      "GeV^{-1}", 'F', -99 ) );
  targ_vars.push_back( MVA_var( "log2_GEN_pt_trg", "log_{2}(GEN muon p_{T} for trigger)", "GeV",      'F', -99 ) );
  targ_vars.push_back( MVA_var( "sqrt_GEN_pt_trg", "sqrt GEN muon p_{T} for trigger",     "GeV^{0.5}",'F', -99 ) );
  targ_vars.push_back( MVA_var( "GEN_charge_trg",  "Muon charge x dPhi sign for trigger", "",         'I', -99 ) );

  /////////////////////////////////////////////////////////////////////////////
  ///  Spectator variables: not used in training, but saved in output tree  ///
  /////////////////////////////////////////////////////////////////////////////
  spec_vars.push_back( MVA_var( "GEN_pt",        "GEN p_{T}",                 "GeV", 'F', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_pt",       "EMTF p_{T}",                "GeV", 'F', -77 ) );
  spec_vars.push_back( MVA_var( "GEN_eta",       "GEN #eta",                  "",    'F', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_eta",      "EMTF #eta",                 "",    'F', -77 ) );
  spec_vars.push_back( MVA_var( "TRK_eta",       "Track #eta",                "",    'F', -77 ) );
  spec_vars.push_back( MVA_var( "GEN_charge",    "GEN charge",                "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_charge",   "EMTF charge",               "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_mode",     "EMTF mode",                 "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_mode_CSC", "EMTF CSC-only mode",        "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "EMTF_mode_RPC", "EMTF RPC-only",             "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "TRK_mode",      "Track mode",                "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "TRK_mode_CSC",  "Track CSC-only mode",       "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "TRK_mode_RPC",  "Track RPC-only mode",       "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "dPhi_sign",     "#phi(B) - #phi(A) sign",    "",    'I', -77 ) );
  spec_vars.push_back( MVA_var( "evt_weight",    "Event weight for training", "",    'F', -77 ) );

  // extra spectator variables to inspect correlations
  //spec_vars.push_back( MVA_var( "slope_1",    "St 1 LCT slope",      "int", 'I', -77 ) ); // 0x0000 1000
  //spec_vars.push_back( MVA_var( "slope_2",    "St 2 LCT slope",      "int", 'I', -77 ) ); // 0x0000 2000
  //spec_vars.push_back( MVA_var( "slope_3",    "St 3 LCT slope",      "int", 'I', -77 ) ); // 0x0000 4000
  //spec_vars.push_back( MVA_var( "slope_4",    "St 4 LCT slope",      "int", 'I', -77 ) ); // 0x0000 8000

  spec_vars.push_back( MVA_var( "ph1",    "St 1 LCT phi",      "int", 'I', -77 ) ); // 0x0000 1000
  spec_vars.push_back( MVA_var( "ph2",    "St 2 LCT phi",      "int", 'I', -77 ) ); // 0x0000 2000
  spec_vars.push_back( MVA_var( "ph3",    "St 3 LCT phi",      "int", 'I', -77 ) ); // 0x0000 4000
  spec_vars.push_back( MVA_var( "ph4",    "St 4 LCT phi",      "int", 'I', -77 ) ); // 0x0000 8000


  assert( in_vars.size() > 0 );   // Need at least one input variable
  assert( targ_vars.size() > 0 ); // Need at least one target variable

  // Order is important: input variables first, then target, then specator
  all_vars.insert( all_vars.end(), in_vars.begin(), in_vars.end() );
  all_vars.insert( all_vars.end(), targ_vars.begin(), targ_vars.end() );

  if (SPEC_VARS) all_vars.insert( all_vars.end(), spec_vars.begin(), spec_vars.end() );

  // Fill each factory with the correct set of variables
  for (unsigned iFact = 0; iFact < factories.size(); iFact++) {
    std::cout << "\n*** Factory " << std::get<2>(factories.at(iFact)) << " variables ***" << std::endl;

    std::cout << std::endl << "*** Input ***" << std::endl;
    for (unsigned i = 0; i < in_vars.size(); i++) {
      // Hex bit mask for in_vars
      if ( 0x1 & (std::get<5>(factories.at(iFact)) >> i) ) {
        MVA_var v = in_vars.at(i);
        std::cout << v.name << std::endl;
        std::get<1>(factories.at(iFact))->AddVariable( v.name, v.descr, v.unit, v.type ); // Add var to dataloader
        std::get<3>(factories.at(iFact)).push_back( v.name );    // Add to vector of var names
        std::get<4>(factories.at(iFact)).push_back( v.def_val ); // Add to vector of var values
      }
    }

    TString targ_str = ""; // Save name of target variable
    std::cout << std::endl << "*** Target ***" << std::endl;
    for (unsigned i = 0; i < targ_vars.size(); i++) {
      MVA_var v = targ_vars.at(i);
      if ( (v.name == "GEN_pt_trg"      && std::get<2>(factories.at(iFact)).Contains("_ptTarg"))    ||
           (v.name == "inv_GEN_pt_trg"  && std::get<2>(factories.at(iFact)).Contains("_invPtTarg")) ||
           (v.name == "log2_GEN_pt_trg" && std::get<2>(factories.at(iFact)).Contains("_logPtTarg")) ||
           (v.name == "sqrt_GEN_pt_trg" && std::get<2>(factories.at(iFact)).Contains("_sqrtPtTarg")) ||
           (v.name == "GEN_charge_trg"  && std::get<2>(factories.at(iFact)).Contains("_chargeTarg")) ) {
        std::cout << v.name << std::endl;
        targ_str = v.name;
        std::get<1>(factories.at(iFact))->AddTarget( v.name, v.descr, v.unit, v.type );
        std::get<3>(factories.at(iFact)).push_back( v.name );
        std::get<4>(factories.at(iFact)).push_back( v.def_val );
      }
    }

    std::cout << std::endl << "*** Spectator ***" << std::endl;
    for (UInt_t i = 0; i < spec_vars.size(); i++) {
      MVA_var v = spec_vars.at(i);
      if (v.name == targ_str) continue; // Don't add target variable
      std::cout << v.name << std::endl;
      std::get<1>(factories.at(iFact))->AddSpectator( v.name, v.descr, v.unit, v.type );
      std::get<3>(factories.at(iFact)).push_back( v.name );
      std::get<4>(factories.at(iFact)).push_back( v.def_val );
    }
  } // End loop: for (UInt_t iFact = 0; iFact < factories.size(); iFact++)

  int nSMEvents = SM_in_chain->GetEntries();
  int nZBEvents = ZB_in_chain->GetEntries();
  std::cout << "\n******* About to loop over chains *******" << std::endl;
  std::cout << "\n in_chains size: "<< in_chains.size() << " N(SingleMu) = " << nSMEvents << " N(ZeroBias) = " << nZBEvents << std::endl;
  UInt_t NonZBEvt = 0;
  UInt_t ZBEvt = 0;
  UInt_t nTrain = 0;
  UInt_t nTest  = 0;
  Bool_t isZB = false;//tag per event
  Bool_t isTEST = false;//tag per event

  unsigned iEvent = 0;
  //=================================
  //Register events: loop over chains
  //=================================
  for (unsigned iCh = 0; iCh < in_chains.size(); iCh++) {
    TChain *in_chain = in_chains.at(iCh);

    std::cout << "******* About to enter the event loop for chain " << iCh+1 << " " << in_chain->GetEntries() << " *******" << std::endl;

    for (UInt_t jEvt = 0; jEvt < in_chain->GetEntries(); jEvt++) {

      if (iEvent > nEvents) break;
      iEvent++;
      if (jEvt%1000==0) std::cout << "******* About to loop on event " << jEvt << " *******" << std::endl;
      //!!! jEvt restarts from 0 in new chain

      //!!! iCh<1 important here: Protect against small MAX_TR setting
      //When iCh = 1, it start to load ZB events, the first break from MAX_TR shouldn't affect the following ZB loading process
      //Otherwise no ZB events will be loaded, cause trouble when calculating rate
      if (nTrain > MAX_TR && iCh<1) break;
      if (nTest > MAX_TE) break;

      //iCh=0 means SingleMu dataset,
      //need to modify in the future if have more types of samples added for training, such as Muonia, etc
      if (iCh<1) {
        isZB = false;
        isTEST = false;
        NonZBEvt += 1;
      }

      in_chain->GetEntry(jEvt);

      UInt_t nMuons = I("nGenMuons");//reco_* branches are true info reference
      UInt_t nHits  = I("nHits");//hit_* branches are unpacked hits
      UInt_t nTrks  = I("nTracks");//trk_* branches are EMTF tracks
      UInt_t nSegs  = I("nSegs");//csc segments number

      //===================
      //Loop over EMTF trks
      //===================
      for (UInt_t iTrk = 0; iTrk < nTrks; iTrk++) {
        double emtf_pt    = F("trk_pt",iTrk);
        double emtf_eta   = F("trk_eta",iTrk);
        double emtf_phi   = F("trk_phi",iTrk);
        int emtf_eta_int  = I("trk_eta_int", iTrk);
        int emtf_charge   = I("trk_charge", iTrk);
        int emtf_mode     = I("trk_mode", iTrk);
        int emtf_mode_CSC = I("trk_mode_CSC", iTrk);
        int emtf_mode_RPC = I("trk_mode_RPC", iTrk);
        int emtf_unique_match = I("trk_dR_match_unique", iTrk);
        int emtf_unique_iMu = 0;//I("trk_dR_match_iReco", iTrk);
        int emtf_dR_match_nReco = I("trk_dR_match_nReco", iTrk);
        int emtf_dR_match_nRecoSoft = I("trk_dR_match_nRecoSoft", iTrk);
        double mu_pt = 999.;//Default for muons in ZB
        double mu_eta = -99.;
        double mu_phi = -99.;
        int mu_charge = -99;
        int gmt_pt = 999;
        Bool_t mu_train = false;  // tag muon for training

        // index of emtf_unique_iMu is 0 or 1
        mu_train = true;
        mu_pt =  F("mu_pt", emtf_unique_iMu);
        mu_eta = F("mu_eta", emtf_unique_iMu);
        mu_phi = F("mu_phi", emtf_unique_iMu);
        mu_charge = I("mu_charge", emtf_unique_iMu);

        if(verbose) {
          std::cout << "True muon pt " << mu_pt << std::endl;
          std::cout << "True muon eta " << mu_eta << std::endl;
          std::cout << "True muon phi " << mu_phi << std::endl;
          std::cout << "True muon charge " << mu_charge << std::endl;
        }

        if(verbose) std::cout << "RECO kinematics ... "<< std::endl;

        //===============================
        //RECO mu kinematics requirements
        //===============================
        if ( !isZB && (mu_pt < minPt || mu_pt > maxPt) ) continue;
        if ( !isZB && (fabs( mu_eta ) < minEta || fabs( mu_eta ) > maxEta) ) continue;
        if ( mu_pt < minPtTrain || mu_pt > maxPtTrain || isTEST) mu_train = false;

        //==================
        //Require valid mode
        //==================
        if(verbose) std::cout << "Valid modes ... "<< std::endl;
        bool good_emtf_mode = false;

        for (UInt_t jMode = 0; jMode < EMTF_MODES.size(); jMode++) {
          if ( emtf_mode == EMTF_MODES.at(jMode) ) good_emtf_mode = true;
        }
        if (!good_emtf_mode) {
          emtf_mode = -99;
          continue;
        }
        if (emtf_mode < 0) {
          std::cout << "Rare case: EMTF mode < 0 "<< std::endl;
          continue;
        }

        //======================
        //Trk hits from stations
        //======================
        int i1GEM=-99; // separate index for GEM
        int i1CSC=-99; // separate index for CSC%
        int i2=-99;
        int i3=-99;
        int i4=-99;

        // added on 2019-11-05 per Andrew's suggestions
        if ( I("trk_nHits", iTrk) != VI("trk_iHit", iTrk).size() and false) {

          std::cout << "Checking number of Track hits " << std::endl;
          std::cout << ">>>trk_nHits " << I("trk_nHits", iTrk) << std::endl;
          std::cout << ">>>trk_iHit.size " << VI("trk_iHit", iTrk).size() << std::endl;
          std::cout << ">>>mode_RPC " << I("trk_mode_RPC", iTrk)  << std::endl;
          std::cout << ">>>mode_CSC " << I("trk_mode_CSC", iTrk)  << std::endl;

          continue;
        }

	//std::cout << "i1GEM before: " << i1GEM << std::endl;

        for (int jhit = 0; jhit < I("trk_nHits", iTrk); jhit++) {

          int iHit = I("trk_iHit", iTrk, jhit);  // Access the index of each hit in the emtf track

          // trk_nHits, VI("trk_iHit", iTrk).size(), trk_nRPC, and trk_mode_CSC

          if( iHit < nHits){//Avoid the case when iHit index larger than the total number of hits in the event, this happens sometimes
            if(       I("hit_station", iHit) == 1 && I("hit_isCSC",iHit)==1 ){ i1CSC = iHit; }
            else if(  I("hit_station", iHit) == 1 && I("hit_isGEM",iHit)==1 ){ i1GEM = iHit; }
            else if ( I("hit_station", iHit) == 2 && I("hit_isCSC",iHit)==1 ){ i2 = iHit; }
            else if ( I("hit_station", iHit) == 3 && I("hit_isCSC",iHit)==1 ){ i3 = iHit; }
            else if ( I("hit_station", iHit) == 4 && I("hit_isCSC",iHit)==1 ){ i4 = iHit; }
          }
        }//end loop over hits in selected emtf track

        //std::cout << "i1GEM after: " << i1GEM << std::endl;

        if(verbose) {
          std::cout << "index GE1/1: "<<i1GEM<< std::endl;
          std::cout << "index ME1: "<<i1CSC<< std::endl;
          std::cout << "index ME2: "<<i2<< std::endl;
          std::cout << "index ME3: "<<i3<< std::endl;
          std::cout << "index ME4: "<<i4<< std::endl;
        }

        //Assign built trk properties the same as emtf track
        int mode     = emtf_mode;
        int mode_CSC = emtf_mode_CSC;
        int mode_RPC = emtf_mode_RPC;
        if(verbose) std::cout << "mode: "<<mode<<" MODE: "<<emtfMode<< std::endl;
        if (mode != emtfMode) continue;
        if (mode != mode_CSC) {
          if(verbose) std::cout << "Not CSC-only track"<< std::endl;
          continue;
        }

        int ph1 = (i1CSC >= 0 ? I("hit_phi_int",i1CSC ) : -99);
        int ph1GEM = (i1GEM >= 0 ? I("hit_phi_int",i1GEM ) : -99);
        int ph2 = (i2 >= 0 ? I("hit_phi_int", i2 ) : -99);
        int ph3 = (i3 >= 0 ? I("hit_phi_int", i3 ) : -99);
        int ph4 = (i4 >= 0 ? I("hit_phi_int", i4 ) : -99);

        //if ( i1CSC>0 && i1GEM>0 ) { std::cout << "ph1 CSC: " << ph1 << ", ph1GEM: " << ph1GEM << std::endl; }
        //if ( i1CSC>0 && i1GEM>0 ) { std::cout << "ph1 CSC: " << ph1 << ", ph1GEM / 4.: " << ph1GEM/4. << std::endl; }
        //if ( i1CSC>0 && i1GEM>0 && (abs(ph1 - ph1GEM)>1000) ) { ph1GEM = ph1GEM - 3600; }
        //if ( i1CSC>0 && i1GEM>0 ) { std::cout << "dPh : " << ph1 - ph1GEM << std::endl; }

        //std::cout << "Before function: " << ph1GEM << std::endl;
        //ph1GEM = ph1GEMFix(ph1, ph1GEM);
        //std::cout << "After function: " << ph1GEM << std::endl;

        int th1 = (i1CSC >= 0 ? I("hit_theta_int",i1CSC ) : -99);
        int th1GEM = (i1GEM >= 0 ? I("hit_theta_int",i1GEM ) : -99);
        int th2 = (i2 >= 0 ? I("hit_theta_int", i2 ) : -99);
        int th3 = (i3 >= 0 ? I("hit_theta_int", i3 ) : -99);
        int th4 = (i4 >= 0 ? I("hit_theta_int", i4 ) : -99);

        int endcap1 = (i1CSC >= 0 ? I("hit_endcap",i1CSC ) : -99);
        int endcap2 = (i2 >= 0 ? I("hit_endcap", i2 ) : -99);
        int endcap3 = (i3 >= 0 ? I("hit_endcap", i3 ) : -99);
        int endcap4 = (i4 >= 0 ? I("hit_endcap", i4 ) : -99);

        int station1 = (i1CSC >= 0 ? I("hit_station",i1CSC ) : -99);
        int station2 = (i2 >= 0 ? I("hit_station", i2 ) : -99);
        int station3 = (i3 >= 0 ? I("hit_station", i3 ) : -99);
        int station4 = (i4 >= 0 ? I("hit_station", i4 ) : -99);

        int ring1 = (i1CSC >= 0 ? I("hit_ring",i1CSC ) : -99);
        int ring2 = (i2 >= 0 ? I("hit_ring",i2 ) : -99);
        int ring3 = (i3 >= 0 ? I("hit_ring",i3 ) : -99);
        int ring4 = (i4 >= 0 ? I("hit_ring",i4 ) : -99);

        int chamber1 = (i1CSC >= 0 ? I("hit_chamber",i1CSC ) : -99);
        int chamber2 = (i2 >= 0 ? I("hit_chamber",i2 ) : -99);
        int chamber3 = (i3 >= 0 ? I("hit_chamber",i3 ) : -99);
        int chamber4 = (i4 >= 0 ? I("hit_chamber",i4 ) : -99);

        // 4-bit value
        int strip1 = (i1CSC >= 0 ? I("hit_strip",i1CSC ) : -99);
        int strip2 = (i2 >= 0 ? I("hit_strip", i2 ) : -99);
        int strip3 = (i3 >= 0 ? I("hit_strip", i3 ) : -99);
        int strip4 = (i4 >= 0 ? I("hit_strip", i4 ) : -99);

        // if (endcap1 == 1 and station1 == 1 and ring1 == 1 and chamber1==1)
        //   std::cout << station1 << ring1 << chamber1 << " hit_strip1 " << strip1 << " hit_phi_int1 " << ph1 << std::endl;
        // std::cout << "hit_strip2 " << strip2 << " hit_phi_int2 " << ph2 << std::endl;
        // std::cout << "hit_strip3 " << strip3 << " hit_phi_int3 " << ph3 << std::endl;
        // std::cout << "hit_strip4 " << strip4 << " hit_phi_int4 " << ph4 << std::endl;

        // 4-bit value
        int pat1 = (i1CSC >= 0 ? I("hit_pattern",i1CSC ) : -99);
        int pat2 = (i2 >= 0 ? I("hit_pattern", i2 ) : -99);
        int pat3 = (i3 >= 0 ? I("hit_pattern", i3 ) : -99);
        int pat4 = (i4 >= 0 ? I("hit_pattern", i4 ) : -99);

        // 4-bit value
        int pat1_run3 = (i1CSC >= 0 ? I("hit_pattern_run3",i1CSC ) : -99);
        int pat2_run3 = (i2 >= 0 ? I("hit_pattern_run3", i2 ) : -99);
        int pat3_run3 = (i3 >= 0 ? I("hit_pattern_run3", i3 ) : -99);
        int pat4_run3 = (i4 >= 0 ? I("hit_pattern_run3", i4 ) : -99);

        // 4-bit value
        int slope1 = (i1CSC >= 0 ? I("hit_slope",i1CSC ) : -99);
        int slope2 = (i2 >= 0 ? I("hit_slope", i2 ) : -99);
        int slope3 = (i3 >= 0 ? I("hit_slope", i3 ) : -99);
        int slope4 = (i4 >= 0 ? I("hit_slope", i4 ) : -99);

        // 1-bit sign
        int bend1 = (i1CSC >= 0 ? I("hit_bend",i1CSC ) : -99);
        int bend2 = (i2 >= 0 ? I("hit_bend", i2 ) : -99);
        int bend3 = (i3 >= 0 ? I("hit_bend", i3 ) : -99);
        int bend4 = (i4 >= 0 ? I("hit_bend", i4 ) : -99);
        if(verbose) {
        std::cout << "hit_bend1 " << bend1  << std::endl;
        std::cout << "hit_bend2 " << bend2  << std::endl;
        std::cout << "hit_bend3 " << bend3 << std::endl;
        std::cout << "hit_bend4 " << bend4 << std::endl;
        }
        // CCLUT bit corrections
        int strip_quart_bit1 = (i1CSC >= 0 ? I("hit_strip_quart_bit",i1CSC ) : -99);
        int strip_quart_bit2 = (i2 >= 0 ? I("hit_strip_quart_bit", i2 ) : -99);
        int strip_quart_bit3 = (i3 >= 0 ? I("hit_strip_quart_bit", i3 ) : -99);
        int strip_quart_bit4 = (i4 >= 0 ? I("hit_strip_quart_bit", i4 ) : -99);

        int strip_eight_bit1 = (i1CSC >= 0 ? I("hit_strip_eight_bit",i1CSC ) : -99);
        int strip_eight_bit2 = (i2 >= 0 ? I("hit_strip_eight_bit", i2 ) : -99);
        int strip_eight_bit3 = (i3 >= 0 ? I("hit_strip_eight_bit", i3 ) : -99);
        int strip_eight_bit4 = (i4 >= 0 ? I("hit_strip_eight_bit", i4 ) : -99);

        int st1_ring2 = (i1CSC >= 0 ? ( I("hit_ring",i1CSC ) == 2 || I("hit_ring",i1CSC ) == 3 ) : 0);

        //===========
        //track info: need to use offline CSC segments as well?
        //===========
        double eta;
        double phi;
        int endcap;

        if      (i2 >= 0) { eta = F("hit_eta", i2 ); phi = F("hit_phi", i2 ); }
        else if (i3 >= 0) { eta = F("hit_eta", i3 ); phi = F("hit_phi", i3 ); }
        else if (i4 >= 0) { eta = F("hit_eta", i4 ); phi = F("hit_phi", i4 ); }
        else if (i1CSC >= 0) { eta = F("hit_eta",i1CSC ); phi = F("hit_phi",i1CSC ); }
        endcap = (eta > 0 ? +1 : -1);

        //if ( abs(F("hit_eta", i1CSC))>1.6 && abs(F("hit_eta", i1CSC))<2.1 ) { std::cout << "i1GEM: " << i1GEM << std::endl; }

        //This block of code adds a correction to the integer phi value based on the quarter and eight-strip position offset.
        if (ph1 != -99) CalcPhiRun3(ph1, ring1, strip_quart_bit1, strip_eight_bit1, 1, endcap,
                                    useOneQuartPrecision, useOneEighthPrecision);
        if (ph2 != -99) CalcPhiRun3(ph2, ring2, strip_quart_bit2, strip_eight_bit2, 2, endcap,
                                    useOneQuartPrecision, useOneEighthPrecision);
        if (ph3 != -99) CalcPhiRun3(ph3, ring3, strip_quart_bit3, strip_eight_bit3, 3, endcap,
                                    useOneQuartPrecision, useOneEighthPrecision);
        if (ph4 != -99) CalcPhiRun3(ph4, ring4, strip_quart_bit4, strip_eight_bit4, 4, endcap,
                                    useOneQuartPrecision, useOneEighthPrecision);


        //========================
        //Variables to go into BDT
        //========================
        int theta;
        int dPh12, dPh13, dPh14, dPh23, dPh24, dPh34, dPhSign;
        int dPhSum4, dPhSum4A, dPhSum3, dPhSum3A, outStPh;
        int dTh12, dTh13, dTh14, dTh23, dTh24, dTh34;
        int dSlope12, dSlope13, dSlope14, dSlope23, dSlope24, dSlope34;
        int dSlopeSum4, dSlopeSum4A, dSlopeSum3, dSlopeSum3A, outStSlope;
        int Ph1Slope12MinusPh2, Ph2Slope23MinusPh3, Ph3Slope34MinusPh4;
        int FR1, FR2, FR3, FR4;
        //uncommented on 19/1/2021 int bend1, bend2, bend3, bend4;
        int RPC1, RPC2, RPC3, RPC4;
        int dPhGE11ME11;
        int GE11;

        // Extra variables for FR computation
        int cham1, cham2, cham3, cham4;

        if (emtfMode == 0) {
          theta = emtf_eta_int;
          goto EMTF_ONLY;
        }

        // GEM does not enter the theta calculation
        theta = CalcTrackTheta( th1, th2, th3, th4, st1_ring2, mode, useBitCompression );

        CalcDeltaPhis(dPh12,dPh13,dPh14,dPh23,dPh24,dPh34,dPhSign,
                      dPhSum4,dPhSum4A,dPhSum3,dPhSum3A,outStPh,
                      ph1,  ph2,  ph3,  ph4,  mode, useBitCompression );

        // special case with GEMs
        if (useGEM) {
          CalcDeltaPhisGEM( dPh12, dPh13, dPh14, dPh23, dPh24, dPh34, dPhSign,
                            dPhSum4, dPhSum4A, dPhSum3, dPhSum3A, outStPh, dPhGE11ME11,
                            ph1, ph2, ph3, ph4, ph1GEM, mode, useBitCompression );
        }

        //Avoid too large dPhis due to neighbouring chamber effects.
        if ( abs(dPh12) > 1000 || abs(dPh13) > 1000 || abs(dPh14) > 1000 ||
             abs(dPh23) > 1000 || abs(dPh24) > 1000 || abs(dPh34) > 1000 ) continue;

        CalcDeltaThetas( dTh12, dTh13, dTh14, dTh23, dTh24, dTh34,
                         th1, th2, th3, th4, mode, useBitCompression );

        // In firmware, RPC 'FR' bit set according to FR of corresponding CSC chamber
        cham1 = (i1CSC >= 0 ? I("hit_chamber",i1CSC ) : -99);
        cham2 = (i2 >= 0 ? I("hit_chamber", i2 ) : -99);
        cham3 = (i3 >= 0 ? I("hit_chamber", i3 ) : -99);
        cham4 = (i4 >= 0 ? I("hit_chamber", i4 ) : -99);

        FR1 = (i1CSC >= 0 ? (cham1 % 2 == 0) : -99);  // Odd chambers are bolted to the iron,
        FR2 = (i2 >= 0 ? (cham2 % 2 == 0) : -99);  // which faces forwared in stations 1 & 2,
        FR3 = (i3 >= 0 ? (cham3 % 2 == 1) : -99);  // backwards in 3 & 4
        FR4 = (i4 >= 0 ? (cham4 % 2 == 1) : -99);
        if (ring1 == 3) FR1 = 0;                   // In ME1/3 chambers are non-overlapping

        // calculate bendings from CCLUT slope (Run-3)
        // this needs to be evaluated before the CalcBends
        // this function does not modify bendX
        if(verbose) {
          std::cout << "Before" << std::endl;
          std::cout << "hit_slope1 " << slope1  << std::endl;
          std::cout << "hit_slope2 " << slope2  << std::endl;
          std::cout << "hit_slope3 " << slope3 << std::endl;
          std::cout << "hit_slope4 " << slope4 << std::endl;
        }
        CalcSlopes(bend1, slope1, endcap, mode, useBitCompression, isRun2 );
        CalcSlopes(bend2, slope2, endcap, mode, useBitCompression, isRun2 );
        CalcSlopes(bend3, slope3, endcap, mode, useBitCompression, isRun2 );
        CalcSlopes(bend4, slope4, endcap, mode, useBitCompression, isRun2 );

        if(verbose) {
          std::cout << "After" << std::endl;
          std::cout << "hit_slope1 " << slope1  << std::endl;
          std::cout << "hit_slope2 " << slope2  << std::endl;
          std::cout << "hit_slope3 " << slope3 << std::endl;
          std::cout << "hit_slope4 " << slope4 << std::endl;
        }
        CalcDeltaSlopes(slope1, slope2, slope3, slope4,
                        dSlope12, dSlope13, dSlope14,
                        dSlope23, dSlope24, dSlope34,
                        dSlopeSum4, dSlopeSum4A,
                        dSlopeSum3, dSlopeSum3A,
                        outStSlope);

        if(verbose) {
          std::cout << "DSlope" << std::endl;
          std::cout << "dSlope12 " << dSlope12  << std::endl;
          std::cout << "dSlope13 " << dSlope13  << std::endl;
          std::cout << "dSlope14 " << dSlope14  << std::endl;
          std::cout << "dSlope23 " << dSlope23  << std::endl;
          std::cout << "dSlope24 " << dSlope24  << std::endl;
          std::cout << "dSlope34 " << dSlope34  << std::endl;
        }

        // CalcDeltaPhiSlope(dSlope1
        //                   );

        // if (endcap1 == 1 and station1 == 1 and ring1 == 1 and chamber1==1)
        //   std::cout << station1 << ring1 << chamber1 << " hit_strip1 " << strip1 << " hit_phi_int1 " << ph1 << std::endl;

        // calculate bendings from pattern numbers (Run-2, Run-3)
        // this function modifies bendX
        CalcBends(bend1, bend2, bend3, bend4,
		  slope1, slope2, slope3, slope4,
                  pat1, pat2, pat3, pat4,
                  pat1_run3, pat2_run3, pat3_run3, pat4_run3,
                  dPhSign, endcap, mode, BIT_COMP, isRun2 );

	//std::cout << "(Before assignment) RPC1: " << RPC1 << ", RPC2: " << RPC2 << ", RPC3: " << RPC3 << ", RPC4: " << RPC4 << std::endl;
        // Check for additional hits
        RPC1 = (i1CSC >= 0 ? ( I("hit_isRPC",i1CSC ) == 1 ? 1 : 0) : -99);
        RPC2 = (i2 >= 0 ? ( I("hit_isRPC", i2 ) == 1 ? 1 : 0) : -99);
        RPC3 = (i3 >= 0 ? ( I("hit_isRPC", i3 ) == 1 ? 1 : 0) : -99);
        RPC4 = (i4 >= 0 ? ( I("hit_isRPC", i4 ) == 1 ? 1 : 0) : -99);

	//std::cout << "(After assignment) RPC1: " << RPC1 << ", RPC2: " << RPC2 << ", RPC3: " << RPC3 << ", RPC4: " << RPC4 << std::endl;

        GE11 = (i1GEM >= 0 ? ( I("hit_isGEM",i1GEM ) == 1 ? 1 : 0) : -99);

        CalcRPCs( RPC1, RPC2, RPC3, RPC4, mode, st1_ring2, theta, useBitCompression );

      EMTF_ONLY: // Skip track building, just store EMTF info

        /////////////////////////////////////////////////////
        ///  Loop over factories and set variable values  ///
        /////////////////////////////////////////////////////
        for (UInt_t iFact = 0; iFact < factories.size(); iFact++) {

          // Set vars equal to default vector of variables for this factory
          var_names = std::get<3>(factories.at(iFact));
          var_vals = std::get<4>(factories.at(iFact));

          // Unweighted distribution: flat in eta and 1/pT
          Double_t evt_weight = 1.0;

          // Weight by 1/pT or (1/pT)^2 so overall distribution is (1/pT)^2 or (1/pT)^3
          if      ( std::get<2>(factories.at(iFact)).Contains("_Pt0p5Wgt") )
            evt_weight = pow(mu_pt,0.5);
          else if ( std::get<2>(factories.at(iFact)).Contains("_log2PtWgt") )
            evt_weight = log2(mu_pt + BIT);
          else if ( std::get<2>(factories.at(iFact)).Contains("_PtWgt") )
            evt_weight = mu_pt;
          else if ( std::get<2>(factories.at(iFact)).Contains("_PtSqWgt") )
            evt_weight = pow(mu_pt, 2);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPt0p5Wgt") )
            evt_weight = 1. / pow(mu_pt, 0.5);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invlog2PtWgt") )
            evt_weight = 1. / log2(mu_pt + BIT); //mu_pt+ BIT offset in case of zero weight
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPtWgt") )
            evt_weight = 1. / mu_pt;
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPt1p5Wgt") )
            evt_weight = 1. / pow(mu_pt, 1.5);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPtSqWgt") )
            evt_weight = 1. / pow(mu_pt, 2);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPt2p5Wgt") )
            evt_weight = 1. / pow(mu_pt, 2.5);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPtCubWgt") )
            evt_weight = 1. / pow(mu_pt, 3);
          else if ( std::get<2>(factories.at(iFact)).Contains("_invPtQuadWgt") )
            evt_weight = 1. / pow(mu_pt, 4);
          else
            assert( std::get<2>(factories.at(iFact)).Contains("_noWgt") );

          // De-weight tracks with one or more RPC hits
          evt_weight *= (1. / pow( 4, ((RPC1 == 1) + (RPC2 == 1) + (RPC3 == 1) + (RPC4 == 1)) ) );

          // Fill all variables
          for (UInt_t iVar = 0; iVar < var_names.size(); iVar++) {
            TString vName = var_names.at(iVar);

            /////////////////////////
            ///  Input variables  ///
            /////////////////////////
            if ( vName == "theta" ) var_vals.at(iVar) = theta;
            if ( vName == "St1_ring2" ) var_vals.at(iVar) = st1_ring2;
            if ( vName == "dPhi_12" ) var_vals.at(iVar) = dPh12;
            if ( vName == "dPhi_13" ) var_vals.at(iVar) = dPh13;

            if ( vName == "dPhi_14" ) var_vals.at(iVar) = dPh14;
            if ( vName == "dPhi_23" ) var_vals.at(iVar) = dPh23;
            if ( vName == "dPhi_24" ) var_vals.at(iVar) = dPh24;
            if ( vName == "dPhi_34" ) var_vals.at(iVar) = dPh34;

            if ( vName == "FR_1" ) var_vals.at(iVar) = FR1;
            if ( vName == "FR_2" ) var_vals.at(iVar) = FR2;
            if ( vName == "FR_3" ) var_vals.at(iVar) = FR3;
            if ( vName == "FR_4" ) var_vals.at(iVar) = FR4;

            if ( vName == "bend_1" ) var_vals.at(iVar) = bend1;
            if ( vName == "bend_2" ) var_vals.at(iVar) = bend2;
            if ( vName == "bend_3" ) var_vals.at(iVar) = bend3;
            if ( vName == "bend_4" ) var_vals.at(iVar) = bend4;

            if ( vName == "dPhiSum4" ) var_vals.at(iVar) = dPhSum4;
            if ( vName == "dPhiSum4A" ) var_vals.at(iVar) = dPhSum4A;
            if ( vName == "dPhiSum3" ) var_vals.at(iVar) = dPhSum3;
            if ( vName == "dPhiSum3A" ) var_vals.at(iVar) = dPhSum3A;
            if ( vName == "outStPhi" ) var_vals.at(iVar) = outStPh;

            if ( vName == "dTh_12" ) var_vals.at(iVar) = dTh12;
            if ( vName == "dTh_13" ) var_vals.at(iVar) = dTh13;
            if ( vName == "dTh_14" ) var_vals.at(iVar) = dTh14;
            if ( vName == "dTh_23" ) var_vals.at(iVar) = dTh23;
            if ( vName == "dTh_24" ) var_vals.at(iVar) = dTh24;
            if ( vName == "dTh_34" ) var_vals.at(iVar) = dTh34;

            if ( vName == "RPC_1" ) var_vals.at(iVar) = RPC1;
            if ( vName == "RPC_2" ) var_vals.at(iVar) = RPC2;
            if ( vName == "RPC_3" ) var_vals.at(iVar) = RPC3;
            if ( vName == "RPC_4" ) var_vals.at(iVar) = RPC4;

            if ( vName == "slope_1" ) var_vals.at(iVar) = slope1;
            if ( vName == "slope_2" ) var_vals.at(iVar) = slope2;
            if ( vName == "slope_3" ) var_vals.at(iVar) = slope3;
            if ( vName == "slope_4" ) var_vals.at(iVar) = slope4;

            if ( vName == "dSlope_12" ) var_vals.at(iVar) = dSlope12;
            if ( vName == "dSlope_13" ) var_vals.at(iVar) = dSlope13;
            if ( vName == "dSlope_14" ) var_vals.at(iVar) = dSlope14;
            if ( vName == "dSlope_23" ) var_vals.at(iVar) = dSlope23;

            if ( vName == "dSlope_24" ) var_vals.at(iVar) = dSlope24;
            if ( vName == "dSlope_34" ) var_vals.at(iVar) = dSlope34;
            if ( vName == "GEM_1" ) var_vals.at(iVar) = max(0, GE11);
            if ( vName == "dPhi_GE11_ME11" ) var_vals.at(iVar) = dPhGE11ME11;

            if ( vName == "dSlopeSum4" ) var_vals.at(iVar) = dSlopeSum4;
            if ( vName == "dSlopeSum4A" ) var_vals.at(iVar) = dSlopeSum4A;
            if ( vName == "dSlopeSum3" ) var_vals.at(iVar) = dSlopeSum3;
            if ( vName == "dSlopeSum3A" ) var_vals.at(iVar) = dSlopeSum3A;
            if ( vName == "outStSlope" ) var_vals.at(iVar) = outStSlope;

            //////////////////////////////
            ///  Target and variables  ///
            //////////////////////////////

            if ( vName == "GEN_pt_trg" ) var_vals.at(iVar) = fmin(mu_pt, PTMAX_TRG);
            if ( vName == "inv_GEN_pt_trg" ) var_vals.at(iVar) = 1. / fmin(mu_pt, PTMAX_TRG);
            if ( vName == "log2_GEN_pt_trg" ) var_vals.at(iVar) = log2(fmin(mu_pt, PTMAX_TRG));
            if ( vName == "sqrt_GEN_pt_trg" ) var_vals.at(iVar) = sqrt(fmin(mu_pt, PTMAX_TRG));
            if ( vName == "GEN_charge_trg" ) var_vals.at(iVar) = mu_charge * dPhSign;

            /////////////////////////////
            ///  Spectator variables  ///
            /////////////////////////////

            if ( vName == "GEN_pt" ) var_vals.at(iVar) = mu_pt;
            if ( vName == "EMTF_pt" ) var_vals.at(iVar) = emtf_pt;
            if ( vName == "inv_GEN_pt" ) var_vals.at(iVar) = 1. / mu_pt;
            if ( vName == "inv_EMTF_pt" ) var_vals.at(iVar) = 1. / emtf_pt;
            if ( vName == "log2_GEN_pt" ) var_vals.at(iVar) = log2(mu_pt);
            if ( vName == "log2_EMTF_pt" ) var_vals.at(iVar) = (emtf_pt > 0 ? log2(emtf_pt) : -99);

            if ( vName == "GEN_eta" ) var_vals.at(iVar) = mu_eta;
            if ( vName == "EMTF_eta" ) var_vals.at(iVar) = emtf_eta;
            if ( vName == "TRK_eta" ) var_vals.at(iVar) = eta;
            if ( vName == "GEN_phi" ) var_vals.at(iVar) = mu_phi;
            if ( vName == "EMTF_phi" ) var_vals.at(iVar) = emtf_phi;
            if ( vName == "TRK_phi" ) var_vals.at(iVar) = phi;
            if ( vName == "GEN_charge" ) var_vals.at(iVar) = mu_charge;
            if ( vName == "EMTF_charge" ) var_vals.at(iVar) = emtf_charge;

            if ( vName == "EMTF_mode" ) var_vals.at(iVar) = emtf_mode;
            if ( vName == "EMTF_mode_CSC" ) var_vals.at(iVar) = emtf_mode_CSC;
            if ( vName == "EMTF_mode_RPC" ) var_vals.at(iVar) = emtf_mode_RPC;
            if ( vName == "TRK_mode" ) var_vals.at(iVar) = mode;
            if ( vName == "TRK_mode_CSC" ) var_vals.at(iVar) = mode_CSC;
            if ( vName == "TRK_mode_RPC" ) var_vals.at(iVar) = mode_RPC;
            if ( vName == "dPhi_sign" ) var_vals.at(iVar) = dPhSign;
            if ( vName == "evt_weight" ) var_vals.at(iVar) = evt_weight;

            if ( vName == "ph1" ) var_vals.at(iVar) = ph1;
            if ( vName == "ph2" ) var_vals.at(iVar) = ph2;
            if ( vName == "ph3" ) var_vals.at(iVar) = ph3;
            if ( vName == "ph4" ) var_vals.at(iVar) = ph4;

          } // End loop: for (UInt_t iVar = 0; iVar < var_names.size(); iVar++)

          // Load values into event
          if ( (NonZBEvt % 2)==0 && mu_train && emtfMode > 0 ) {
            std::get<1>(factories.at(iFact))->AddTrainingEvent( "Regression", var_vals, evt_weight );
            if (iFact == 0) nTrain += 1;

            // std::cout << "Total events in training sample " << nTrain << std::endl;
          }
          else {
            std::get<1>(factories.at(iFact))->AddTestEvent( "Regression", var_vals, evt_weight );
            if (iFact == 0) nTest += 1;

            // std::cout << "Total events in testing sample " << nTest << std::endl;
          }
        } // End loop: for (UInt_t iFact = 0; iFact < factories.size(); iFact++)

      } // End loop: for emtf trks

    } // End loop: for jEvt

  } // End loop: for iCh

  std::cout << "******* Made it out of the event loop *******" << std::endl;

  string NTr;
  string NTe;

  ostringstream convertTr;
  convertTr << nTrain;
  NTr = convertTr.str();
  ostringstream convertTe;
  convertTe << nTest;
  NTe = convertTe.str();

  string numTrainStr = "nTrain_Regression="+NTr+":nTest_Regression="+NTe+":";
  std::cout << "Number of training events: " << NTr << endl << "Number of testing events : " << NTe << std::endl;

  // // global event weights per tree (see below for setting event-wise weights)
  // Double_t regWeight  = 1.0;

  for (UInt_t iFact = 0; iFact < factories.size(); iFact++) {

    TMVA::Factory* factX = std::get<0>(factories.at(iFact));
    TMVA::DataLoader* loadX = std::get<1>(factories.at(iFact));

    loadX->SetWeightExpression( 1.0 );

    // Set nTest_Regression to 0 to tell the DataLoader to use all remaining events in the trees after training for testing:
    loadX->PrepareTrainingAndTestTree( "", numTrainStr+"SplitMode=Random:NormMode=NumEvents:!V" );
    // loadX->PrepareTrainingAndTestTree( mycut, "nTrain_Regression=0:nTest_Regression=0:SplitMode=Random:NormMode=NumEvents:!V" );

    //==================
    // Book MVA methods
    //==================
    // Neural network (MLP)
    if (Use["MLP"])
      factX->BookMethod( loadX,  TMVA::Types::kMLP, "MLP", (string)
                         "!H:!V:VarTransform=Norm:NeuronType=tanh:NCycles=20000:HiddenLayers=N+20:"+
                         "TestRate=6:TrainingMethod=BFGS:Sampling=0.3:SamplingEpoch=0.8:"+
                         "ConvergenceImprove=1e-6:ConvergenceTests=15:!UseRegulator" );

    // Support Vector Machine
    if (Use["SVM"])
      factX->BookMethod( loadX,  TMVA::Types::kSVM, "SVM", "Gamma=0.25:Tol=0.001:VarTransform=Norm" );

    // Boosted Decision Trees
    // AWB settings - AbsoluteDeviation
    if (Use["BDTG_AWB"]) // Optimized settings
      factX->BookMethod( loadX, TMVA::Types::kBDT, "BDTG_AWB", (string)
                         "!H:!V:NTrees=400::BoostType=Grad:Shrinkage=0.1:nCuts=1000:MaxDepth=5:MinNodeSize=0.000001:"+
                         "RegressionLossFunctionBDTG=AbsoluteDeviation" );
    // AWB settings - Huber
    if (Use["BDTG_AWB_Hub"]) // Optimized settings
      factX->BookMethod( loadX, TMVA::Types::kBDT, "BDTG_AWB_Hub", (string)
                         "!H:!V:NTrees=400::BoostType=Grad:Shrinkage=0.1:nCuts=1000:MaxDepth=5:MinNodeSize=0.000001:"+
                         "RegressionLossFunctionBDTG=Huber" );
    // AWB settings - LeastSquares
    if (Use["BDTG_AWB_Sq"]) // Optimized settings
      factX->BookMethod( loadX, TMVA::Types::kBDT, "BDTG_AWB_Sq", (string)
                         "!H:!V:NTrees=400::BoostType=Grad:Shrinkage=0.1:nCuts=1000:MaxDepth=5:MinNodeSize=0.000001:"+
                         "RegressionLossFunctionBDTG=LeastSquares" );

    // Train MVAs using the set of training events
    factX->TrainAllMethods();

    // Evaluate all MVAs using the set of test events
    factX->TestAllMethods();

    // Evaluate and compare performance of all configured MVAs
    // Instead of "EvaluateAllMethods()", just write out the training and testing trees
    // Skip unnecessary evaluatioh histograms, which take time on large datasets
    //factX->EvaluateAllMethods();

    // Code gleaned from original "EvaluateAllMethods()" function in tmva/tmva/src/Factory.cxx - AWB 31.01.17
    if ( factX->fMethodsMap.empty() )
      std::cout << "factX->fMethodsMap is empty" << std::endl;

    std::map<TString, std::vector<IMethod*>*>::iterator itrMap;
    for (itrMap = factX->fMethodsMap.begin(); itrMap != factX->fMethodsMap.end(); itrMap++) {

      std::vector<IMethod*> *methods = itrMap->second;
      std::list<TString> datasets;
      Int_t nmeth_used[2] = {int(mlist.size()), 1};

      for (Int_t k = 0; k < 2; k++) {
        for (Int_t i = 0; i < nmeth_used[k]; i++) {
          MethodBase* theMethod = dynamic_cast<MethodBase*>((*methods)[i]);
          if (theMethod == 0) {
            std::cout << "For k = " << k << ", i = " << i << ", no valid method" << std::endl;
            continue;
          }
          TDirectory* RootBaseDir = (TDirectory*) out_file;
          RootBaseDir->cd( std::get<2>(factories.at(iFact)) );
          if ( std::find( datasets.begin(), datasets.end(), std::get<2>(factories.at(iFact)) ) == datasets.end() ) {
            theMethod->Data()->GetTree(Types::kTesting)->Write( "", TObject::kOverwrite );
            theMethod->Data()->GetTree(Types::kTraining)->Write( "", TObject::kOverwrite );
            datasets.push_back( std::get<2>(factories.at(iFact)) );
          }
        } // End loop: for (Int_t i = 0; i < nmeth_used[k]; i++)
      } // End loop: for (Int_t k = 0; k < 2; k++)
    } // End loop: for (itrMap = factX->fMethodsMap.begin(); itrMap != factX->fMethodsMap.end(); itrMap++)

    // --------------------------------------------------------------

  } // End loop: for (UInt_t iFact = 0; iFact < factories.size(); iFact++)

  // Save the output
  out_file->Close();

  std::cout << "==> Wrote root file: " << out_file->GetName() << std::endl;
  std::cout << "==> TMVARegression is done!" << std::endl;

  //delete factory;
  //delete dataloader;

  // Launch the GUI for the root macros
  if (!gROOT->IsBatch()) TMVA::TMVARegGui( out_file_str );
}
