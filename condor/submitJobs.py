#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
from optparse import OptionParser,OptionGroup

def exec_me(command, dryRun=False):
    print command
    if not dryRun:
        os.system(command)

def write_condor(njobs, exe='condor_submit', files = [], dryRun=True):
    fname = '%s.jdl' % exe
    out = """universe = vanilla
Executable = {exe}.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
Transfer_Input_Files = {exe}.sh,{files}
Output = {exe}.$(Process).$(Cluster).stdout
Error  = {exe}.$(Process).$(Cluster).stdout
Log    = {exe}.$(Process).$(Cluster).log
Arguments = $(Process) {njobs}
Queue {njobs}
    """.format(exe=exe, files=','.join(files), njobs=njobs)
    with open(fname, 'w') as f:
        f.write(out)
    if not dryRun:
        os.system("condor_submit %s" % fname)

def write_bash(temp = 'runjob.sh',  command = '',CMSSW="" ):
    out = '#!/bin/bash\n'
    out += 'date\n'
    out += 'MAINDIR=`pwd`\n'
    out += 'ls\n'
    #out += 'voms-proxy-info --all\n'
    out += '#CMSSW from scratch (only need for root)\n'
    out += 'export CWD=${PWD}\n'
    out += 'export PATH=${PATH}:/cvmfs/cms.cern.ch/common\n'
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
    with open(temp, 'w') as f:
        f.write(out)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--clean', dest='clean', action='store_true',default = False, help='clean submission files', metavar='clean')
    parser.add_option('--dryRun', dest='dryRun', action='store_true',default = False, help='write submission files only', metavar='dryRUn')
    parser.add_option('-o', '--odir', dest='odir', default='./', help='directory to write histograms/job output', metavar='odir')
    parser.add_option('-i', '--inputList', dest='inputList', default='./lists/test.txt', help='txt file for list of input', metavar='inputList')
    ## expert options
    parser.add_option("--isRun2", dest="isRun2", default = True)
    parser.add_option("--useRPC", dest="useRPC", default = True)
    parser.add_option("--useOneQuartPrecision", dest="useOneQuartPrecision", default = False)
    parser.add_option("--useOneEighthPrecision", dest="useOneEighthPrecision", default = False)
    parser.add_option("--useSlopes", dest="useSlopes", default = False)
    parser.add_option("--useGEM", dest="useGEM", default = False)
    parser.add_option("--useL1Pt", dest="useL1Pt", default = False)
    parser.add_option("--useBitCompression", dest="useBitCompression", default = False)
    (options, args) = parser.parse_args()

    CMSSW = "CMSSW_11_2_0_pre9"

    ##Small files used by the exe
    fileName = 'HeavyNeutralLepton_Tree.root'

    ##split input txt list
    command  = 'root -l -b -q "PtRegression2021.C(\"BDTG_AWB_Sq\", {}, {}, {}, {}, {}, {})"'.format(
        options.isRun2,
        options.useRPC,
        options.useOneQuartPrecision,
        options.useOneEighthPrecision,
        options.useSlopes,
        options.useGEM,
        options.useBitCompression,
        options.useL1Pt
    )

    print "command to run: ", command

    exe = "runjob"
    #write_bash(exe+".sh",  command, CMSSW)
    #write_condor(maxJobs, exe, , options.dryRun)
