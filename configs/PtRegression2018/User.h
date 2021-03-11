// *** Default user settings *** //
TString EOS_DIR_NAME = "";
TString in_dir = "";
TString SingleMu_files[1] = {
  "EMTF_MC_NTuple_01062021.root"
};

TString ZeroBias_files[1] = {
	"NTuple_ZeroBias_FlatNtuple_2019_01_09_ZeroBias_PU50_Sep24_FW.root"
};
const int USESingleMu = 1;//# of SM files to use
const int USEZerobias = 0;//# of ZB files to use
TString OUT_DIR_NAME  = "./";
TString OUT_FILE_NAME = "PtRegressionRun3Prep";  // Name base for output ROOT file

namespace PtRegression2018_cfg {

  inline void ConfigureUser( const TString USER ) {

    std::cout << "\nConfiguring PtRegression2018 code for user " << USER << std::endl;

    EOS_DIR_NAME = "root://cmseos.fnal.gov//store/user/mdecaro/Ntuples/";  // Input directory in eos
    in_dir = "";

    if (USER == "dildick") {
      OUT_DIR_NAME = "./";
    }
    if (USER == "mdecaro") {
      OUT_DIR_NAME = "./";
    }
  } // End function: inline void ConfigureUser()

} // End namespace PtRegression2018_cfg
