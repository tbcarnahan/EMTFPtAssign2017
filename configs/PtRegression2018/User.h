// *** Default user settings *** //
TString EOS_DIR_NAME  = "root://eoscms.cern.ch//store/user/abrinke1/EMTF/Emulator/ntuples";  // Input directory in 
TString in_dir = "Ntuples/"; 
TString SingleMu_files[1] = { 
   			    //"NTuple_SingleMuon_FlatNtuple_Run_306154_2018_05_07_SingleMu_2018_emul_dTh4.root"
			    //"NTuple_SingleMuon_FlatNtuple_Run_306154_2018_05_07_SingleMu_2017_emul.root"
		            //"NTuple_SingleMuon_FlatNtuple_Run_2018D_v2_2018_10_25_SingleMuon_PU50_postSep26.root"
	                    "NTuple_SingleMuon_FlatNtuple_2019_01_09_SingleMuon_PU50_Sep24_FW.root"
};   
TString ZeroBias_files[1] = {  
		 	    //"NTuple_ZeroBias1_FlatNtuple_Run_306091_2018_05_07_ZB1_2018_emul_dTh4.root"
		            //"NTuple_ZeroBias1_FlatNtuple_Run_306091_2018_05_07_ZB1_2017_emul.root"
	                    //"NTuple_SingleMuon_FlatNtuple_Run_2018D_v2_2018_10_25_ZeroBias_PU50_postSep26.root"
	                    "NTuple_ZeroBias_FlatNtuple_2019_01_09_ZeroBias_PU50_Sep24_FW.root"
};
const int USESingleMu = 1;//# of SM files to use
const int USEZerobias = 1;//# of ZB files to use
TString OUT_DIR_NAME  = ".";  // Directory for output ROOT file
TString OUT_FILE_NAME = "PtRegression2018";  // Name base for output ROOT file

namespace PtRegression2018_cfg {
  
  inline void ConfigureUser( const TString USER ) {
    
    std::cout << "\nConfiguring PtRegression2018 code for user " << USER << std::endl;
    
    if (USER == "Wei") {
      EOS_DIR_NAME = "/home/ws13/TMVA/TMVA/INPUT/";  // Input directory in eos
      in_dir = "Ntuples/"; 
      OUT_DIR_NAME = "/home/ws13/TMVA/TMVA/EMTFPtAssign2018";
      OUT_FILE_NAME = "PtRegression2018";
    }
    
  } // End function: inline void ConfigureUser()    
  
} // End namespace PtRegression2018_cfg
