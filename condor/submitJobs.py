#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
import argparse
import getpass
import subprocess
from datetime import datetime
from commonVariables import *
from Run2Variables import *
from Run3Variables import *

def hasDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            return True
    return False

def trainVarsSelToHex(trainVariables):
    ## function to return hex string with train variables
    selectedVars = [0] * len(allowedTrainingVars)
    for p in trainVariables:
        if p in allowedTrainingVars:
            selectedVars[allowedTrainingVars.index(p)] = 1

    ## reverse the list
    selectedVars.reverse()
    ## contatenate and turn into a hex string
    selection = "".join([str(p) for p in selectedVars])
    hexsel = hex(int(selection, 2))
    return hexsel

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
Output = {outputlog}/$(Cluster)_$(Process).stdout
Error = {outputlog}/$(Cluster)_$(Process).stderr
Log = {outputlog}/$(Cluster)_$(Process).log
request_memory = 10000
Queue
    """.format(exe=exe,outputlog=outputlog)
    with open(fname, 'w') as f:
        f.write(out)
    if not dryRun:
        os.system("condor_submit %s" % fname)

def write_bash(temp = 'runJob.sh', tarball = '', command = '', outputdirectory = '', USER='', CMSSW = "", SCRAM_ARCH = "", dryRun=True):

    #emtfworkdir = tarball.replace('.tar.gz','')
    emtfworkdir = "EMTFPtAssign2017"

    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    out += 'echo "Copying tarball from EOS"\n'
    out += "xrdcp -s root://cmseos.fnal.gov//store/user/{user}/{tarball} .\n".format(tarball=tarball, user=USER)
    ## unpack it
    out += 'echo "Unpacking tarball \'tar -zxvf {tarball}\'"\n'.format(tarball=tarball)
    out += "tar -zxvf {tarball}\n".format(tarball=tarball)
    ## setup CMSSW
    out += 'export CWD=${PWD}\n'
    out += "source /cvmfs/cms.cern.ch/cmsset_default.sh\n"
    out += 'echo "Setting up CMSSW:"\n'
    out += 'export SCRAM_ARCH={}\n'.format(SCRAM_ARCH)
    out += 'scramv1 project CMSSW {}\n'.format(CMSSW)
    out += 'cd {}/src/\n'.format(CMSSW)
    out += 'eval `scramv1 runtime -sh`\n'
    ## move EMTFPtAssign2017Condor to CMSSW/src/
    out += 'echo "Moving {emtfworkdir} to $PWD"\n'.format(emtfworkdir=emtfworkdir)
    out += 'mv ../../{emtfworkdir} .\n'.format(emtfworkdir=emtfworkdir)
    ## move to directory and execute command
    out += 'cd {emtfworkdir}\n'.format(emtfworkdir=emtfworkdir)
    out += 'ls\n'
    out += command + '\n'
    ## copy the output to EOS
    out += "xrdcp -f Pt*.root root://cmseos.fnal.gov//store/user/{user}/{outdir}/\n".format(outdir=outputdirectory, user=USER)
    out += "xrdcp -r f_MODE* root://cmseos.fnal.gov//store/user/{user}/{outdir}/\n".format(outdir=outputdirectory, user=USER)
    out += 'echo "Removing tarball"\n'
    out += "rm {tarball}\n".format(tarball=tarball)
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

    ## expert options
    parser = argparse.ArgumentParser()
    parser.add_argument('--jobLabel', action='store',default='')
    parser.add_argument('--cleanTarBalls', action='store_true',default = False, help='Remove all tarballs.')
    parser.add_argument('--dryRun', action='store_true',default = False, help='write submission files only')
    parser.add_argument('--interactiveRun', action='store_true', default = False)
    parser.add_argument("--addDateTime", action="store", default = True)
    parser.add_argument('--trainVars',nargs='+', help='Set training variables. Required when Run3 is set', choices=allowedTrainingVars, default = [])
    parser.add_argument('--targetVar', action="store", help='Set target variable', default="log2(pt)")
    parser.add_argument("--isRun2", action="store_true", default = False)
    parser.add_argument("--isRun3", action="store_true", default = False)
    parser.add_argument("--isRun3Default", action="store_true", default = False)
    parser.add_argument("--useQSBit", action="store_true", default = False)
    parser.add_argument("--useESBit", action="store_true", default = False)
    parser.add_argument("--useBitComp", action="store_true", default = False)
    parser.add_argument("--emtfMode", action="store", default = 15)
    parser.add_argument("--minEta", action="store", default = 1.25)
    parser.add_argument("--maxEta", action="store", default = 2.4)
    parser.add_argument("--minPt", action="store", default = 1.)
    parser.add_argument("--maxPt", action="store", default = 1000.)
    parser.add_argument("--minPtTrain", action="store", default = 1.)
    parser.add_argument("--maxPtTrain", action="store", default = 256.)
    parser.add_argument("--nEvents", action="store", default = -1)
    parser.add_argument("--verbose", action="store_true", default = False)
    args = parser.parse_args()

    ## CMSSW version
    CWD = subprocess.Popen("echo $PWD", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    CMSSW = subprocess.Popen("echo $CMSSW_VERSION", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    SCRAM_ARCH = subprocess.Popen("echo $SCRAM_ARCH", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
    USER = getpass.getuser()

    if CMSSW not in CWD:
        sys.exit("Error: CMSSW environment variable has not been set! Exiting.")

    ## few checks
    if CMSSW == '' or CMSSW_DIR == '' or SCRAM_ARCH == '' or USER == '':
        sys.exit("Error: an environment variable has not been set! Exiting.")

    currentDateTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    tarball = "EMTFPtAssign2017Condor_{}.tar.gz".format(currentDateTime)

    if args.cleanTarBalls:
        print("Info: removing tarballs matching EMTFPtAssign2017Condor*.tar.gz")
        exec_me('rm {cmssw}/src/EMTFPtAssign2017/condor/EMTFPtAssign2017Condor*.tar.gz'.format(cmssw=CMSSW_DIR), args.dryRun)
        sys.exit()

    ## get the training variables
    trainVariables = args.trainVars

    ## check for duplicates
    if hasDuplicates(trainVariables):
        sys.exit("Error: training variable selection has duplicates. Exiting.")

    ## if no selection is provided for Run-2, use the default ones!
    if args.isRun2 and len(trainVariables) == 0:
        trainVariables = Run2TrainingVariables[args.emtfMode]
        print("Info: no training variable selection provided for Run-2 with mode {mode}. Using default selection.".format(mode = args.emtfMode))

    if args.isRun3 and len(trainVariables) == 0:
        sys.exit("Error: no training variable selection provided for Run-3 with mode {mode}. Exiting.".format(mode = args.emtfMode))

    if args.isRun3Default and len(trainVariables) == 0:
        args.isRun3 = True
        trainVariables = Run3TrainingVariables[args.emtfMode]
        print("Info: no training variable selection provided for Run-3 with mode {mode}. Using default selection.".format(mode = args.emtfMode))

    ## get the associated hex string for this selection
    trainVarsHex = trainVarsSelToHex(trainVariables)
    print("Info: Chosen training variables {0} -> {1}".format(trainVariables, trainVarsHex))
    print("Info: Chosen target variable(s): {}".format(args.targetVar))

    # local variables
    dryRun = args.dryRun
    interactiveRun = args.interactiveRun
    isRun2 = args.isRun2
    isRun3 = args.isRun3
    useQSBit = args.useQSBit
    useESBit = args.useESBit
    useBitComp = args.useBitComp
    addDateTime = args.addDateTime

    if isRun2:
        useQSBit = False
        useESBit = False
        isRun3 = False

    ## if both isRun2 and isRun3 are set, pick isRun3!
    if isRun3:
        isRun2 = False

    ## if 1/8 strip precision is set, also 1/4 strip precision
    if useESBit:
        useQSBit = True

    ## check if slopes are used
    useSlopes = any(item in trainVariables for item in ['slope_1', 'slope_2', 'slope_3', 'slope_4'])
    useBend = any(item in trainVariables for item in ['bend_1', 'bend_2', 'bend_3', 'bend_4'])

    ## cannot mix slope and bend
    if useSlopes and useBend:
        sys.exit("Error: cannot mix slope with bend training variables.")

    ## prefer dryRun over inveractiveRun
    if dryRun and interactiveRun:
        interactiveRun = False

    ## training command
    def runCommand(localdir = './'):
        command  = 'root -l -b -q "{localdir}PtRegressionRun3Prep.C({user}, {method}, {bemtfMode}, {minPt}, {maxPt}, {minPtTrain}, {maxPtTrain}, {minEta}, {maxEta}, {btrainVarsHex}, {btrainVarsSize}, {bisRun2}, {buseQSBit}, {buseESBit}, {buseBitComp}, {nEvents}, {verbose})"'.format(
            user = '''\\\"{}\\\"'''.format(USER),
            method = '''\\\"BDTG_AWB_Sq\\\"''',
            bemtfMode = int(args.emtfMode),
            minPt = float(args.minPt),
            maxPt = float(args.maxPt),
            minPtTrain = float(args.minPtTrain),
            maxPtTrain = float(args.maxPtTrain),
            minEta = float(args.minEta),
            maxEta = float(args.maxEta),
            btrainVarsHex = int(trainVarsHex, 16),
            btrainVarsSize = 0,
            bisRun2 = int(isRun2),
            buseQSBit = int(useQSBit),
            buseESBit = int(useESBit),
            buseBitComp = int(useBitComp),
            localdir = localdir,
            nEvents = int(args.nEvents),
            verbose = int(args.verbose)
        )
        return command

    command = runCommand()

    ## do interactive run?
    if interactiveRun:
        WORK_DIR = CMSSW_DIR + "/src/EMTFPtAssign2017/"
        command = runCommand('../')
        print(command)
        os.system(command)
        sys.exit()

    ## name for output directory on EOS
    outputdirectory = "EMTF_BDT_Train"
    outputdirectory += "_{}".format(args.jobLabel)
    outputdirectory += "_eta{}to{}".format(args.minEta, args.maxEta)
    if isRun2:      outputdirectory += "_isRun2"
    if isRun3:      outputdirectory += "_isRun3"
    if useQSBit:    outputdirectory += "_useQSBit"
    if useESBit:    outputdirectory += "_useESBit"
    outputdirectory += "_Selection{}".format(trainVarsHex)
    if addDateTime: outputdirectory += "_{}".format(currentDateTime)

    outputlog = outputdirectory.replace('Train','Log')
    os.system('mkdir {}'.format(outputlog))
    print("Info: command to run: ", command, "for user", USER)
    print("Info: using output directory {}".format(outputdirectory))

    ## 0: make output directory
    exec_me('eos root://cmseos.fnal.gov mkdir /store/user/{user}/{outdir}'.format(user=USER, outdir=outputdirectory), dryRun)

    ## 1: make a tarball of the directory
    print("Info: Making tarball")
    exec_me('''tar --exclude-vcs --exclude='EMTFPtAssign2017/*md' --exclude='EMTFPtAssign2017/macros_Rice2020/*'  --exclude='EMTFPtAssign2017/condor/*' --exclude='EMTFPtAssign2017/macros/*' -C {cmssw}/src/ -czvf {tarball} EMTFPtAssign2017 '''.format(cmssw=CMSSW_DIR, tarball=tarball), dryRun)
    tarBallCode = os.system("ls {cmssw}/src/EMTFPtAssign2017/condor/{tarball}".format(cmssw=CMSSW_DIR, tarball=tarball))
    if tarBallCode != 0:
        sys.exit("Error: tarball does not exist")

    ## 2: copy the tarball to EOS (if it does not exist yet)
    print("Info: Check if tarball exists.")
    tarBallCode = os.system("eos root://cmseos.fnal.gov ls /store/user/{user}/{tarball}".format(user=USER, tarball=tarball))
    if tarBallCode != 0:
        print("Info: Copying tarball")
        exec_me('xrdcp {cmssw}/src/EMTFPtAssign2017/condor/{tarball} root://cmseos.fnal.gov//store/user/{user}/'.format(cmssw=CMSSW_DIR, user=USER, tarball=tarball), dryRun)
        exec_me('rm {cmssw}/src/EMTFPtAssign2017/condor/{tarball}'.format(cmssw=CMSSW_DIR, tarball=tarball), dryRun)
    else:
        print("Warning: Tarball {tarball} exists already on EOS LPC!".format(tarball=tarball))

    ## 3: create the bash file
    print("Info: Creating bash file")
    exe = "runJob"
    write_bash(exe+".sh", tarball, command, outputdirectory, USER, CMSSW, SCRAM_ARCH, dryRun)

    ## 4: submit the job
    print("Info: Creating job file")
    write_condor(exe, outputlog, dryRun)
