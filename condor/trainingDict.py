## dictionary with trainings
## label, directory, legend

prefix = "root://cmseos.fnal.gov//store/user/dildick/"
## all output files ahve the same name. The directory says all information
fileName = "PtRegression_output.root"
xmlFileName = ""

trainings = {

    ## Run-2 uncompressed

    # 4-station
    "Run2_Mode15_Uncompressed" : [prefix + "EMTF_BDT_Train_Mode15_Prep2018DataRate_eta1.25to2.4_isRun2_Selection0xf41f11ff_20210513_140026/" + fileName, "Run-2, Mode 15"],
    # 3-station
    "Run2_Mode14_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 14"],
    "Run2_Mode13_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 13"],
    "Run2_Mode11_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 11"],
    "Run2_Mode7_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 7"],
    # 2-station
    "Run2_Mode12_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 12"],
    "Run2_Mode10_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 10"],
    "Run2_Mode9_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 9"],
    "Run2_Mode6_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 6"],
    "Run2_Mode5_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 5"],
    "Run2_Mode3_Uncompressed" : [prefix + "" + fileName, "Run-2, Mode 3"],


    ## Run-2 compressed

    # 4-station
    "Run2_Mode15_Compressed" : [prefix + "" + fileName, "Run-2, Mode 15, Compr."],
    # 3-station
    "Run2_Mode14_Compressed" : [prefix + "" + fileName, "Run-2, Mode 14, Compr."],
    "Run2_Mode13_Compressed" : [prefix + "" + fileName, "Run-2, Mode 13, Compr."],
    "Run2_Mode11_Compressed" : [prefix + "" + fileName, "Run-2, Mode 11, Compr."],
    "Run2_Mode7_Compressed" : [prefix + "" + fileName, "Run-2, Mode 7, Compr."],
    # 2-station
    "Run2_Mode12_Compressed" : [prefix + "" + fileName, "Run-2, Mode 12, Compr."],
    "Run2_Mode10_Compressed" : [prefix + "" + fileName, "Run-2, Mode 10, Compr."],
    "Run2_Mode9_Compressed" : [prefix + "" + fileName, "Run-2, Mode 9, Compr."],
    "Run2_Mode6_Compressed" : [prefix + "" + fileName, "Run-2, Mode 6, Compr."],
    "Run2_Mode5_Compressed" : [prefix + "" + fileName, "Run-2, Mode 5, Compr."],
    "Run2_Mode3_Compressed" : [prefix + "" + fileName, "Run-2, Mode 3, Compr."],

    ## Run-3 V1.0 (change bend_i by slope_i) uncompressed

    # 4-station
    "Run3_V1p0_Mode15_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15"],
    # 3-station
    "Run3_V1p0_Mode14_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14"],
    "Run3_V1p0_Mode13_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13"],
    "Run3_V1p0_Mode11_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11"],
    "Run3_V1p0_Mode7_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7"],
    # 2-station
    "Run3_V1p0_Mode12_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12"],
    "Run3_V1p0_Mode10_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10"],
    "Run3_V1p0_Mode9_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9"],
    "Run3_V1p0_Mode6_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6"],
    "Run3_V1p0_Mode5_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5"],
    "Run3_V1p0_Mode3_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3"],

    ## Run-3 V1.0 (change bend_i by slope_i) compressed

    # 4-station
    "Run3_V1p0_Mode15_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15, Compr."],
    # 3-station
    "Run3_V1p0_Mode14_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14, Compr."],
    "Run3_V1p0_Mode13_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13, Compr."],
    "Run3_V1p0_Mode11_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11, Compr."],
    "Run3_V1p0_Mode7_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7, Compr."],
    # 2-station
    "Run3_V1p0_Mode12_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12, Compr."],
    "Run3_V1p0_Mode10_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10, Compr."],
    "Run3_V1p0_Mode9_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9, Compr."],
    "Run3_V1p0_Mode6_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6, Compr."],
    "Run3_V1p0_Mode5_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5, Compr."],
    "Run3_V1p0_Mode3_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3, Compr."],

    ## Run-3 V1.1 (change bend_i by slope_i, 1/4-strip resolution) uncompressed

    # 4-station
    "Run3_V1p1_Mode15_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15"],
    # 3-station
    "Run3_V1p1_Mode14_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14"],
    "Run3_V1p1_Mode13_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13"],
    "Run3_V1p1_Mode11_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11"],
    "Run3_V1p1_Mode7_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7"],
    # 2-station
    "Run3_V1p1_Mode12_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12"],
    "Run3_V1p1_Mode10_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10"],
    "Run3_V1p1_Mode9_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9"],
    "Run3_V1p1_Mode6_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6"],
    "Run3_V1p1_Mode5_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5"],
    "Run3_V1p1_Mode3_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3"],

    ## Run-3 V1.1 (change bend_i by slope_i, 1/4-strip resolution) compressed

    # 4-station
    "Run3_V1p1_Mode15_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15, Compr."],
    # 3-station
    "Run3_V1p1_Mode14_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14, Compr."],
    "Run3_V1p1_Mode13_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13, Compr."],
    "Run3_V1p1_Mode11_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11, Compr."],
    "Run3_V1p1_Mode7_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7, Compr."],
    # 2-station
    "Run3_V1p1_Mode12_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12, Compr."],
    "Run3_V1p1_Mode10_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10, Compr."],
    "Run3_V1p1_Mode9_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9, Compr."],
    "Run3_V1p1_Mode6_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6, Compr."],
    "Run3_V1p1_Mode5_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5, Compr."],
    "Run3_V1p1_Mode3_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3, Compr."],

    ## Run-3 V1.2 (change bend_i by slope_i, 1/8-strip resolution) uncompressed

    # 4-station
    "Run3_V1p2_Mode15_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15"],
    # 3-station
    "Run3_V1p2_Mode14_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14"],
    "Run3_V1p2_Mode13_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13"],
    "Run3_V1p2_Mode11_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11"],
    "Run3_V1p2_Mode7_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7"],
    # 2-station
    "Run3_V1p2_Mode12_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12"],
    "Run3_V1p2_Mode10_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10"],
    "Run3_V1p2_Mode9_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9"],
    "Run3_V1p2_Mode6_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6"],
    "Run3_V1p2_Mode5_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5"],
    "Run3_V1p2_Mode3_Uncompressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3"],

    ## Run-3 V1.2 (change bend_i by slope_i, 1/8-strip resolution) compressed

    # 4-station
    "Run3_V1p2_Mode15_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 15, Compr."],
    # 3-station
    "Run3_V1p2_Mode14_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 14, Compr."],
    "Run3_V1p2_Mode13_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 13, Compr."],
    "Run3_V1p2_Mode11_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 11, Compr."],
    "Run3_V1p2_Mode7_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 7, Compr."],
    # 2-station
    "Run3_V1p2_Mode12_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 12, Compr."],
    "Run3_V1p2_Mode10_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 10, Compr."],
    "Run3_V1p2_Mode9_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 9, Compr."],
    "Run3_V1p2_Mode6_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 6, Compr."],
    "Run3_V1p2_Mode5_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 5, Compr."],
    "Run3_V1p2_Mode3_Compressed" : [prefix + "" + fileName, "Run-3 V1.0, Mode 3, Compr."],
}
