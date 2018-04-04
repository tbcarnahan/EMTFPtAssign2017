//////////////////////////////////////////////////////////////////
///  pT Regression with 2017 data for 2018 EMTF pT assignment  ///
///                  Wei Shi                                   ///
///  Adapted from PtRegression_Apr_2017.C                      ///        
//////////////////////////////////////////////////////////////////
#include <cstdlib>
#include <iostream>
#include <map>
#include <string>

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

void PtRegression2018 ( TString myMethodList = "" ) {

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
   Use["BDTG_AWB"]                = 1;
   Use["BDTG_AWB_Hub"]            = 0;
   Use["BDTG_AWB_Sq"]             = 0;
   //==================================
   bool verbose = false;//for debug

   std::cout << std::endl;
   std::cout << "==> Start PtRegression2018" << std::endl;

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
   PtRegression2018_cfg::ConfigureMode( MODE );
   PtRegression2018_cfg::ConfigureUser( USER );

   // Create a new root output file
   TString out_file_str;
   TString bit_str = (BIT_COMP ? "bitCompr" : "noBitCompr");
   TString RPC_str = (USE_RPC  ? "RPC"      : "noRPC");
	
   out_file_str.Form( "%s/%s_MODE_%d_%s_%s.root", 
		      OUT_DIR_NAME.Data(), OUT_FILE_NAME.Data(), 
		      MODE, bit_str.Data(), RPC_str.Data() );

   TFile* out_file = TFile::Open( out_file_str, "RECREATE" );

   // Initialize empty file to access each file in the list
   TFile *file_tmp(0);

   // List of input files
   std::vector<TString> SM_in_file_names;//SingleMu
   std::vector<TString> ZB_in_file_names;//Zerobias
   TString SM_file_name;
   TString ZB_file_name;

   for (int i = 0; i < USESingleMu; i++) {
	  SM_file_name.Form( "%s/%s/%s", EOS_DIR_NAME.Data(), in_dir.Data(), SingleMu_files[i].Data() );
  	  std::cout << "Adding file " << SM_file_name.Data() << std::endl;
          SM_in_file_names.push_back(SM_file_name.Data());
   }
   for (int i = 0; i < USEZerobias; i++) {
	  ZB_file_name.Form( "%s/%s/%s", EOS_DIR_NAME.Data(), in_dir.Data(), ZeroBias_files[i].Data() );
  	  std::cout << "Adding file " << ZB_file_name.Data() << std::endl;
          ZB_in_file_names.push_back(ZB_file_name.Data());
   }
  
   // Open all input files
   for (int i = 0; i < SM_in_file_names.size(); i++) {
     if ( !gSystem->AccessPathName(SM_in_file_names.at(i)) )
       file_tmp = TFile::Open( SM_in_file_names.at(i) ); // Check if file exists
     if (!file_tmp) {
       std::cout << "ERROR: could not open data file " << SM_in_file_names.at(i) << std::endl;
       return;
     }
   }

   for (int i = 0; i < ZB_in_file_names.size(); i++) {
     if ( !gSystem->AccessPathName(ZB_in_file_names.at(i)) )
       file_tmp = TFile::Open( ZB_in_file_names.at(i) ); // Check if file exists
     if (!file_tmp) {
       std::cout << "ERROR: could not open data file " << ZB_in_file_names.at(i) << std::endl;
       return;
     }
   }
	
   // Add tree from the input files to the TChain 
   std::vector<TChain*> in_chains;
   TChain *SM_in_chain = new TChain("FlatNtupleData/tree");
   TChain *ZB_in_chain = new TChain("FlatNtupleData/tree");
   for (int i = 0; i < SM_in_file_names.size(); i++) {
	   SM_in_chain->Add( SM_in_file_names.at(i) );
   }	
   for (int i = 0; i < ZB_in_file_names.size(); i++) {
	   ZB_in_chain->Add( ZB_in_file_names.at(i) );
   }
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
   std::vector< std::tuple<TMVA::Factory*, TMVA::DataLoader*, TString, std::vector<TString>, std::vector<Double_t>, int> > factories;

   for (int iTarg = 0; iTarg < TARG_VARS.size(); iTarg++) {
     for (int iWgt = 0; iWgt < EVT_WGTS.size(); iWgt++) {

       TString factName;  // "Targ" and "Wgt" components not arbitrary - correspond to specific options later on
       factName.Form( "f_MODE_%d_%sTarg_%sWgt_%s_%s", 
		      MODE, TARG_VARS.at(iTarg).Data(), EVT_WGTS.at(iWgt).Data(), 
		      bit_str.Data(), RPC_str.Data() );

       // 4-station tracks
       if        (MODE == 15) {
	 // BASELINE mode 15 - dPhi12/23/34 + combos, theta, FR1, St1 ring, dTh14, bend1, RPC 1/2/3/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x041f11ff) );
       }
       // 3-station tracks
       else if   (MODE == 14) {
	 // BASELINE mode 14 - dPhi12/23/13, theta, FR1/2, St1 ring, dTh13, bend1, RPC 1/2/3
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x7200132f) );
       } else if (MODE == 13) {
	 // BASELINE mode 13 - dPhi12/24/14, theta, FR1/2, St1 ring, dTh14, bend1, RPC 1/2/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xb40013c7) );
       } else if (MODE == 11) {
	 // BASELINE mode 11 - dPhi13/34/14, theta, FR1/3, St1 ring, dTh14, bend1, RPC 1/3/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xd4001573) );
       } else if (MODE ==  7) {
	 // BASELINE mode  7 - dPhi23/34/24, theta, FR2, dTh24, bend2, RPC 2/3/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xe8002299) );
       } 
       // 2-station tracks
       else if   (MODE == 12) {
	 // BASELINE mode 12 - dPhi12, theta, FR1/2, St1 ring, dTh12, bend1/2, RPC 1/2
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x30403307) );
       } else if (MODE == 10) {
	 // BASELINE mode 10 - dPhi13, theta, FR1/3, St1 ring, dTh13, bend1/3, RPC 1/3
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x52005523) );
       } else if (MODE ==  9) {
	 // BASELINE mode  9 - dPhi14, theta, FR1/4, St1 ring, dTh14, bend1/4, RPC 1/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x94009943) );
       } else if (MODE ==  6) {
	 // BASELINE mode  6 - dPhi23, theta, FR2/3, dTh23, bend2/3, RPC 2/3
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0x60806609) );
       } else if (MODE ==  5) {
	 // BASELINE mode  5 - dPhi24, theta, FR2/4, dTh24, bend2/4, RPC 2/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xa800aa81) );
       } else if (MODE ==  3) {
	 // BASELINE mode  3 - dPhi34, theta, FR3/4, dTh12, bend3/4, RPC 3/4
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xc100cc11) );
       } else if (MODE == 0) {
	 // Null track, for testing EMTF performance
	 factories.push_back( std::make_tuple( nullF, nullL, factName, var_names, var_vals, 0xc0000001) );
       }

     } // End loop: for (int iTarg = 0; iTarg < TARG_VARS.size(); iTarg++)
   } // End loop: for (int iWgt = 0; iWgt < EVT_WGTS.size(); iWgt++)

   // Initialize factories and dataloaders
   for (UInt_t iFact = 0; iFact < factories.size(); iFact++) {
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
   in_vars.push_back( MVA_var( "theta",     "Track #theta",          "int", 'I', -88 ) ); // 0x0000 0001
   in_vars.push_back( MVA_var( "St1_ring2", "St 1 hit in ring 2",    "int", 'I', -88 ) ); // 0x0000 0002  
   in_vars.push_back( MVA_var( "dPhi_12",   "#phi(2) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0004
   in_vars.push_back( MVA_var( "dPhi_23",   "#phi(3) - #phi(2)",     "int", 'I', -88 ) ); // 0x0000 0008

   in_vars.push_back( MVA_var( "dPhi_34",   "#phi(4) - #phi(3)",     "int", 'I', -88 ) ); // 0x0000 0010
   in_vars.push_back( MVA_var( "dPhi_13",   "#phi(3) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0020
   in_vars.push_back( MVA_var( "dPhi_14",   "#phi(4) - #phi(1)",     "int", 'I', -88 ) ); // 0x0000 0040
   in_vars.push_back( MVA_var( "dPhi_24",   "#phi(4) - #phi(2)",     "int", 'I', -88 ) ); // 0x0000 0080

   in_vars.push_back( MVA_var( "FR_1",      "St 1 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0100
   in_vars.push_back( MVA_var( "FR_2",      "St 2 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0200
   in_vars.push_back( MVA_var( "FR_3",      "St 3 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0400
   in_vars.push_back( MVA_var( "FR_4",      "St 4 LCT F/R",          "int", 'I', -88 ) ); // 0x0000 0800

   in_vars.push_back( MVA_var( "bend_1",    "St 1 LCT bending",      "int", 'I', -88 ) ); // 0x0000 1000
   in_vars.push_back( MVA_var( "bend_2",    "St 2 LCT bending",      "int", 'I', -88 ) ); // 0x0000 2000
   in_vars.push_back( MVA_var( "bend_3",    "St 3 LCT bending",      "int", 'I', -88 ) ); // 0x0000 4000
   in_vars.push_back( MVA_var( "bend_4",    "St 4 LCT bending",      "int", 'I', -88 ) ); // 0x0000 8000

   in_vars.push_back( MVA_var( "dPhiSum4",  "#Sigmad#phi (6)",       "int", 'I', -88 ) ); // 0x0001 0000
   in_vars.push_back( MVA_var( "dPhiSum4A", "#Sigma|d#phi| (6)",     "int", 'I', -88 ) ); // 0x0002 0000
   in_vars.push_back( MVA_var( "dPhiSum3",  "#Sigmad#phi (3)",       "int", 'I', -88 ) ); // 0x0004 0000
   in_vars.push_back( MVA_var( "dPhiSum3A", "#Sigma|d#phi| (3)",     "int", 'I', -88 ) ); // 0x0008 0000
   
   in_vars.push_back( MVA_var( "outStPhi",  "#phi outlier St",       "int", 'I', -88 ) ); // 0x0010 0000
   in_vars.push_back( MVA_var( "filler",    "Filler",                "int", 'I', -88 ) ); // 0x0020 0000
   in_vars.push_back( MVA_var( "dTh_12",    "#theta(2) - #theta(1)", "int", 'I', -88 ) ); // 0x0040 0000
   in_vars.push_back( MVA_var( "dTh_23",    "#theta(3) - #theta(2)", "int", 'I', -88 ) ); // 0x0080 0000

   in_vars.push_back( MVA_var( "dTh_34",    "#theta(4) - #theta(3)", "int", 'I', -88 ) ); // 0x0100 0000
   in_vars.push_back( MVA_var( "dTh_13",    "#theta(3) - #theta(1)", "int", 'I', -88 ) ); // 0x0200 0000
   in_vars.push_back( MVA_var( "dTh_14",    "#theta(4) - #theta(1)", "int", 'I', -88 ) ); // 0x0400 0000
   in_vars.push_back( MVA_var( "dTh_24",    "#theta(4) - #theta(2)", "int", 'I', -88 ) ); // 0x0800 0000

   if (USE_RPC) {
     in_vars.push_back( MVA_var( "RPC_1",   "St 1 hit is RPC",       "int", 'I', -88 ) ); // 0x1000 0000
     in_vars.push_back( MVA_var( "RPC_2",   "St 2 hit is RPC",       "int", 'I', -88 ) ); // 0x2000 0000
     in_vars.push_back( MVA_var( "RPC_3",   "St 3 hit is RPC",       "int", 'I', -88 ) ); // 0x4000 0000
     in_vars.push_back( MVA_var( "RPC_4",   "St 4 hit is RPC",       "int", 'I', -88 ) ); // 0x8000 0000
   }

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

   assert( in_vars.size() > 0 );   // Need at least one input variable
   assert( targ_vars.size() > 0 ); // Need at least one target variable
   // Order is important: input variables first, then target, then specator
   all_vars.insert( all_vars.end(), in_vars.begin(), in_vars.end() );
   all_vars.insert( all_vars.end(), targ_vars.begin(), targ_vars.end() );
   if (SPEC_VARS) all_vars.insert( all_vars.end(), spec_vars.begin(), spec_vars.end() );

   // Fill each factory with the correct set of variables
   for (UInt_t iFact = 0; iFact < factories.size(); iFact++) {
     std::cout << "\n*** Factory " << std::get<2>(factories.at(iFact)) << " variables ***" << std::endl;
       
     std::cout << "*** Input ***" << std::endl;
     for (UInt_t i = 0; i < in_vars.size(); i++) {
       if ( 0x1 & (std::get<5>(factories.at(iFact)) >> i) ) { // Hex bit mask for in_vars
	 MVA_var v = in_vars.at(i);
	 std::cout << v.name << std::endl;
	 std::get<1>(factories.at(iFact))->AddVariable( v.name, v.descr, v.unit, v.type ); // Add var to dataloader 
	 std::get<3>(factories.at(iFact)).push_back( v.name );    // Add to vector of var names
	 std::get<4>(factories.at(iFact)).push_back( v.def_val ); // Add to vector of var values
       }
     }

     TString targ_str = ""; // Save name of target variable
     std::cout << "*** Target ***" << std::endl;
     for (UInt_t i = 0; i < targ_vars.size(); i++) {
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

     std::cout << "*** Spectator ***" << std::endl;
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
   UInt_t NonZBEvt = 0;
   UInt_t ZBEvt = 0;
   UInt_t nTrain = 0;
   UInt_t nTest  = 0;
   Bool_t isZB = false;
   Bool_t isTEST = false;
	
   //================================
   //Register events: loop over chains
   //================================
   for (int iCh = 0; iCh < in_chains.size(); iCh++) {
     TChain *in_chain = in_chains.at(iCh);
     
     std::cout << "\n******* About to enter the event loop for chain " << iCh+1 << " *******" << std::endl;
     
     for (UInt_t jEvt = 0; jEvt < in_chain->GetEntries(); jEvt++) {
       if (NonZBEvt > MAX_TR) break;
       if (jEvt < nSMEvents) {
	       isZB = false;
	       isTEST = false;
       }
       if (jEvt >= nSMEvents) {
	       isZB = true;
	       isTEST = true;
       }

       in_chain->GetEntry(jEvt);
	     
       UInt_t nMuons = I("nRecoMuons");//reco_* branches are true info reference
       UInt_t nHits  = I("nHits");//hit_* branches are unpacked hits 
       UInt_t nTrks  = I("nTracks");//trk_* branches are EMTF tracks
       	     
       if ( (NonZBEvt % REPORT_EVT) == 0 || (ZBEvt > 0 && (ZBEvt % REPORT_EVT) == 0 ) )
	       std::cout << "Looking at Non-ZB event " << NonZBEvt << "; ZB event " << ZBEvt << std::endl;
       
       //============================================
       //EMTF biased events can't be used in training
       //============================================
       int BarrelRecoMu=0;
       int EndcapRecoMu=0;
       for (UInt_t iMu = 0; iMu < nMuons; iMu++) {
	 //RECO mu pT >  Bias pT, Iso < Bias_Iso, match St1 segment, medium ID
	 if( F("reco_pt", iMu) >= Bias_Pt && F("reco_iso", iMu) < Bias_Iso && I("reco_ID_station", iMu) == 1 && I("reco_ID_medium", iMu) == 1){
		 //Barrel Reco mu
		 if( fabs(F("reco_eta",iMu) ) < Bias_Eta){
			 BarrelRecoMu++;
		 }
		 //Endcap Reco mu
		 if( fabs(F("reco_eta",iMu) ) >= Bias_Eta){
			 EndcapRecoMu++;
		 }
	 }//end if 
       }//end Remove bias  
       if (!isZB && BarrelRecoMu==0 && EndcapRecoMu<=1 ) isTEST = true;//Don't use EMTF biased event in training
       
       if(verbose) std::cout << "End removing bias ... "<< std::endl;    
	     
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
	 int emtf_unique_iMu = I("trk_dR_match_iReco", iTrk);       
	 double mu_pt = -999.;
	 double mu_eta = -999.;
	 double mu_phi = -999.;
	 int mu_charge = -999;
	 Bool_t mu_train = true;  // Can use the reco muon for training 
	       
	 //if can't find unique match, assign 1 GeV true pT for training
	 if( emtf_unique_match == 1 ){//note matched is -999 in 2018 NTuple
		 mu_pt = F("reco_pt", emtf_unique_iMu);
		 mu_eta = F("reco_eta", emtf_unique_iMu);
		 mu_phi = F("reco_phi", emtf_unique_iMu);
	         mu_charge = I("reco_charge", emtf_unique_iMu);
	 }
	 else {
		 continue;
		 /*
		 mu_pt = 1;
		 mu_eta = (ETAMIN+ETAMAX)/2;
		 mu_phi = emtf_phi;
	         mu_charge = emtf_charge;
		 */
	 }
	       
	 if(verbose) std::cout << "RECO kinematics ... "<< std::endl;   
	       
	 //===============================    
         //RECO mu kinematics requirements
	 //===============================
	 if ( mu_pt < PTMIN || mu_pt > PTMAX ) continue;
	 if ( fabs( mu_eta ) < ETAMIN || fabs( mu_eta ) > ETAMAX ) continue;
	 if ( mu_pt < PTMIN_TR || mu_pt > PTMAX_TR || isTEST) mu_train = false;
         
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
	 int i1=-99;
	 int i2=-99;
	 int i3=-99;
	 int i4=-99;
	 for (int jhit = 0; jhit < I("trk_nHits", iTrk); jhit++) {
		 int iHit = I("trk_iHit", iTrk, jhit);  // Access the index of each hit in the emtf track
	         if( I("hit_station", iHit) ==1 ){
			 i1 = iHit;
		 }
	         else if ( I("hit_station", iHit) == 2 ){
	                 i2 = iHit;
	         }
	         else if ( I("hit_station", iHit) == 3 ){
			 i3 = iHit;
		 }
		 else if ( I("hit_station", iHit) == 4 ){
			 i4 = iHit;
		 }
         }//end loop over hits in selected emtf track
	       
	 if(verbose) {      
	 std::cout << "hit id at 1: "<<i1<< std::endl;
	 std::cout << "hit id at 2: "<<i2<< std::endl;
	 std::cout << "hit id at 3: "<<i3<< std::endl;
	 std::cout << "hit id at 4: "<<i4<< std::endl;
	 }
	 
	 //Assign built trk properties the same as emtf track 
	 int mode     = emtf_mode;
	 int mode_CSC = emtf_mode_CSC;
	 int mode_RPC = emtf_mode_RPC;
	 if(verbose) std::cout << "mode: "<<mode<<" MODE: "<<MODE<< std::endl;
	 if (mode != MODE) continue;
	 if (mode != mode_CSC) {
		 if(verbose) std::cout << "Not CSC-only track"<< std::endl; 
		 continue;
	 }     

	 int ph1 = (i1 >= 0 ? I("hit_phi_int", i1 ) : -99); 
	 int ph2 = (i2 >= 0 ? I("hit_phi_int", i2 ) : -99);
	 int ph3 = (i3 >= 0 ? I("hit_phi_int", i3 ) : -99);
	 int ph4 = (i4 >= 0 ? I("hit_phi_int", i4 ) : -99);
	   
	 int th1 = (i1 >= 0 ? I("hit_theta_int", i1 ) : -99);
	 int th2 = (i2 >= 0 ? I("hit_theta_int", i2 ) : -99);
	 int th3 = (i3 >= 0 ? I("hit_theta_int", i3 ) : -99);
	 int th4 = (i4 >= 0 ? I("hit_theta_int", i4 ) : -99);

	 int pat1 = (i1 >= 0 ? I("hit_pattern", i1 ) : -99);
	 int pat2 = (i2 >= 0 ? I("hit_pattern", i2 ) : -99);
	 int pat3 = (i3 >= 0 ? I("hit_pattern", i3 ) : -99);
	 int pat4 = (i4 >= 0 ? I("hit_pattern", i4 ) : -99); 

	 int st1_ring2 = (i1 >= 0 ? ( I("hit_ring", i1 ) == 2 || I("hit_ring", i1 ) == 3 ) : 0);
         
	 //===========
	 //track info
	 //===========
	 double eta;
	 double phi;
	 int endcap;
	 if      (i2 >= 0) { eta = F("hit_eta", i2 ); phi = F("hit_phi", i2 ); }
	 else if (i3 >= 0) { eta = F("hit_eta", i3 ); phi = F("hit_phi", i3 ); }
	 else if (i4 >= 0) { eta = F("hit_eta", i4 ); phi = F("hit_phi", i4 ); }
	 else if (i1 >= 0) { eta = F("hit_eta", i1 ); phi = F("hit_phi", i1 ); }
	 endcap = (eta > 0 ? +1 : -1);
		 
	 //========================
	 //Variables to go into BDT
	 //========================
	 int theta;
	 int dPh12, dPh13, dPh14, dPh23, dPh24, dPh34, dPhSign;
	 int dPhSum4, dPhSum4A, dPhSum3, dPhSum3A, outStPh;
	 int dTh12, dTh13, dTh14, dTh23, dTh24, dTh34;
	 int FR1, FR2, FR3, FR4;
	 int bend1, bend2, bend3, bend4;
	 int RPC1, RPC2, RPC3, RPC4;

	 // Extra variables for FR computation
	 int ring1, cham1, cham2, cham3, cham4;

	 if (MODE == 0) {
		 theta = emtf_eta_int;
		 goto EMTF_ONLY;
	 }

	 theta = CalcTrackTheta( th1, th2, th3, th4, st1_ring2, mode, BIT_COMP );
	   
	 CalcDeltaPhis( dPh12, dPh13, dPh14, dPh23, dPh24, dPh34, dPhSign,
			  dPhSum4, dPhSum4A, dPhSum3, dPhSum3A, outStPh,
			  ph1, ph2, ph3, ph4, mode, BIT_COMP );
	  
	 CalcDeltaThetas( dTh12, dTh13, dTh14, dTh23, dTh24, dTh34,
			    th1, th2, th3, th4, mode, BIT_COMP );

	 // In firmware, RPC 'FR' bit set according to FR of corresponding CSC chamber
	 ring1 = (i1 >= 0 ? I("hit_ring", i1 ) : -99);
	 cham1 = (i1 >= 0 ? I("hit_chamber", i1 ) : -99);
	 cham2 = (i2 >= 0 ? I("hit_chamber", i2 ) : -99);
	 cham3 = (i3 >= 0 ? I("hit_chamber", i3 ) : -99);
	 cham4 = (i4 >= 0 ? I("hit_chamber", i4 ) : -99);

	 FR1 = (i1 >= 0 ? (cham1 % 2 == 0) : -99);  // Odd chambers are bolted to the iron,
	 FR2 = (i2 >= 0 ? (cham2 % 2 == 0) : -99);  // which faces forwared in stations 1 & 2,
	 FR3 = (i3 >= 0 ? (cham3 % 2 == 1) : -99);  // backwards in 3 & 4
	 FR4 = (i4 >= 0 ? (cham4 % 2 == 1) : -99);
	 if (ring1 == 3) FR1 = 0;                   // In ME1/3 chambers are non-overlapping

	 CalcBends( bend1, bend2, bend3, bend4,
		   pat1, pat2, pat3, pat4, 
		   dPhSign, endcap, mode, BIT_COMP );

	 RPC1 = (i1 >= 0 ? ( I("hit_isRPC", i1 ) == 1 ? 1 : 0) : -99);
	 RPC2 = (i2 >= 0 ? ( I("hit_isRPC", i2 ) == 1 ? 1 : 0) : -99);
	 RPC3 = (i3 >= 0 ? ( I("hit_isRPC", i3 ) == 1 ? 1 : 0) : -99);
	 RPC4 = (i4 >= 0 ? ( I("hit_isRPC", i4 ) == 1 ? 1 : 0) : -99);

	 CalcRPCs( RPC1, RPC2, RPC3, RPC4, mode, st1_ring2, theta, BIT_COMP );
	   
	 // Clean out showering muons with outlier station 1, or >= 2 outlier stations
	 if (log2(mu_pt) > 6 && CLEAN_HI_PT && MODE == 15)
		 if ( dPhSum4A >= fmax(40., 332. - 40*log2(mu_pt)) )
			 if ( outStPh < 2 || dPhSum3A >= fmax(24., 174. - 20*log2(mu_pt)) )
				 mu_train = false;

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
	       if ( vName == "theta" )
		 var_vals.at(iVar) = theta;
	       if ( vName == "St1_ring2" )
		 var_vals.at(iVar) = st1_ring2;

	       if ( vName == "dPhi_12" )
		 var_vals.at(iVar) = dPh12;
	       if ( vName == "dPhi_13" )
		 var_vals.at(iVar) = dPh13;
	       if ( vName == "dPhi_14" )
		 var_vals.at(iVar) = dPh14;
	       if ( vName == "dPhi_23" )
		 var_vals.at(iVar) = dPh23;
	       if ( vName == "dPhi_24" )
		 var_vals.at(iVar) = dPh24;
	       if ( vName == "dPhi_34" )
		 var_vals.at(iVar) = dPh34;
	       
	       if ( vName == "FR_1" )
		 var_vals.at(iVar) = FR1;
	       if ( vName == "FR_2" )
		 var_vals.at(iVar) = FR2;
	       if ( vName == "FR_3" )
		 var_vals.at(iVar) = FR3;
	       if ( vName == "FR_4" )
		 var_vals.at(iVar) = FR4;
	       
	       if ( vName == "bend_1" )
		 var_vals.at(iVar) = bend1;
	       if ( vName == "bend_2" )
		 var_vals.at(iVar) = bend2;
	       if ( vName == "bend_3" )
		 var_vals.at(iVar) = bend3;
	       if ( vName == "bend_4" )
		 var_vals.at(iVar) = bend4;
	       
	       if ( vName == "dPhiSum4" )
		 var_vals.at(iVar) = dPhSum4;
	       if ( vName == "dPhiSum4A" )
		 var_vals.at(iVar) = dPhSum4A;
	       if ( vName == "dPhiSum3" )
		 var_vals.at(iVar) = dPhSum3;
	       if ( vName == "dPhiSum3A" )
		 var_vals.at(iVar) = dPhSum3A;
	       if ( vName == "outStPhi" )
		 var_vals.at(iVar) = outStPh;

	       if ( vName == "dTh_12" )
		 var_vals.at(iVar) = dTh12;
	       if ( vName == "dTh_13" )
		 var_vals.at(iVar) = dTh13;
	       if ( vName == "dTh_14" )
		 var_vals.at(iVar) = dTh14;
	       if ( vName == "dTh_23" )
		 var_vals.at(iVar) = dTh23;
	       if ( vName == "dTh_24" )
		 var_vals.at(iVar) = dTh24;
	       if ( vName == "dTh_34" )
		 var_vals.at(iVar) = dTh34;

	       if ( vName == "RPC_1" )
		 var_vals.at(iVar) = RPC1;
	       if ( vName == "RPC_2" )
		 var_vals.at(iVar) = RPC2;
	       if ( vName == "RPC_3" )
		 var_vals.at(iVar) = RPC3;
	       if ( vName == "RPC_4" )
		 var_vals.at(iVar) = RPC4;

	       
	       //////////////////////////////
	       ///  Target and variables  ///
	       //////////////////////////////

	       if ( vName == "GEN_pt_trg" )
		 var_vals.at(iVar) = fmin(mu_pt, PTMAX_TRG);
	       if ( vName == "inv_GEN_pt_trg" )
		 var_vals.at(iVar) = 1. / fmin(mu_pt, PTMAX_TRG);
	       if ( vName == "log2_GEN_pt_trg" )
		 var_vals.at(iVar) = log2(fmin(mu_pt, PTMAX_TRG));
	       if ( vName == "sqrt_GEN_pt_trg" )
		 var_vals.at(iVar) = sqrt(fmin(mu_pt, PTMAX_TRG));
	       if ( vName == "GEN_charge_trg" )
		 var_vals.at(iVar) = mu_charge * dPhSign;

	       /////////////////////////////
	       ///  Spectator variables  ///
	       /////////////////////////////

	       if ( vName == "GEN_pt" )
		 var_vals.at(iVar) = mu_pt;
	       if ( vName == "EMTF_pt" )
	       	 var_vals.at(iVar) = emtf_pt;
	       if ( vName == "inv_GEN_pt" )
		 var_vals.at(iVar) = 1. / mu_pt;
	       if ( vName == "inv_EMTF_pt" )
	       	 var_vals.at(iVar) = 1. / emtf_pt;
	       if ( vName == "log2_GEN_pt" )
		 var_vals.at(iVar) = log2(mu_pt);
	       if ( vName == "log2_EMTF_pt" )
	       	 var_vals.at(iVar) = (emtf_pt > 0 ? log2(emtf_pt) : -99);

	       if ( vName == "GEN_eta" )
		 var_vals.at(iVar) = mu_eta;
	       if ( vName == "EMTF_eta" )
	       	 var_vals.at(iVar) = emtf_eta;
	       if ( vName == "TRK_eta" )
	       	 var_vals.at(iVar) = eta;
	       if ( vName == "GEN_phi" )
		 var_vals.at(iVar) = mu_phi;
	       if ( vName == "EMTF_phi" )
	       	 var_vals.at(iVar) = emtf_phi;
	       if ( vName == "TRK_phi" )
	       	 var_vals.at(iVar) = phi;
	       if ( vName == "GEN_charge" )
		 var_vals.at(iVar) = mu_charge;
	       if ( vName == "EMTF_charge" )
	       	 var_vals.at(iVar) = emtf_charge;

	       if ( vName == "EMTF_mode" )
	       	 var_vals.at(iVar) = emtf_mode;
	       if ( vName == "EMTF_mode_CSC" )
	       	 var_vals.at(iVar) = emtf_mode_CSC;
	       if ( vName == "EMTF_mode_RPC" )
	       	 var_vals.at(iVar) = emtf_mode_RPC;
	       if ( vName == "TRK_mode" )
	       	 var_vals.at(iVar) = mode;
	       if ( vName == "TRK_mode_CSC" )
	       	 var_vals.at(iVar) = mode_CSC;
	       if ( vName == "TRK_mode_RPC" )
	       	 var_vals.at(iVar) = mode_RPC;
	       if ( vName == "dPhi_sign" )
		 var_vals.at(iVar) = dPhSign;
	       if ( vName == "evt_weight" )
		 var_vals.at(iVar) = evt_weight;
	       
	     } // End loop: for (UInt_t iVar = 0; iVar < var_names.size(); iVar++)
	     
	     // Load values into event
	     if ( mu_train && MODE > 0 ) { 
	       std::get<1>(factories.at(iFact))->AddTrainingEvent( "Regression", var_vals, evt_weight );
	       if (iFact == 0) nTrain += 1;
	       // std::cout << "Added train event " << nTrain << std::endl;
	     }
	     else {
	       std::get<1>(factories.at(iFact))->AddTestEvent( "Regression", var_vals, evt_weight );
	       if (iFact == 0) nTest += 1;
	       // std::cout << "Added test event " << nTest << std::endl;
	     }
	 } // End loop: for (UInt_t iFact = 0; iFact < factories.size(); iFact++) 
	       
       } // End loop: for emtf trks
	     
       if(jEvt < nZBEvents){
	       NonZBEvt += 1;
       }
       else{
	       ZBEvt += 1;
       }
       
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
   std::cout << "NTr: " << NTr << ", NTe: " << NTe << std::endl;

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


int main( int argc, char** argv )
{
   // Select methods (don't look at this code - not of interest)
   TString methodList;
   for (int i=1; i<argc; i++) {
      TString regMethod(argv[i]);
      if(regMethod=="-b" || regMethod=="--batch") continue;
      if (!methodList.IsNull()) methodList += TString(",");
      methodList += regMethod;
   }
   PtRegression2018(methodList);
   return 0;
}
