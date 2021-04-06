#! /usr/bin/env python

##This file contains the Run-2 training variables for each mode
## the ordering of the variables here does not matter
Run2TrainingVariables = {

    ## 4-station tracks

    # BASELINE mode 15 - dPhi12/23/34 + combos, theta, FR1, St1 ring, dTh14, bend1, RPC 1/2/3/4
    '15' : [
        ['theta',3],
        ['St1_ring2',1],
        ['dPhi_12',7],
        ['dPhi_23',5],
        ['dPhi_34',4],
        ['dPhi_13',32],
        ['dPhi_14',32],
        ['dPhi_24',32],
        ['FR_1',1],
        ['bend_1',1],
        ['dPhiSum4',32],
        ['dPhiSum4A',32],
        ['dPhiSum3',32],
        ['dPhiSum3A',32],
        ['outStPhi',32],
        ['dTh_14',2],
        ['RPC_1',1],
        ['RPC_2',1],
        ['RPC_3',1],
        ['RPC_4',1],
    ],

    ## 3-station tracks

    # BASELINE mode 14 - dPhi12/23/13, theta, FR1/2, St1 ring, dTh13, bend1, RPC 1/2/3
    '14' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_12',7],
        ['dPhi_23',5],
        ['dPhi_13',32],
        ['FR_1',1],
        ['FR_2',1],
        ['bend_1',1],
        ['dTh_13',3],
        ['RPC_1',1],
        ['RPC_2',1],
        ['RPC_3',1],
    ],
    # BASELINE mode 13 - dPhi12/24/14, theta, FR1/2, St1 ring, dTh14, bend1, RPC 1/2/4
    '13' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_12',7],
        ['dPhi_14',5],
        ['dPhi_24',32],
        ['FR_1',1],
        ['FR_2',1],
        ['bend_1',1],
        ['dTh_14',3],
        ['RPC_1',1],
        ['RPC_2',1],
        ['RPC_4',1],
    ],
    # BASELINE mode 11 - dPhi13/34/14, theta, FR1/3, St1 ring, dTh14, bend1, RPC 1/3/4
    '11' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_34',7],
        ['dPhi_13',5],
        ['dPhi_14',32],
        ['FR_1',1],
        ['FR_3',1],
        ['bend_1',1],
        ['dTh_14',3],
        ['RPC_1',1],
        ['RPC_3',1],
        ['RPC_4',1],
    ],
    # BASELINE mode  7 - dPhi23/34/24, theta, FR2, dTh24, bend2, RPC 2/3/4
    '7' : [
        ['theta',5],
        ['dPhi_23',7],
        ['dPhi_34',5],
        ['dPhi_24',32],
        ['FR_2',1],
        ['bend_2',1],
        ['dTh_24',3],
        ['RPC_2',1],
        ['RPC_3',1],
        ['RPC_4',1],
    ],

    ## 2-station tracks

    # BASELINE mode 12 - dPhi12, theta, FR1/2, St1 ring, dTh12, bend1/2, RPC 1/2
    '12' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_12',7],
        ['FR_1',1],
        ['FR_2',1],
        ['bend_1',1],
        ['bend_2',1],
        ['dTh_12',3],
        ['RPC_1',1],
        ['RPC_2',1],
    ],
    # BASELINE mode 10 - dPhi13, theta, FR1/3, St1 ring, dTh13, bend1/3, RPC 1/3
    '10' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_13',7],
        ['FR_1',1],
        ['FR_3',1],
        ['bend_1',1],
        ['bend_3',1],
        ['dTh_13',3],
        ['RPC_1',1],
        ['RPC_3',1],
    ],
    # BASELINE mode  9 - dPhi14, theta, FR1/4, St1 ring, dTh14, bend1/4, RPC 1/4
    '9' : [
        ['theta',5],
        ['St1_ring2',1],
        ['dPhi_14',7],
        ['FR_1',1],
        ['FR_4',1],
        ['bend_1',1],
        ['bend_4',1],
        ['dTh_14',3],
        ['RPC_1',1],
        ['RPC_4',1],
    ],
    # BASELINE mode  6 - dPhi23, theta, FR2/3, dTh23, bend2/3, RPC 2/3
    '6' : [
        ['theta',5],
        ['dPhi_23',7],
        ['FR_2',1],
        ['FR_3',1],
        ['bend_2',2],
        ['bend_3',2],
        ['dTh_23',3],
        ['RPC_2',1],
        ['RPC_3',1],
    ],
    # BASELINE mode  5 - dPhi24, theta, FR2/4, dTh24, bend2/4, RPC 2/4
    '5' : [
        ['theta',5],
        ['dPhi_24',7],
        ['FR_2',1],
        ['FR_4',1],
        ['bend_2',2],
        ['bend_4',2],
        ['dTh_24',3],
        ['RPC_2',1],
        ['RPC_4',1],
    ],
    # BASELINE mode  3 - dPhi34, theta, FR3/4, dTh34, bend3/4, RPC 3/4
    '3' : [
        ['theta',5],
        ['dPhi_34',7],
        ['FR_3',1],
        ['FR_4',1],
        ['bend_3',2],
        ['bend_4',2],
        ['dTh_34',3],
        ['RPC_3',1],
        ['RPC_4',1],
    ],
    # Null track, for testing EMTF performance
    '0' : [
        ['theta',5],
        ['RPC_3',1],
        ['RPC_4',1],
    ],
}
