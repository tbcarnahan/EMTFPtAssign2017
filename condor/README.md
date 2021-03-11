# Submit condor jobs in LPC

The `submitJobs.py` script submits the training script `PtRegression2021.C` to LPC condor queue


## Run-2 LCTs


### Run-2 with RPCs
```
python submitJobs.py --isRun2=True --useRPC=True
```

### Run-2 without RPCs
```
python submitJobs.py --isRun2=True --useRPC=False
```

### Run-2 with GEMs
```
python submitJobs.py --isRun2=True --useRPC=False --useGEM=True
```


## Run-3 LCTs


### Run-3 without resolution improvement
```
python submitJobs.py --isRun2=False --useRPC=False
```

### Run-3 with 1/4 strip
```
python submitJobs.py --isRun2=False --useRPC=False --useOneQuartPrecision=True
```

### Run-3 with 1/4 and 1/8 strip
```
python submitJobs.py --isRun2=False --useRPC=False --useOneQuartPrecision=True --useOneEighthPrecision=True
```

### Run-3 with 1/4 and 1/8 strip and slopes
```
python submitJobs.py --isRun2=False --useRPC=False --useOneQuartPrecision=True --useOneEighthPrecision=True --useSlopes=True
```

### Run-3 with 1/4 and 1/8 strip and slopes and GEMs
```
python submitJobs.py --isRun2=False --useRPC=False --useOneQuartPrecision=True --useOneEighthPrecision=True --useSlopes=True --useGEM=True
```
