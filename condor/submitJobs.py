#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
from optparse import OptionParser,OptionGroup
import getpass
import subprocess
from datetime import datetime

def exec_me(command, dryRun=False):
    print command
    if not dryRun:
        os.system(command)

def write_condor(exe='condor_submit', dryRun=True):
    fname = '%s.jdl' % exe
    out = """universe = vanilla
Executable = {exe}.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {exe}.sh
Output = BDT_$(Cluster)_$(Process).stdout
Error = BDT_$(Cluster)_$(Process).stderr
Log = BDT_$(Cluster)_$(Process).log
request_memory = 10000
Queue
    """.format(exe=exe)
    with open(fname, 'w') as f:
        f.write(out)
    if not dryRun:
        os.system("condor_submit %s" % fname)

def write_bash(temp = 'runJob.sh', command = '', outputdirectory = '', CMSSW = "", SCRAM_ARCH = "", dryRun=True):

    ## 2: make run script
    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    ## get the tarball from EOS
    out += "xrdcp -s root://cmseos.fnal.gov//store/user/$USER/EMTFPtAssign2017Condor.tar.gz .\n"
    ## unpack it
    out += "tar zxvf EMTFPtAssign2017Condor.tar.gz .\n"
    out += "rm EMTFPtAssign2017Condor.tar.gz .\n"
    ## setup CMSSW
    out += 'export CWD=${PWD}\n'
    out += "source /cvmfs/cms.cern.ch/cmsset_default.sh\n"
    out += 'echo "Setting up CMSSW:"\n'
    out += 'export SCRAM_ARCH={}\n'.format(SCRAM_ARCH)
    out += 'scramv1 project CMSSW {}\n'.format(CMSSW)
    out += 'cd {}/src/\n'.format(CMSSW)
    out += 'eval `scramv1 runtime -sh`\n'
    ## move EMTFPtAssign2017Condor to CMSSW/src/
    out += 'mv ../../EMTFPtAssign2017Condor .\n'
    ## move to directory and execute command
    out += 'cd EMTFPtAssign2017Condor\n'
    out += 'ls\n'
    out += command + '\n'
    ## copy the output to EOS
    out += "xrdcp -f Pt*.root root://cmseos.fnal.gov//store/user/$USER/{}/\n".format(outputdirectory)
    ## cleanup
    out += 'cd $CWD\n'
    out += 'ls\n'
    out += 'echo "DELETING..."\n'
    out += 'rm -rf {}\n'.format(CMSSW)
    out += 'ls\n'
    out += 'date\n'

    with open(temp, 'w') as f:
        f.write(out)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--clean', dest='clean', action='store_true',default = False, help='clean submission files', metavar='clean')
    parser.add_option('--dryRun', dest='dryRun', action='store_true',default = True, help='write submission files only', metavar='dryRUn')
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

    if options.isRun2:
        options.useRPC = True
        options.useOneQuartPrecision = False
        options.useOneEighthPrecision = False
        options.useSlopes = False
        options.useGEM = False

    if options.useESBit:
        options.useQSBit = True

    if not options.isRun2 and options.useRPC and options.useGEM:
        options.useRPC = False

    ## CMSSW version
    CMSSW = "CMSSW_11_2_0_pre9"
    SCRAM_ARCH = "slc7_amd64_gcc820"

    ## training command
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

    ## name for output directory on EOS
    currentDateTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputdirectory = "EMTF_BDT_Train"
    if options.isRun2:
        outputdirectory += "_isRun2"
    if options.useRPC:
        outputdirectory += "_useRPC"
    if options.useQSBit:
        outputdirectory += "_useQSBit"
    if options.useESBit:
        outputdirectory += "_useESBit"
    if options.useSlopes:
        outputdirectory += "_useSlopes"
    if options.useGEM:
        outputdirectory += "_useGEM"
    outputdirectory += "_{}".format(currentDateTime)

    print("command to run: ", command, "for user", getpass.getuser())
    print("Using output directory {}".format(outputdirectory))
    ## 1: make a tarball of the directory
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    exec_me('''tar -pczf {0}/src/EMTFPtAssign2017Condor.tar.gz {0}/src/EMTFPtAssign2017 \
    --exclude \"{0}/src/EMTFPtAssign2017/condor/"  \
    --exclude \"{0}/src/EMTFPtAssign2017/macros/" \
    --exclude \"{0}/src/EMTFPtAssign2017/macros_Rice2020/"  '''.format(CMSSW_DIR), options.dryRun)

    ## 2: copy the tarball to EOS
    exec_me('xrdcp {0}/src/EMTFPtAssign2017Condor.tar.gz root://cmseos.fnal.gov//store/user/$USER/'.format(CMSSW_DIR), options.dryRun)

    ## 3: create the bash file
    exe = "runJob"
    write_bash(exe+".sh", command, outputdirectory, CMSSW, SCRAM_ARCH, options.dryRun)

    ## 4: submit the job
    write_condor(exe, options.dryRun)
