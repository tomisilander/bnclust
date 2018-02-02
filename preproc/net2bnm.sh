#!/bin/bash

dn=$1
benedir=/home/tsilande/old-home/bene/bin
dd=disdat/${dn}_V #directory for the data

$benedir/net2bn.sh $dd/net > $dd/bn

source activate BN
python -m bn.util.bn_picture $dd/bn $dd/pic.jpg -f jpg
python -m bn.model.bnmodel $dd/vds $dd/bn $dd/dat $dd/bnm -t cnml
source deactivate
