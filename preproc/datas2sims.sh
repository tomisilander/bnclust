#!/bin/bash
while read dn; do
    echo processing $dn '...'
    ./data2net.sh $dn
    ./net2bnm.sh $dn
    ./bnm2sim.sh $dn
done