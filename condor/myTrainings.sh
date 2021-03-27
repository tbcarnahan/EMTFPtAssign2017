# 2021-03-27
# per Andrew's suggestion: start off with basic stuff
#  In terms of "sanity checks", here are a few suggestions:
#1) Run separate trainings for 2 separate |eta| regions, e.g. 1.2 < |eta| < 1.55 and 2.1 < |eta| 2.4.
#2) In these 2 regions, do a training with only 3 input variables: dPhi12, dPhi23, and dPhi34.

#If the "Run 3" training is still worse than the "Run 2" training in either of these 2 regions, then we can start looking directly at the dPhi correlation to charge / GEN pT.

#If "Run 3" is better, then start adding in variables (e.g. bend) until "Run 2" starts to pass it up, then look at that variable.

python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=1.2 --maxEta=1.55
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=1.2 --maxEta=1.55
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --minEta=1.2 --maxEta=1.55
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --useESBit --minEta=1.2 --maxEta=1.55
sleep 2


python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=2.1 --maxEta=2.4
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --minEta=2.1 --maxEta=2.4
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --minEta=2.1 --maxEta=2.4
sleep 2
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --useESBit --minEta=2.1 --maxEta=2.4
sleep 2
