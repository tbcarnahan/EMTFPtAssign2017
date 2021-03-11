# Submit condor jobs in LPC

The `submitJobs.py` script submits the training script `PtRegressionRun3Prep.C` to LPC condor queue. For interactive run, add `--interactiveRun`


## Run-2 LCTs


### Run-2 with RPCs
```
python submitJobs.py --isRun2 --useRPC
```

### Run-2 without RPCs
```
python submitJobs.py --isRun2
```

### Run-2 with GEMs (GEMs and RPCs don't mix yet)
```
python submitJobs.py --isRun2 --useGEM
```


## Run-3 LCTs


### Run-3 without resolution improvement
```
python submitJobs.py --isRun3
```

### Run-3 with 1/4 strip
```
python submitJobs.py --isRun3 --useQSBit
```

### Run-3 with 1/4 and 1/8 strip
```
python submitJobs.py --isRun3 --useQSBit --useESBit
```

### Run-3 with 1/4 and 1/8 strip and slopes
```
python submitJobs.py --isRun3 --useQSBit --useESBit --useSlopes
```

### Run-3 with 1/4 and 1/8 strip and slopes and GEMs
```
python submitJobs.py --isRun3 --useQSBit --useESBit --useSlopes --useGEM
```
