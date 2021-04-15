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


## check addition of slope1 (does not work, need difference in slope)
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --jobLabel=Test3DPhiSlope
sleep 60
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 slope_1 --jobLabel=Test3DPhiSlope
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
