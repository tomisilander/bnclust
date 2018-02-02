#!/bin/bash

dn=$1
benedir=/home/tsilande/old-home/bene/bin
datadir=disdat/${dn}_V
resdir=/local/tmp/$dn

$benedir/data2net.sh $datadir/vds $datadir/dat qNML $resdir
cp $resdir/net $datadir
rm -fr $resdir


