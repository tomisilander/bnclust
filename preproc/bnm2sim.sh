#!/bin/bash

dn=$1
dd=disdat/${dn}_V #directory for the data

rm -f $dd/vds.vd $dd/bnm.bnm
ln -s vds $dd/vds.vd
ln -s bnm $dd/bnm.bnm
source activate BN
python -m bn.infer.inout $dd/vds.vd $dd/bnm.bnm +$dd/ifr.ifr
python -m bn.util.fishim -m $dd/vds $dd/bnm $dd/ifr.ifr < $dd/dat > $dd/sim
source deactivate
mv $dd/sim ../data/${dn}_Bnsimx.txt

