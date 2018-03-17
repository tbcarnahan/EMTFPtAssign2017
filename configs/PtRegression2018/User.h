// *** Default user settings *** //
TString EOS_DIR_NAME  = "root://eoscms.cern.ch//store/user/abrinke1/EMTF/Emulator/ntuples";  // Input directory in 
TString in_dir = "Ntuples/"; 
TString SingleMu_files[3] = { 
	  		    "NTuple_SingleMuon_FlatNtuple_Run_306092_2018_03_02_SingleMu.root",
   			    "NTuple_SingleMuon_FlatNtuple_Run_306135_2018_03_02_SingleMu.root",
   			    "NTuple_SingleMuon_FlatNtuple_Run_306154_2018_03_02_SingleMu.root"
};   
TString ZeroBias_files[4] = { 
	  		    "NTuple_ZeroBias1_FlatNtuple_Run_306091_2018_03_02_ZB1.root",
		            "NTuple_ZeroBias2_FlatNtuple_Run_306091_2018_03_02_ZB2.root",
		            "NTuple_ZeroBias3_FlatNtuple_Run_306091_2018_03_02_ZB3.root", 
		 	    "NTuple_ZeroBias4_FlatNtuple_Run_306091_2018_03_02_ZB4.root"
};
const int USESingleMu = 3;//# of SM files to use
const int USEZerobias = 4;//# of ZB files to use
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
