
// *** Default user settings *** //
TString IN_DIR_NAME   = ".";          // Directory for input ROOT files
TString OUT_DIR_NAME  = "/home/ws13/TMVA/TMVA/EMTFPtAssign2018";      // Directory for output ROOT file
TString OUT_FILE_NAME = "RateVsEff";  // Name base for output ROOT file
std::vector<PtAlgo> ALGOS    = {};    // Vector of factory-MVA-mode sets for evaluation
std::vector<int>    EFF_CUTS = {};    // Vector of efficiency thresholds (%)
std::vector<int>    TURN_ONS = {};    // Vector of pT cuts for turn-on curves

namespace RateVsEff_cfg {

  inline void ConfigureUser( const TString USER ) {
    
    std::cout << "\nConfiguring RateVsEff code for user " << USER << std::endl;

    if (USER == "WEI") {
      const int MODE = 15;  // Specify one mode in particular to look at

      IN_DIR_NAME   = "/home/ws13/TMVA/TMVA/EMTFPtAssign2018";
      TString out_str;
      out_str.Form("RateVsEff_mode_%d_eta_1p2_2p5", MODE);
      OUT_FILE_NAME = out_str;

      EFF_CUTS    = {90};
      TURN_ONS    = {8, 16, 24};

      TString in_str;
      TString fact_str;
      TString ID_str;
      TString alias_str;

      PtAlgo EMTF15;  // 2017 EMTF pT algorithm, mode 15
      EMTF15.in_file_name = "PtRegression2018_MODE_15_bitCompr_CSC.root";
      EMTF15.fact_name    = "f_MODE_15_invPtTarg_invPtWgt_bitCompr_RPC";
      EMTF15.MVA_name     = "EMTF_pt";
      EMTF15.unique_ID    = "EMTF15";
      EMTF15.alias        = "EMTF mode 15";
      EMTF15.modes        = {15};
      EMTF15.modes_CSC    = {15};
      EMTF15.modes_RPC    = {0};  // No RPC hits allowed
      EMTF15.trg_pt_scale = 1.2 / (1 - 0.015*fmin(20., pt) );  // 2017 pT scale 
      EMTF15.color        = 1;  // kBlack 
      
      // Mode 15, invPt pT target, invPt weight
      PtAlgo BDT15_invPt_invPt_Sq;
      BDT15_invPt_invPt_Sq.in_file_name = "PtRegression2018_MODE_15_bitCompr_CSC.root";
      BDT15_invPt_invPt_Sq.fact_name    = "f_MODE_15_invPtTarg_invPtWgt_bitCompr_RPC";
      BDT15_invPt_invPt_Sq.MVA_name     = "BDTG_AWB_Sq";
      BDT15_invPt_invPt_Sq.unique_ID    = "BDT_15_invPt_Sq";
      BDT15_invPt_invPt_Sq.alias        = "invPt target, LeastSq loss";
      BDT15_invPt_invPt_Sq.modes        = {15};
      BDT15_invPt_invPt_Sq.modes_CSC    = {15};
      BDT15_invPt_invPt_Sq.modes_RPC    = {0};
      BDT15_invPt_invPt_Sq.color        = 840;  // kTeal

      ALGOS.push_back(EMTF15);  // First algo is always the standard comparison algo
      ALGOS.push_back(BDT15_invPt_invPt_Sq);
    } // End conditional: if (USER == "WEI")
    
  } // End function: inline void ConfigureUser()    

} // End namespace RateVsEff_cfg
