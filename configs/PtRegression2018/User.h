// *** Default user settings *** //
TString EOS_DIR_NAME = "root://cmseos.fnal.gov//store/user/dildick/SingleMu_Run3_Pt1to50OneOverPt_noPU_10M/crab_SingleMu_Run3_Pt1to50OneOverPt_noPU_10M_NTUPLE_20210413/210413_215540/0000/";
//TString EOS_DIR_NAME = "root://cmseos.fnal.gov//store/user/mdecaro/Ntuples/";
TString in_dir = "";
std::vector<TString> SingleMu_files = {
        "EMTF_MC_NTuple_SingleMu_1-1.root",
	"EMTF_MC_NTuple_SingleMu_1-2.root",
	"EMTF_MC_NTuple_SingleMu_1-3.root",
	"EMTF_MC_NTuple_SingleMu_1-4.root",
        "EMTF_MC_NTuple_SingleMu_2.root",
        "EMTF_MC_NTuple_SingleMu_3.root",
        "EMTF_MC_NTuple_SingleMu_4.root",
        "EMTF_MC_NTuple_SingleMu_5.root",
    	"EMTF_MC_NTuple_SingleMu_7.root"
};

TString ZeroBias_files[1] = {
	"NTuple_ZeroBias_FlatNtuple_2019_01_09_ZeroBias_PU50_Sep24_FW.root"
};
const int USESingleMu = SingleMu_files.size();//# of SM files to use
const int USEZerobias = 0;//# of ZB files to use
TString OUT_DIR_NAME  = "./";
TString OUT_FILE_NAME = "PtRegressionRun3Prep";  // Name base for output ROOT file

namespace PtRegression2018_cfg {

  inline void ConfigureUser( const TString USER ) {

    std::cout << "\nConfiguring PtRegression2018 code for user " << USER << std::endl;

    in_dir = "";
    if (USER == "dildick") {
      OUT_DIR_NAME = "./";
    }
    if (USER == "mdecaro") {
      OUT_DIR_NAME = "./";
    }
  } // End function: inline void ConfigureUser()

} // End namespace PtRegression2018_cfg
