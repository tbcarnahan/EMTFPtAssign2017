# Submit condor jobs in LPC

The `submitJobs.py` script submits the training script `PtRegressionRun3Prep.C` to LPC condor queue. For interactive run, add `--interactiveRun`


## Run-2 LCTs


### Default Run-2
```
python submitJobs.py --isRun2 --emtfMode=15
```

### Own selection
```
python submitJobs.py --isRun2 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34
```

## Run-3 LCTs: define your own selection (both mode and variables)!

Example:
```
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34
```

Example: with 1/4 strip
```
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit
```

Example: with 1/4 and 1/8 strip
```
python submitJobs.py --isRun3 --emtfMode=15 --trainVars dPhi_12 dPhi_23 dPhi_34 --useQSBit --useESBit
```
