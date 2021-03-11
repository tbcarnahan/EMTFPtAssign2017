#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
from optparse import OptionParser,OptionGroup
import getpass
import subprocess

def exec_me(command, dryRun=False):
    print command
    if not dryRun:
        os.system(command)

def write_condor(njobs, exe='condor_submit', dryRun=True):
    fname = '%s.jdl' % exe
    out = """universe = vanilla
Executable = {exe}.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {exe}.sh
Output = BDT_$(Cluster)_$(Process).stdout
Error = BDT_$(Cluster)_$(Process).stderr
Log = BDT_$(Cluster)_$(Process).log
Arguments = $(Process) {njobs}
request_memory = 10000
Queue
    """.format(exe=exe)
    with open(fname, 'w') as f:
        f.write(out)
    if not dryRun:
        os.system("condor_submit %s" % fname)

def write_bash(temp = 'runJob.sh', command = '', CMSSW = "", dryRun=True):

    USER_NAME = getpass.getuser()
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read()

    #exec_me('''tar -pczf EMTFPtAssign2017Condor.tar.gz {0}/src/EMTFPtAssign2017 --exclude \"{0}/src/EMTFPtAssign2017/condor/" '''.format(CMSSW_DIR), dryRun)
    ## 1: make a tarball of the directory

    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    out += '#CMSSW from scratch (only need for root)\n'
    out += 'export CWD=${PWD}\n'
    out += 'export PATH=${PATH}:/cvmfs/cms.cern.ch/common\n'
    out += 'echo "Setting up CMSSW:"\n'
    out += 'export SCRAM_ARCH=slc7_amd64_gcc700\n'
    out += 'scramv1 project CMSSW %s\n'%CMSSW
    ## move executable to folder
    out += 'mv %s %s/src\n'%(command.split()[0],CMSSW)
    ## move tar to folder
    out += 'mv corrections.tar.gz %s/src\n'%CMSSW
    ## move tar to folder
    out += 'mv JEC.tar.gz %s/src\n'%CMSSW
    out += 'cd %s/src\n'%CMSSW
    out += 'eval `scramv1 runtime -sh` # cmsenv\n'
    out += 'ls\n'
    out += command + '\n'
    out += 'echo "Inside $MAINDIR:"\n'
    out += 'ls\n'
    out += 'echo "DELETING..."\n'
    out += 'rm -rf %s\n'%CMSSW
    out += 'rm -rf *.pdf *.C core*\n'
    out += 'ls\n'
    out += 'date\n'

    """
    #You'll need to first compress your CMSSW release (with BDT code) into
    #  a tarball and xrdcp it into eos. Point the next line to your tarball.

    xrdcp -s root://cmseos.fnal.gov//store/user/$USER/EMTFPtAssign2017.tar .
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

    """

    with open(temp, 'w') as f:
        f.write(out)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--clean', dest='clean', action='store_true',default = False, help='clean submission files', metavar='clean')
    parser.add_option('--dryRun', dest='dryRun', action='store_true',default = False, help='write submission files only', metavar='dryRUn')
    parser.add_option('-o', '--odir', dest='odir', default='./', help='directory to write histograms/job output', metavar='odir')
    ## expert options
    parser.add_option("--isRun2", dest="isRun2", default = True)
    parser.add_option("--useRPC", dest="useRPC", default = True)
    parser.add_option("--useQSBit", dest="useQSBit", default = False)
    parser.add_option("--useESBit", dest="useESBit", default = False)
    parser.add_option("--useSlopes", dest="useSlopes", default = False)
    parser.add_option("--useGEM", dest="useGEM", default = False)
    parser.add_option("--useL1Pt", dest="useL1Pt", default = False)
    parser.add_option("--useBitCompression", dest="useBitCompression", default = False)
    (options, args) = parser.parse_args()

    CMSSW = "CMSSW_11_2_0_pre9"

    ##split input txt list
    command  = 'root -l -b -q "PtRegressionRun3Prep.C(\"BDTG_AWB_Sq\", {}, {}, {}, {}, {}, {})"'.format(
        options.isRun2,
        options.useRPC,
        options.useQSBit,
        options.useESBit,
        options.useSlopes,
        options.useGEM,
        options.useBitCompression,
        options.useL1Pt
    )

    print "command to run: ", command, "for user", getpass.getuser()

    exe = "runJob"
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    print CMSSW_DIR
    exec_me('''tar -pczf {0}/src/EMTFPtAssign2017Condor.tar.gz {0}/src/EMTFPtAssign2017 --exclude \"{0}/src/EMTFPtAssign2017/condor/"  --exclude \"{0}/src/EMTFPtAssign2017/macros/" --exclude \"{0}/src/EMTFPtAssign2017/macros_Rice2020/"  '''.format(CMSSW_DIR), True)
    #write_bash(exe+".sh", command, CMSSW)
    #write_condor(maxJobs, exe, options.dryRun)
