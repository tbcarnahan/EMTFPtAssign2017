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
TString OUT_DIR_NAME  = ".";  // Directory for output ROOT file
TString OUT_FILE_NAME = "PtRegression2018";  // Name base for output ROOT file

namespace PtRegression2018_cfg {

  inline void ConfigureUser( const TString USER ) {

    std::cout << "\nConfiguring PtRegression2018 code for user " << USER << std::endl;

    EOS_DIR_NAME = "root://cmsxrootd-site.fnal.gov///store/user/mdecaro/Ntuples/";  // Input directory in eos
    in_dir = "";
    OUT_FILE_NAME = "PtRegression2018";

    if (USER == "Sven") {
      OUT_DIR_NAME = "/uscms/home/dildick/nobackup/work/Rice_EMTF_Summer2019/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/";
    }
    if (USER == "Matthew") {
      OUT_DIR_NAME = "~/nobackup/BDTGEM/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/";
    }
  } // End function: inline void ConfigureUser()

} // End namespace PtRegression2018_cfg
