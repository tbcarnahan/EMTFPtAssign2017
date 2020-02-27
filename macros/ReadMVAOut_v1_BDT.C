
/////////////////////////////////////////////////////////
///          Macro to compute rate and efficiency     ///
///            Wei Shi         12.18.18               ///
///          For Run 3 training on data using BDT     ///
/////////////////////////////////////////////////////////

#include "TFile.h"
#include "TSystem.h"
#include "TChain.h"
#include "TTree.h"
#include "TBranch.h"
#include "TH1.h"
#include "TH2.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TCanvas.h"
#include <vector>
#include "stdio.h"
#include "math.h"
#include "TMath.h"
#include "TGraph.h"

void ReadMVAOut_v1_BDT() {

  // Initialize empty file to access each file in the list
  TFile *file_tmp(0);

  // List of input files
  std::vector<TString> in_file_names;
  in_file_names.push_back(
                          "/uscms/home/dildick/nobackup/work/Rice_EMTF_Summer2019/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/PtRegression2018_MODE_15_noBitCompr_noRPC_GEM.root"
                          //"/home/ws13/TMVA/TMVA/EMTFPtAssign2018/PtRegression2018_MODE_15_noBitCompr_noRPC.root"
                          );

  // Open all input files
  for (UInt_t i = 0; i < in_file_names.size(); i++) {
    if ( !gSystem->AccessPathName(in_file_names.at(i)) )
      file_tmp = TFile::Open( in_file_names.at(i) ); // Check if file exists
    if (!file_tmp) {
      std::cout << "ERROR: could not open data file " << in_file_names.at(i) << std::endl;
      return;
    }
  }

  // Add trees from the input files to the TChain
  TChain *train_chain = new TChain("f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_GEM/TrainTree");
  TChain *test_chain = new TChain("f_MODE_15_logPtTarg_invPtWgt_noBitCompr_noRPC_GEM/TestTree");
  for (UInt_t i = 0; i < in_file_names.size(); i++) {
    train_chain->Add( in_file_names.at(i) );
    test_chain->Add( in_file_names.at(i) );
  }

    //bins for trigger efficiency
    double trigger_Cut[50]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50};//for cut
    double trigger_Cut_scaled[50]={0};//scaled so BDT reach 90% at each trigger cut
    double EMTF_trigger_Cut_scaled[50]={0};//scale EMTF to 90%

    double GEN_pT[51]={1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,256};//for counting purpose only
    double count[50]={0};//total count in each bin

    double pass_count[50][50]={0};//BDT predict
    double EMTF_pass_count[50][50]={0};//current EMTF
    double efficiency[50][50]={0};//BDT efficiency
    double EMTF_efficiency[50][50]={0};//EMTF efficiency

    //choose special trigger cuts to evaluate how scale factor change
    double trigger_Cut_special[3] = {8,16,24};
    const Int_t special_cuts=3;

    //Not scaled to 90%
    double efficiency_special[3][50]={0};//BDT efficiency
    double EMTF_efficiency_special[3][50]={0};//EMTF efficiency

  // Get branches from the chains
    Long64_t test_events=0;

    Float_t EMTF_pt_test_br;
    Float_t GEN_pt_test_br;
    Float_t log_GEN_pt_test_br;
    Float_t BDT_test_br;
    //special for identifying ZeroBias data in test
    Float_t GEN_eta_test_br;
    Int_t GEN_charge_test_br;

    //test
    test_chain->SetBranchAddress("EMTF_pt", &EMTF_pt_test_br);
    test_chain->SetBranchAddress("GEN_pt", &GEN_pt_test_br);
    test_chain->SetBranchAddress("log2_GEN_pt_trg", &log_GEN_pt_test_br);
    test_chain->SetBranchAddress("BDTG_AWB_Sq", &BDT_test_br);
    test_chain->SetBranchAddress("GEN_eta", &GEN_eta_test_br);
    test_chain->SetBranchAddress("GEN_charge", &GEN_charge_test_br);

    test_events = test_chain->GetEntries();

  std::cout << "\n******* 1st Enter the test event loop *******" << std::endl;
  for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++) {

  //  if (iEvt > 10) break;
  //  if ( (iEvt % 1) == 0 )
      //std::cout << "\n*** Looking at event " << iEvt << " ***" <<  std::endl;

    test_chain->GetEntry(iEvt);

      //test trigger efficiency 50 bins, 50 cuts as well
      for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {
          if (GEN_pt_test_br > GEN_pT[Gen_bin] && GEN_pt_test_br <= GEN_pT[Gen_bin+1]){
              //need to count muons in all bins, don't use break
              count[Gen_bin]++;

              //deal with each cut
              for(int Cut_bin=0;Cut_bin<50;Cut_bin++){
                  //BDT is targeting log2pT, need to convert
                  if (pow(2, BDT_test_br) > trigger_Cut[Cut_bin]) {
                      pass_count[Cut_bin][Gen_bin]++;
                  }//end if BDT
                  if (EMTF_pt_test_br > trigger_Cut[Cut_bin]){
                      EMTF_pass_count[Cut_bin][Gen_bin]++;
                  }//end if EMTF
              }//end trigger cuts

          }//end if GEN_pt
      }//end for Gen_bin

  } // End loop: for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++)
  //std::cout << "\n******* Leaving the test event loop *******" << std::endl;

    TProfile2D* BDT_trigger_Gen_efficiency = new TProfile2D("BDT_trigger_Gen_efficiency","BDT trigger efficiency versus thresholds and GEN pT",49,1,50,49,1,50,0,1);
    TProfile2D*EMTF_trigger_Gen_efficiency = new TProfile2D("EMTF_trigger_Gen_efficiency","EMTF trigger efficiency versus thresholds and GEN pT",49,1,50,49,1,50,0,1);

    //======================================================
    //calculate trigger efficiency BDT not scaled to 90% yet
    //======================================================
    for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {

        for(int Cut_bin=0;Cut_bin<50;Cut_bin++){

            efficiency[Cut_bin][Gen_bin]=pass_count[Cut_bin][Gen_bin]/count[Gen_bin];
            EMTF_efficiency[Cut_bin][Gen_bin]=EMTF_pass_count[Cut_bin][Gen_bin]/count[Gen_bin];
            //fill 2D profile for non-scaled BDT
            BDT_trigger_Gen_efficiency->Fill(GEN_pT[Gen_bin],trigger_Cut[Cut_bin],efficiency[Cut_bin][Gen_bin]);
            EMTF_trigger_Gen_efficiency->Fill(GEN_pT[Gen_bin],trigger_Cut[Cut_bin],EMTF_efficiency[Cut_bin][Gen_bin]);
        }//end Cut bin

    }//end Gen bin

    //write to output file
    TFile myPlot("/uscms/home/dildick/nobackup/work/Rice_EMTF_Summer2019/CMSSW_10_6_1_patch2/src/EMTFPtAssign2017/RateVsEff_mode_15.root","RECREATE");

    //write 2D non scaled efficiency plot
    BDT_trigger_Gen_efficiency->Write();
    EMTF_trigger_Gen_efficiency->Write();

    //book graph for special trigger efficiency,EMTF not scaled
    TGraph *BDT_eff[special_cuts];
    TGraph *EMTF_eff[special_cuts];
    TCanvas *C[special_cuts];
    TMultiGraph *mg[special_cuts];
    for(Int_t i=0; i<special_cuts;i++){
      for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {
        //1D projection from 2D scaled eff plot
        efficiency_special[i][Gen_bin]=efficiency[Int_t(trigger_Cut_special[i])-1][Gen_bin];//minus one because of the index; 8GeV is from index 7.
        EMTF_efficiency_special[i][Gen_bin]=EMTF_efficiency[Int_t(trigger_Cut_special[i])-1][Gen_bin];
      }
    }
    for(Int_t i=0; i<special_cuts;i++){
        BDT_eff[i] = new TGraph(50,trigger_Cut,efficiency_special[i]); BDT_eff[i]->SetMarkerStyle(21); BDT_eff[i]->SetMarkerColor(2);//red
        EMTF_eff[i] = new TGraph(50,trigger_Cut,EMTF_efficiency_special[i]); EMTF_eff[i]->SetMarkerStyle(21); EMTF_eff[i]->SetMarkerColor(1);//black
        C[i] = new TCanvas(Form("C%d",i),Form("Efficiency_%d",i),700,500);
        mg[i] = new TMultiGraph();
        C[i]->cd();
        mg[i]->SetTitle(Form("Mode 15 trigger efficiency pT > %.0f GeV",trigger_Cut_special[i]));
        mg[i]->Add(BDT_eff[i]);
        mg[i]->Add(EMTF_eff[i]);
        mg[i]->Draw();
        mg[i]->Write();
    }

    //================================================================================
    //Scale BDT(and EMTF) to 90%:
    //loop over true pT, for BDT, needs to rescale threshold X by multiply a factor[0,1]
    //to achieve 90% eff when true pT = X, these factors vary depend
    //on what the X is. Under each X, loop over change the scale factor; Under each
    //scale factor, loop over all test events to figure out how many pT > X*scale factor,
    //divide by total count in [bin X] to calculate the efficiency. If not close
    //to 90% eff cut, continue incresing BDT assigned pT scale factor until it closes.
    //================================================================================
    //scale factor of threshold of BDT assigned pT to achieve 90% efficiency,
    //it's between 0 and 1. It will be used in rate plot

    double EMTF_scale_Max=1.6;//2017 EMTF is mostly scaled to 90%
    double EMTF_scale_Min=0.6;
    double EMTF_scale[50]={0};
    double EMTF_pass_count_scaled[50][50]={0};
    double EMTF_efficiency_scaled[50][50]={0};
    double EMTF_efficiency_scale=0.90;
    double EMTF_scale_consistency[50]={0};
    TProfile* EMTF_scale_plot = new TProfile("EMTF_scale_plot","EMTF scale versus thresholds",49,1,50,0,2);
    TProfile* EMTF_scale_consistency_plot = new TProfile("EMTF_scale_consistency_plot","EMTF scale factor to 90% at thresholds",49,1,50,0,1);

    double BDT_scale_Max=1.0;
    double BDT_scale_Min=0.0;
    double BDT_scale[50]={0};
    double pass_count_scaled[50][50]={0};
    double efficiency_scaled[50][50]={0};
    double efficiency_scale=0.90;
    double BDT_scale_consistency[50]={0};
    TProfile* BDT_scale_plot = new TProfile("BDT_scale_plot","BDT scale versus thresholds",49,1,50,0,1);
    TProfile* BDT_scale_consistency_plot = new TProfile("BDT_scale_consistency_plot","BDT scale factor to 90% at thresholds",49,1,50,0,1);

    for(int Cut_bin=0;Cut_bin<50;Cut_bin++){

        double efficiency_tmp=0;
        double BDT_min=1.1;
        double BDT_scale_tmp=0;
        int flag=0;//stop loop over the scale for this bin when flag=1;

        double EMTF_efficiency_tmp=0;
        double EMTF_min=1.1;
        double EMTF_scale_tmp=0;
        int EMTF_flag=0;//stop loop over the scale for this bin when flag=1;

        for (int i=0; i<101; i++) {

            //initialize # BDT pT> X * this scale factor
            double pass_count_tmp=0;
            double EMTF_pass_count_tmp=0;
            if (flag == 1 && EMTF_flag == 1) break;

            //scale BDT assigned pT up to compare rate
            BDT_scale_tmp = BDT_scale_Max - i*(BDT_scale_Max-BDT_scale_Min)/100.0;
            EMTF_scale_tmp = EMTF_scale_Max - i*(EMTF_scale_Max-EMTF_scale_Min)/100.0;

            //==================================================
            //Enter test branch again to fix final scale
            //===================================================
            //std::cout << "\n******* Enter the test event loop for Cut bin: "<<Cut_bin<< "; Current scale: "<<BDT_scale_tmp<<" *******" << std::endl;
            for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++) {

            //  if ( (iEvt % 1) == 0 )
            //std::cout << "\n*** Looking at event " << iEvt << " ***" <<  std::endl;
                test_chain->GetEntry(iEvt);

                //need to specify events in this bin
                if (GEN_pt_test_br > GEN_pT[Cut_bin] && GEN_pt_test_br <= GEN_pT[Cut_bin+1]){
                    //BDT is targeting log2pT, need to convert
                    if (pow(2, BDT_test_br) > trigger_Cut[Cut_bin]*BDT_scale_tmp) {
                        pass_count_tmp++;
                    }//end if BDT
                    if (EMTF_pt_test_br > trigger_Cut[Cut_bin]*EMTF_scale_tmp){
                        EMTF_pass_count_tmp++;
                    }//end if EMTF
                }//end if

            }//End loop: for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++)
            //****Leaving the test event loop ****

            //calculate eff under this scale factor
            efficiency_tmp = pass_count_tmp/count[Cut_bin];
            EMTF_efficiency_tmp = EMTF_pass_count_tmp/count[Cut_bin];

            if (fabs(efficiency_tmp-efficiency_scale) < BDT_min) {
                BDT_min = fabs(efficiency_tmp-efficiency_scale);
                BDT_scale[Cut_bin] = BDT_scale_tmp;
                BDT_scale_consistency[Cut_bin] = efficiency_tmp;
                //if goes past the scale, stop loop over efficiency scale
                if(efficiency_tmp >= efficiency_scale){
                    flag=1;
                }//end if flag
            }//end if

            if (fabs(EMTF_efficiency_tmp-EMTF_efficiency_scale) < EMTF_min) {
                EMTF_min = fabs(EMTF_efficiency_tmp-EMTF_efficiency_scale);
                EMTF_scale[Cut_bin] = EMTF_scale_tmp;
                EMTF_scale_consistency[Cut_bin] = EMTF_efficiency_tmp;
                //if goes past the scale, stop loop over efficiency scale
                if(EMTF_efficiency_tmp >= EMTF_efficiency_scale){
                    EMTF_flag=1;
                }//end if EMTF flag
            }//end if

        }//end varying scale fac
        std::cout << "\n******* Leave the test event loop for Cut bin: "<<Cut_bin<< "; BDT scale: "<<BDT_scale[Cut_bin]<<"; EMTF scale: "<<EMTF_scale[Cut_bin]<<" *******" << std::endl;

        //see if all 90% at all trigger thresholds
        BDT_scale_consistency_plot->Fill(trigger_Cut[Cut_bin],BDT_scale_consistency[Cut_bin]);
        BDT_scale_plot->Fill(trigger_Cut[Cut_bin],BDT_scale[Cut_bin]);
        trigger_Cut_scaled[Cut_bin] = trigger_Cut[Cut_bin]*BDT_scale[Cut_bin];

        EMTF_scale_consistency_plot->Fill(trigger_Cut[Cut_bin],EMTF_scale_consistency[Cut_bin]);
        EMTF_scale_plot->Fill(trigger_Cut[Cut_bin],EMTF_scale[Cut_bin]);
        EMTF_trigger_Cut_scaled[Cut_bin] = trigger_Cut[Cut_bin]*EMTF_scale[Cut_bin];

    }//end loop over Cuts

    BDT_scale_plot->Write();
    BDT_scale_consistency_plot->Write();

    EMTF_scale_plot->Write();
    EMTF_scale_consistency_plot->Write();

    //====================================================
    //recount using the new BDT scaled threshold
    //====================================================
    std::cout << "\n******* Enter the test event loop to recount passing trigger events *******" << std::endl;
    for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++) {

        //  if (iEvt > 10) break;
        //  if ( (iEvt % 1) == 0 )
        //std::cout << "\n*** Looking at event " << iEvt << " ***" <<  std::endl;

        test_chain->GetEntry(iEvt);

        for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {

            if (GEN_pt_test_br > GEN_pT[Gen_bin] && GEN_pt_test_br <= GEN_pT[Gen_bin+1]){
            //deal with each cut
            for(int Cut_bin=0;Cut_bin<50;Cut_bin++){

                if (pow(2, BDT_test_br) > trigger_Cut_scaled[Cut_bin]) {//this scaled cut correspond to original trigger cut when plot 2d
                    pass_count_scaled[Cut_bin][Gen_bin]++;
                }//end if BDT
                if (EMTF_pt_test_br > EMTF_trigger_Cut_scaled[Cut_bin]){
                    EMTF_pass_count_scaled[Cut_bin][Gen_bin]++;
                }//end if EMTF

            }//end trigger cuts

        }//end if GEN_pt
        }//end Gen bin

    }// End loop: for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++)
    std::cout << "\n******* Finish recount, leaving the test event loop *******" << std::endl;

    //=========================================
    //calculate trigger efficiency after rescale
    //=========================================
    TProfile2D* BDT_trigger_Gen_efficiency_scaled = new TProfile2D("BDT_trigger_Gen_efficiency_scaled","BDT trigger efficiency versus thresholds and GEN pT SCALED",49,1,50,49,1,50,0,1);
    TProfile2D* EMTF_trigger_Gen_efficiency_scaled = new TProfile2D("EMTF_trigger_Gen_efficiency_scaled","EMTF trigger efficiency versus thresholds and GEN pT SCALED",49,1,50,49,1,50,0,1);

    //====================================================
    //check efficiency consistent for rate plot
    //====================================================
    double efficiency_threshold=0.90;
    double BDT_cuts[50]={0};
    double EMTF_cuts[50]={0};
    double BDT_efficiency_cuts[50]={0};
    double EMTF_efficiency_cuts[50]={0};
    TProfile* BDT_efficiency_cuts_consistency = new TProfile("BDT_efficiency_cuts_consistency","BDT cut efficiency versus GEN pT",49,1,50,0,1);
    TProfile* EMTF_efficiency_cuts_consistency = new TProfile("EMTF_efficiency_cuts_consistency","EMTF cut efficiency versus GEN pT",49,1,50,0,1);
    TProfile* BDT_cuts_vs_Gen_pT = new TProfile("BDT_cuts_vs_Gen_pT","BDT cuts versus GEN pT",49,1,50,0,50);
    TProfile* EMTF_cuts_vs_Gen_pT = new TProfile("EMTF_cuts_vs_Gen_pT","EMTF cuts versus GEN pT",49,1,50,0,50);


    for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {

        double BDT_min=1.1;//calculate the difference of EFF and each bin, find the closet to EFF
        double EMTF_min=1.1;

        for(int Cut_bin=0;Cut_bin<50;Cut_bin++){

            //BDT eff after scaled
            efficiency_scaled[Cut_bin][Gen_bin]=pass_count_scaled[Cut_bin][Gen_bin]/count[Gen_bin];
            EMTF_efficiency_scaled[Cut_bin][Gen_bin]=EMTF_pass_count_scaled[Cut_bin][Gen_bin]/count[Gen_bin];

            //===========================================================================
            //fill 2D profile, don't fill trigger cut scaled! fill original trigger cut!
            //===========================================================================
            BDT_trigger_Gen_efficiency_scaled->Fill(GEN_pT[Gen_bin],trigger_Cut[Cut_bin],efficiency_scaled[Cut_bin][Gen_bin]);
            EMTF_trigger_Gen_efficiency_scaled->Fill(GEN_pT[Gen_bin],trigger_Cut[Cut_bin],EMTF_efficiency_scaled[Cut_bin][Gen_bin]);

            if (fabs(efficiency_scaled[Cut_bin][Gen_bin]-efficiency_threshold)<BDT_min) {
                BDT_min = fabs(efficiency_scaled[Cut_bin][Gen_bin]-efficiency_threshold);
                BDT_cuts[Gen_bin] = trigger_Cut_scaled[Cut_bin];//need to multiply the corresponding scale factor, trigger_Cut_scaled[Cut_bin] = trigger_Cut[Cut_bin]*BDT_scale[Cut_bin];
                BDT_efficiency_cuts[Gen_bin] = efficiency_scaled[Cut_bin][Gen_bin];
            }//end if

            if (fabs(EMTF_efficiency_scaled[Cut_bin][Gen_bin]-efficiency_threshold)<EMTF_min) {
                EMTF_min = fabs(EMTF_efficiency_scaled[Cut_bin][Gen_bin]-efficiency_threshold);
                EMTF_cuts[Gen_bin] = EMTF_trigger_Cut_scaled[Cut_bin];
                EMTF_efficiency_cuts[Gen_bin] = EMTF_efficiency_scaled[Cut_bin][Gen_bin];
            }
        }//end Cut bin

    }//end Gen bin

    //fill 1D profile
    for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {
        BDT_efficiency_cuts_consistency->Fill(GEN_pT[Gen_bin],BDT_efficiency_cuts[Gen_bin]);
        EMTF_efficiency_cuts_consistency->Fill(GEN_pT[Gen_bin],EMTF_efficiency_cuts[Gen_bin]);
        BDT_cuts_vs_Gen_pT->Fill(GEN_pT[Gen_bin],BDT_cuts[Gen_bin]);
        EMTF_cuts_vs_Gen_pT->Fill(GEN_pT[Gen_bin],EMTF_cuts[Gen_bin]);
    }

    BDT_trigger_Gen_efficiency_scaled->Write();
    EMTF_trigger_Gen_efficiency_scaled->Write();

    //book graph for scaled special trigger efficiency
    TGraph *BDT_eff_scaled[special_cuts];
    TGraph *EMTF_eff_scaled[special_cuts];
    TCanvas *CScaled[special_cuts];
    TMultiGraph *mgScaled[special_cuts];
    double efficiency_special_scaled[3][50]={0};//BDT efficiency scaled to 90%
    double EMTF_efficiency_special_scaled[3][50]={0};//EMTF efficiency scaled to 90%
    for(Int_t i=0; i<special_cuts;i++){
      for (int Gen_bin=0;Gen_bin<50;Gen_bin++) {
        efficiency_special_scaled[i][Gen_bin]=efficiency_scaled[Int_t(trigger_Cut_special[i])-1][Gen_bin];
        EMTF_efficiency_special_scaled[i][Gen_bin]=EMTF_efficiency_scaled[Int_t(trigger_Cut_special[i])-1][Gen_bin];
      }
    }
    for(Int_t i=0; i<special_cuts;i++){
        BDT_eff_scaled[i] = new TGraph(50,trigger_Cut,efficiency_special_scaled[i]); BDT_eff_scaled[i]->SetMarkerStyle(21); BDT_eff_scaled[i]->SetMarkerColor(2);//red
        EMTF_eff_scaled[i] = new TGraph(50,trigger_Cut,EMTF_efficiency_special_scaled[i]); EMTF_eff_scaled[i]->SetMarkerStyle(21); EMTF_eff_scaled[i]->SetMarkerColor(1);//black
        CScaled[i] = new TCanvas(Form("CScaled%d",i),Form("Efficiency_%d",i),700,500);
        mgScaled[i] = new TMultiGraph();
        CScaled[i]->cd();
        mgScaled[i]->SetTitle(Form("Mode 15 trigger efficiency(scaled) pT > %.0f GeV",trigger_Cut_special[i]));
        mgScaled[i]->Add(BDT_eff_scaled[i]);
        mgScaled[i]->Add(EMTF_eff_scaled[i]);
        mgScaled[i]->Draw();
        mgScaled[i]->Write();
    }

    BDT_efficiency_cuts_consistency->Write();
    EMTF_efficiency_cuts_consistency->Write();
    BDT_cuts_vs_Gen_pT->Write();
    EMTF_cuts_vs_Gen_pT->Write();

    //===================================================
    //Enter test again for zero bias data to final rate plot
    //===================================================
    double rate_count[50]={0};
    double EMTF_rate_count[50]={0};

    std::cout << "\n******* Enter Zerobias test event to calculate rate *******" << std::endl;
    for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++) {

        test_chain->GetEntry(iEvt);

        //rate reduction using ZeroBias data in test sample: eta==-99,pt==999
        for (int Gen_bin =0;Gen_bin<50;Gen_bin++){
            if (GEN_pt_test_br == 999 && GEN_eta_test_br == -99){//both in zero bias
                if(pow(2, BDT_test_br) > BDT_cuts[Gen_bin]){
                    rate_count[Gen_bin]++;
                }
                if(EMTF_pt_test_br > EMTF_cuts[Gen_bin]){
                    EMTF_rate_count[Gen_bin]++;
                }
            }//end if Zerobias

        }//end for Gen_bin
    }// End loop: for (UInt_t iEvt = 0; iEvt < test_chain->GetEntries(); iEvt++)
    //std::cout << "\n******* Leaving the test event loop *******" << std::endl;

    //=========
    //rate plot
    //=========
    TGraph *BDT_rate = new TGraph(50,trigger_Cut,rate_count); BDT_rate->SetMarkerStyle(21); BDT_rate->SetMarkerColor(2);//red
    TGraph *EMTF_rate = new TGraph(50,trigger_Cut,EMTF_rate_count); EMTF_rate->SetMarkerStyle(21); EMTF_rate->SetMarkerColor(1);//black
    TCanvas *C_rate = new TCanvas("C_rate","Mode 15 rate",700,500);
    TMultiGraph *mg_rate = new TMultiGraph();
    C_rate->cd();
    mg_rate->SetTitle(Form("Mode 15 rate vs %.2f efficiency cut",efficiency_threshold));
    mg_rate->Add(BDT_rate);
    mg_rate->Add(EMTF_rate);
    mg_rate->Draw();
    mg_rate->Write();

    //==================
    //make log rate plot
    //==================
    double rate_count_log[50]={0};
    double EMTF_rate_count_log[50]={0};
    bool make_log_rate_plot = true;

    for (Int_t i=0;i<50;i++){
      if(rate_count[i]==0 || EMTF_rate_count[i]==0) make_log_rate_plot=false;
    };
    if(make_log_rate_plot){
      for (Int_t i=0;i<50;i++){rate_count_log[i] = log(rate_count[i])/log(10);};
      for (Int_t i=0;i<50;i++){EMTF_rate_count_log[i] = log(EMTF_rate_count[i])/log(10);};

      TGraph *BDT_rate_log = new TGraph(50,trigger_Cut,rate_count_log); BDT_rate_log->SetMarkerStyle(21); BDT_rate_log->SetMarkerColor(2);//red
      TGraph *EMTF_rate_log = new TGraph(50,trigger_Cut,EMTF_rate_count_log); EMTF_rate_log->SetMarkerStyle(21); EMTF_rate_log->SetMarkerColor(1);//black
      TCanvas *C_rate_log = new TCanvas("C_rate_log","Mode 15 log rate",700,500);
      TMultiGraph *mg_rate_log = new TMultiGraph();
      C_rate_log->cd();
      mg_rate_log->SetTitle(Form("Mode 15 log(rate)vs %.2f efficiency cut",efficiency_threshold));
      mg_rate_log->Add(BDT_rate_log);
      mg_rate_log->Add(EMTF_rate_log);
      mg_rate_log->Draw();
      mg_rate_log->Write();

      //==============
      //rate ratio plot
      //==============
      double rate_ratio[50]={0};
      for (Int_t i=0;i<50;i++){rate_ratio[i] = rate_count[i]/EMTF_rate_count[i];};
      TGraph *rate_ratio_plot = new TGraph(50,trigger_Cut,rate_ratio); rate_ratio_plot->SetMarkerStyle(21); rate_ratio_plot->SetMarkerColor(1);//black
      TCanvas *C_rate_ratio = new TCanvas("C_rate_ratio","Mode 15 rate ratio: BDT/EMTF",700,500);
      C_rate_ratio->cd();
      rate_ratio_plot->Draw();
      rate_ratio_plot->Write();
    }

} // End Macro
