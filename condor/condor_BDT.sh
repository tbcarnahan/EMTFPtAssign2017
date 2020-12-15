#!/bin/bash
xrdcp -s root://cmseos.fnal.gov//store/user/mdecaro/file.tar .
source /cvmfs/cms.cern.ch/cmsset_default.sh
tar -xf file.tar
rm file.tar
cd CMSSW_10_6_1_patch2/src/
scramv1 b ProjectRename
eval `scramv1 runtime -sh`
echo $CMSSW_BASE
#cd ${_CONDOR_SCRATCH_DIR}
pwd
#cmsenv
cd EMTFPtAssign2017
root -l -b PtRegression2019_GEM_SD.C

xrdcp -f Pt*.root root://cmseos.fnal.gov//store/user/mdecaro/condor_output_BDT/
rm Pt*.root
