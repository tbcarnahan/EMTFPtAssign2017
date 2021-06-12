#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
import argparse
import getpass
import subprocess

eospath = "/store/user/dildick/"
allowedModes = [15, 14, 13, 12, 11, 10, 9, 7, 6, 5, 3]
label = "Prep2018DataRate_eta1.25to2.4_isRun3"
xmlFileName = "f_logPtTarg_invPtWgt_BDTG_AWB_Sq.weights.xml"
tags = ['isRun3_bitComp', 'isRun3_useQS_bitComp', 'isRun3_useQS_useES_bitComp']
dirs = ['v1p0', 'v1p1', 'v1p2']

CMSSW_DIR = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')

for mode in allowedModes:
    print(mode)

    for itag in range(0,len(tags)):
        eoscommand = ('''eos root://cmseos.fnal.gov ls /store/user/dildick | grep "EMTF_BDT_Train_Mode{}" | grep "{}" | grep "{}"'''.format(mode, label, tags[itag]))
        trainings = subprocess.Popen(eoscommand, shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
        splittrainings = trainings.split('\n')
        #print(trainings.split('\n'))

        for training in splittrainings:
            #print("eos root://cmseos.fnal.gov ls /store/user/dildick/" + training)
            exec_string = ("xrdcp /eos/uscms/store/user/dildick/" + training + "/" + xmlFileName + " " +
                           CMSSW_DIR + "/src/L1Trigger/L1TMuonEndCap/data/pt_xmls/{}/".format(dirs[itag]) +
                           xmlFileName.replace('.weights.xml', '_mode{}.weights.xml'.format(mode)))
            print(exec_string)
            os.system(exec_string)
