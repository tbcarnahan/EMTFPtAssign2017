#!/bin/bash

#You'll need to first compress your CMSSW release (with BDT code) into
#  a tarball and xrdcp it into eos. Point the next line to your tarball.
xrdcp -s root://cmseos.fnal.gov//store/user/mdecaro/EMTFPtAssign2017.tar .
source /cvmfs/cms.cern.ch/cmsset_default.sh
tar -xf EMTFPtAssign2017.tar
rm EMTFPtAssign2017.tar
cd CMSSW_10_6_1_patch2/src/
scramv1 b ProjectRename
eval `scramv1 runtime -sh`
echo $CMSSW_BASE
#cd ${_CONDOR_SCRATCH_DIR}
pwd
#cmsenv
cd EMTFPtAssign2017
root -l -b PtRegression2019_GEM_SD.C

#Specify the BDT output to a location on eos.
xrdcp -f Pt*.root root://cmseos.fnal.gov//store/user/mdecaro/condor_output_BDT/
rm Pt*.root
