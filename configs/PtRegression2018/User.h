// *** Default user settings *** //
TString OUT_DIR_NAME  = ".";  // Directory for output ROOT file
TString OUT_FILE_NAME = "PtRegression2018";  // Name base for output ROOT file
TString EOS_DIR_NAME  = "root://eoscms.cern.ch//store/user/abrinke1/EMTF/Emulator/ntuples";  // Input directory in 

namespace PtRegression2018_cfg {
  
  inline void ConfigureUser( const TString USER ) {
    
    std::cout << "\nConfiguring PtRegression2018 code for user " << USER << std::endl;
    
    if (USER == "Wei") {
      EOS_DIR_NAME = "/home/ws13/TMVA/TMVA/INPUT/";  // Input directory in eos
      OUT_DIR_NAME = "/home/ws13/TMVA/TMVA/EMTFPtAssign2018";
      OUT_FILE_NAME = "PtRegression2018";
    }
    
  } // End function: inline void ConfigureUser()    
  
} // End namespace PtRegression2018_cfg
