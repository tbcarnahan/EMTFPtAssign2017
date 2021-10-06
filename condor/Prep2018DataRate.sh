allModes=(15 14 13 12 11 10 9 7 6 5 3)
versions=("--isRun2" "--isRun3" "--isRun3 --run3Version=v0" "--isRun3 --run3Version=v1")
bitcomp=("" "--useBitComp")

for imode in ${allModes[@]}; do
    #echo $imode
    for iversion in ${versions[@]}; do
        #echo $iversion
        for ibit in ${bitcomp[@]}; do
            #echo $iversion
            echo python submitJobs.py $iversion --emtfMode=$imode --jobLabel=Prep2018DataRate $ibit
        done
    done
done


## Run-2
#python submitJobs.py --isRun2 --emtfMode=15 --jobLabel=Prep2018DataRate
#sleep 60
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
sleep 60


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
sleep 60


## Run-3 V1.0
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=3 --jobLabel=Prep2018DataRate
sleep 60


## Run-3 V1.0 compressed
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp
sleep 60


## Run-3 V1.1
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=3 --jobLabel=Prep2018DataRate
sleep 60


## Run-3 V1.1 compressed
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp
sleep 60


## Run-3 V1.2
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=15 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=14 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=13 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=11 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=7 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=12 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=10 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=9 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=6 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=5 --jobLabel=Prep2018DataRate
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=3 --jobLabel=Prep2018DataRate
sleep 60


## Run-3 V1.2 compressed
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=15 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=14 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=13 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=11 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=7 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=12 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=10 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=9 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=6 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=5 --jobLabel=Prep2018DataRate --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v1 --useQSBit --useESBit --emtfMode=3 --jobLabel=Prep2018DataRate --useBitComp
sleep 60


## Run-3 V0.0
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=15 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=14 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=13 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=11 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=7 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=12 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=10 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=9 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=6 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=5 --jobLabel=v0p0
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=3 --jobLabel=v0p0
sleep 60


## Run-3 V0.0 compressed
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=15 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=14 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=13 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=11 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=7 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=12 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=10 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=9 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=6 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=5 --jobLabel=v0p0 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --emtfMode=3 --jobLabel=v0p0 --useBitComp
sleep 60


## Run-3 V0.1
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=15 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=14 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=13 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=11 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=7 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=12 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=10 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=9 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=6 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=5 --jobLabel=v0p1
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=3 --jobLabel=v0p1
sleep 60


## Run-3 V0.1 compressed
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=15 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=14 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=13 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=11 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=7 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=12 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=10 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=9 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=6 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=5 --jobLabel=v0p1 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --emtfMode=3 --jobLabel=v0p1 --useBitComp
sleep 60


## Run-3 V0.2
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=15 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=14 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=13 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=11 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=7 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=12 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=10 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=9 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=6 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=5 --jobLabel=v0p2
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=3 --jobLabel=v0p2
sleep 60


## Run-3 V0.2 compressed
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=15 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=14 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=13 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=11 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=7 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=12 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=10 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=9 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=6 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=5 --jobLabel=v0p2 --useBitComp
sleep 60
python submitJobs.py --isRun3 --run3Version=v0 --useQSBit --useESBit --emtfMode=3 --jobLabel=v0p2 --useBitComp
sleep 60
