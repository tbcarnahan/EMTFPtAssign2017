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

def write_bash(temp = 'runJob.sh', tarball = '', command = '', outputdirectory = '', USER='', CMSSW = "", SCRAM_ARCH = "", dryRun=True):

    ## 2: make run script
    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    ## get the tarball from EOS
    out += "xrdcp -s root://cmseos.fnal.gov//store/user/{user}/{tarball} .\n".format(tarball=tarball, user=USER)
    ## unpack it
    out += "tar zxvf {tarball} .\n".format(tarball=tarball)
    out += "rm {tarball} .\n".format(tarball=tarball)
    ## setup CMSSW
    out += 'export CWD=${PWD}\n'
    out += "source /cvmfs/cms.cern.ch/cmsset_default.sh\n"
    out += 'echo "Setting up CMSSW:"\n'
    out += 'export SCRAM_ARCH={}\n'.format(SCRAM_ARCH)
    out += 'scramv1 project CMSSW {}\n'.format(CMSSW)
    out += 'cd {}/src/\n'.format(CMSSW)
    out += 'eval `scramv1 runtime -sh`\n'
    ## move EMTFPtAssign2017Condor to CMSSW/src/
    out += 'mv ../../{emtfworkdir} .\n'.format(emtfworkdir=tarball.replace('.tar.gz',''))
    ## move to directory and execute command
    out += 'cd {emtfworkdir}\n'.format(emtfworkdir=tarball.replace('.tar.gz',''))
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
    parser.add_option('--interactiveRun', dest='interactiveRun', action='store_true',default = False, help='do interactive run', metavar='dryRun')
    ## expert options
    parser.add_option("--isRun2", dest="isRun2", action="store_true", default = False)
    parser.add_option("--isRun3", dest="isRun3", action="store_true", default = False)
    parser.add_option("--useRPC", dest="useRPC", action="store_true", default = False)
    parser.add_option("--useQSBit", dest="useQSBit", action="store_true", default = False)
    parser.add_option("--useESBit", dest="useESBit", action="store_true", default = False)
    parser.add_option("--useSlopes", dest="useSlopes", action="store_true", default = False)
    parser.add_option("--useGEM", dest="useGEM", action="store_true", default = False)
    parser.add_option("--useL1Pt", dest="useL1Pt", action="store_true", default = False)
    parser.add_option("--useBitComp", dest="useBitComp", action="store_true", default = False)
    parser.add_option("--addDateTime", dest="addDateTime", action="store", default = True)
    (options, args) = parser.parse_args()

    # local variables
    dryRun = options.dryRun
    interactiveRun = options.interactiveRun
    isRun2 = options.isRun2
    isRun3 = options.isRun3
    useRPC = options.useRPC
    useQSBit = options.useQSBit
    useESBit = options.useESBit
    useSlopes = options.useSlopes
    useGEM = options.useGEM
    useL1Pt = options.useL1Pt
    useBitComp = options.useBitComp
    addDateTime = options.addDateTime

    if isRun2:
        useQSBit = False
        useESBit = False
        useSlopes = False
        useGEM = False
        isRun3 = False

    ## if both isRun2 and isRun3 are set, pick isRun3!
    if isRun3:
        isRun2 = False

    ## if 1/8 strip precision is set, also 1/4 strip precision
    if useESBit:
        useQSBit = True

    ## GEM and RPC do not mix yet
    if useGEM:
        useRPC = False

    ## CMSSW version
    CMSSW = subprocess.Popen("echo $CMSSW_VERSION", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    SCRAM_ARCH = subprocess.Popen("echo $SCRAM_ARCH", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    USER = getpass.getuser()
    currentDateTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    tarball = "EMTFPtAssign2017Condor_{}.tar.gz".format(currentDateTime)

    ## training command
    def runCommand(localdir = './'):
        command  = 'root -l -b -q "{localdir}PtRegressionRun3Prep.C({user}, {method}, {bisRun2}, {buseRPC}, {buseQSBit}, {buseESBit}, {buseSlopes}, {buseGEM})"'.format(
            user = '''\\\"{}\\\"'''.format(USER),
            method = '''\\\"BDTG_AWB_Sq\\\"''',
            bisRun2 = int(isRun2),
            buseRPC = int(useRPC),
            buseQSBit = int(useQSBit),
            buseESBit = int(useESBit),
            buseSlopes = int(useSlopes),
            buseGEM = int(useGEM),
            ## not considered yet
            buseBitComp = int(useBitComp),
            buseL1Pt = int(useL1Pt),
            localdir = localdir
        )
        return command

    command = runCommand()

    ## do interactive run?
    if interactiveRun:
        CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
        WORK_DIR = CMSSW_DIR + "/src/EMTFPtAssign2017/"
        command = runCommand('../')
        print(command)
        os.system(command)
        exit(1)

    ## name for output directory on EOS
    outputdirectory = "EMTF_BDT_Train"
    if isRun2:      outputdirectory += "_isRun2"
    if isRun3:      outputdirectory += "_isRun3"
    if useRPC:      outputdirectory += "_useRPC"
    if useQSBit:    outputdirectory += "_useQSBit"
    if useESBit:    outputdirectory += "_useESBit"
    if useSlopes:   outputdirectory += "_useSlopes"
    if useGEM:      outputdirectory += "_useGEM"
    if addDateTime: outputdirectory += "_{}".format(currentDateTime)

    outputlog = outputdirectory.replace('Train','Log')

    print("command to run: ", command, "for user", USER)
    print("Using output directory {}".format(outputdirectory))

    ## 0: make output directory
    exec_me('eos root://cmseos.fnal.gov mkdir /store/user/{user}/{outdir}'.format(user=USER, outdir=outputdirectory), dryRun)

    ## 1: make a tarball of the directory
    print("Making tarball")
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    exec_me('''tar -pczf {cmssw}/src/{tarball} {cmssw}/src/EMTFPtAssign2017 \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/condor/" \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/macros/" \
    --exclude \"{cmssw}/src/EMTFPtAssign2017/macros_Rice2020/"'''.format(cmssw=CMSSW_DIR, tarball=tarball), dryRun)

    ## 2: copy the tarball to EOS (if it does not exist yet)
    print("Copying tarball")
    tarBallCode = os.system("eos root://cmseos.fnal.gov ls /store/user/{user}/{tarball}".format(user=USER, tarball=tarball))
    if tarBallCode != 0:
        exec_me('xrdcp {cmssw}/src/{tarball} root://cmseos.fnal.gov//store/user/{user}/'.format(cmssw=CMSSW_DIR, user=USER, tarball=tarball), dryRun)
    else:
        print("..Tarball {tarball} exists already on EOS LPC!".format(tarball=tarball))

    ## 3: create the bash file
    print("Creating bash file")
    exe = "runJob"
    write_bash(exe+".sh", tarball, command, outputdirectory, USER, CMSSW, SCRAM_ARCH, dryRun)

    ## 4: submit the job
    print("Creating job file")
    write_condor(exe, outputlog, dryRun)
