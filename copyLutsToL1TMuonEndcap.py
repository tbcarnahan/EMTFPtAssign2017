#! /usr/bin/env python

import glob
import sys, commands, os, fnmatch
import argparse
import getpass
import subprocess
import xml.etree.ElementTree as ET

eospath = "/store/user/dildick/"
allowedModes = [15, 14, 13, 12, 11, 10, 9, 7, 6, 5, 3]
label = "Prep2018DataRate_eta1.25to2.4_isRun3"
label = "v0p"
xmlFileName = "f_logPtTarg_invPtWgt_BDTG_AWB_Sq.weights.xml"
tags = ['isRun3_bitComp', 'isRun3_useQS_bitComp', 'isRun3_useQS_useES_bitComp']
tags = ['isRun3_bitComp']
#dirs = ['v1p0', 'v1p1', 'v1p2']
dirs = ['v0p0', 'v0p1', 'v0p2']

cmssw_directory = subprocess.Popen("echo $CMSSW_BASE", shell=True, stdout=subprocess.PIPE).stdout.read().strip('\n')
target_directory = cmssw_directory + "/src/L1Trigger/L1TMuonEndCap/data/pt_xmls/"

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
                           "{}/{}/".format(target_directory, dirs[itag]) +
                           xmlFileName.replace('.weights.xml', '_mode{}.weights.xml'.format(mode)))
            print(exec_string)
            os.system(exec_string)

            #continue

            ## split up the XML in 400 separate XML files
            tree = ET.parse('{}/{}/f_logPtTarg_invPtWgt_BDTG_AWB_Sq_mode15.weights.xml'.format(target_directory, dirs[itag]))
            root = tree.getroot()
            weights= root.find('Weights')

            for itree in range(0,len(weights)):
                iweight = weights[itree]
                mydata = ET.tostring(iweight)
                myfile = open("{}/{}/{}/{}.xml".format(target_directory, dirs[itag], mode, itree), "w")
                myfile.write("""<?xml version="1.0"?>\n""")
                myfile.write(mydata)
                myfile.close()
                
