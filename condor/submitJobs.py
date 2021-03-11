B#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
from optparse import OptionParser,OptionGroup
import getpass
import subprocess
from datetime import datetime
1;95;0c
def exec_me(command, dryRun=False):
    print command
    if not dryRun:
        os.system(command)

def write_condor(exe='condor_submit', outputlog = '', dryRun=True):
    fname = '%s.jdl' % exe
    out = """universe = vanilla
Executable = {exe}.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {exe}.sh
Output = {outputlog}/BDT_$(Cluster)_$(Process).stdout
Error = {outputlog}/BDT_$(Cluster)_$(Process).stderr
Log = {outputlog}/BDT_$(Cluster)_$(Process).log
request_memory = 10000
Queue
    """.format(exe=exe,outputlog=outputlog)
    with open(fname, 'w') as f:
        f.write(out)
    if not dryRun:
        os.system("condor_submit %s" % fname)

def write_bash(temp = 'runJob.sh', command = '', outputdirectory = '', USER='', CMSSW = "", SCRAM_ARCH = "", dryRun=True):

    ## 2: make run script
    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    ## get the tarball from EOS
    out += "xrdcp -s root://cmseos.fnal.gov//store/user/{user}/EMTFPtAssign2017Condor.tar.gz .\n".format(user=USER)
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
    out += "xrdcp -f Pt*.root root://cmseos.fnal.gov//store/user/{user}/{outdir}/\n".format(outdir=outputdirectory, user=USER)
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
    parser.add_option('--dryRun', dest='dryRun', action='store_true',default = False, help='write submission files only', metavar='dryRun')
    ## expert options
    parser.add_option("--isRun2", dest="isRun2", action="store_true", default = False)
    parser.add_option("--isRun3", dest="isRun3", action="store_true", default = False)
    parser.add_option("--useRPC", dest="useRPC", action="store_true", default = False)
    parser.add_option("--useQSBit", dest="useQSBit", action="store_true", default = False)
    parser.add_option("--useESBit", dest="useESBit", action="store_true", default = False)
    parser.add_option("--useSlopes", dest="useSlopes", action="store_true", default = False)
    parser.add_option("--useGEM", dest="useGEM", action="store_true", default = False)
    parser.add_option("--useL1Pt", dest="useL1Pt", action="store_true", default = False)
    parser.add_option("--useBitCompression", dest="useBitCompression", action="store_true", default = False)
    parser.add_option("--addDateTime", dest="addDateTime", action="store", default = True)
    (options, args) = parser.parse_args()

    if options.isRun2:
        options.useOneQuartPrecision = False
        options.useOneEighthPrecision = False
        options.useSlopes = False
        options.useGEM = False
        options.isRun3 = False

    ## if both isRun2 and isRun3 are set, pick isRun3!
    if options.isRun3:
        options.isRun2 = False

    ## if 1/8 strip precision is set, also 1/4 strip precision
    if options.useESBit:
        options.useQSBit = True

    ## GEM and RPC do not mix yet
    if options.useGEM:
        options.useRPC = False

    ## CMSSW version
    CMSSW = "CMSSW_11_2_0_pre9"
    SCRAM_ARCH = "slc7_amd64_gcc820"
    USER = getpass.getuser()
    tarball = "EMTFPtAssign2017Condor.tar.gz"

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
    if options.isRun2:      outputdirectory += "_isRun2"
    if options.isRun3:      outputdirectory += "_isRun3"
    if options.useRPC:      outputdirectory += "_useRPC"
    if options.useQSBit:    outputdirectory += "_useQSBit"
    if options.useESBit:    outputdirectory += "_useESBit"
    if options.useSlopes:   outputdirectory += "_useSlopes"
    if options.useGEM:      outputdirectory += "_useGEM"
    if options.addDateTime: outputdirectory += "_{}".format(currentDateTime)

    outputlog = outputdirectory.replace('Train','Log')

    print("command to run: ", command, "for user", USER)
    print("Using output directory {}".format(outputdirectory))

    ## 1: make a tarball of the directory
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    exec_me('''tar -pczf {cmssw}/src/tarball {cmssw}/src/EMTFPtAssign2017 \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/condor/" \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/macros/" \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/macros_Rice2020/"'''.format(cmssw=CMSSW_DIR, tarball=tarball), options.dryRun)

    ## 2: copy the tarball to EOS (if it does not exist yet)
    tarBallCode = os.system("eos root://cmseos.fnal.gov ls /store/user/{user}/{tarball}".format(user=USER, tarball=tarball))
    if tarBallCode != 0:
        exec_me('xrdcp {cmssw}/src/{tarball} root://cmseos.fnal.gov//store/user/{user}/'.format(cmssw=CMSSW_DIR, user=USER, tarball=tarball), options.dryRun)
    else:
        print("Tarball {tarball} exists already on EOS LPC!".format(tarball=tarball))

    ## 3: create the bash file
    exe = "runJob"
    write_bash(exe+".sh", command, outputdirectory, USER, CMSSW, SCRAM_ARCH, options.dryRun)

    ## 4: submit the job
    write_condor(exe, outputlog, options.dryRun)
