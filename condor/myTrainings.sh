# 2021-03-27
# per Andrew's suggestion: start off with basic stuff
#  In terms of "sanity checks", here are a few suggestions:
#1) Run separate trainings for 2 separate |eta| regions, e.g. 1.2 < |eta| < 1.55 and 2.1 < |eta| 2.4.
#2) In these 2 regions, do a training with only 3 input variables: dPhi12, dPhi23, and dPhi34.

#If the "Run 3" training is still worse than the "Run 2" training in either of these 2 regions, then we can start looking directly at the dPhi correlation to charge / GEN pT.

#If "Run 3" is better, then start adding in variables (e.g. bend) until "Run 2" starts to pass it up, then look at that variable.

## test if the half-strip is working ok
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=1.2 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=1.2 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dSlope_12 --minEta=1.2 --maxEta=2.4 --jobLabel=Test3DPhi

'''
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=2.1 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=2.1 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --minEta=2.1 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --useESBit --minEta=2.1 --maxEta=2.4 --jobLabel=Test3DPhi
sleep 60


'''
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 slope_1 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dSlopeSum4A --jobLabel=Test3DPhiSlope
'''
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dSlope_12 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dSlope_12 dSlope_23 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dSlope_12 dSlope_23 dSlope_23 --jobLabel=Test3DPhiSlope

## check performance of all dphis
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dPhi_13 dPhi_14 dPhi_24 dPhiSum4 dPhiSum4A dPhiSum3 dPhiSum3A --jobLabel=TestAllDPhi
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 dPhi_13 dPhi_14 dPhi_24 dPhiSum4 dPhiSum4A dPhiSum3 dPhiSum3A --jobLabel=TestAllDPhi
'''

## Run-2
python submitJobs.py --isRun2 --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun2 --emtfMode=3 --jobLabel=Prep2018DataRate

## Run-2 compressed
python submitJobs.py --isRun2 --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun2 --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp


## Run-3 V1.0
python submitJobs.py --isRun3Default --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --emtfMode=3 --jobLabel=Prep2018DataRate

## Run-3 V1.0 compressed
python submitJobs.py --isRun3Default --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp





## Run-3 V1.1
python submitJobs.py --isRun3Default --useQSBit --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=3 --jobLabel=Prep2018DataRate

## Run-3 V1.1 compressed
python submitJobs.py --isRun3Default --useQSBit --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp



## Run-3 V1.2
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=3 --jobLabel=Prep2018DataRate

## Run-3 V1.2 compressed
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3Default --useQSBit --useESBit --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp
