#!/bin/bash
tmpfn=/tmp/$$.disdatcateg
echo Using temporarary file $tmpfn
while read dataname; do
	echo Processing $dataname '...'

	datafn=../Categorical/${dataname}_Vectors.txt

	python unify_csv.py $datafn $tmpfn
	resdir=disdat/${dataname}_V
	python -m pydida.dizo -d 011 -c '.. :: DIS NOM' -m '\?' -I GI -n GEN $tmpfn $resdir
	mv $resdir/dat ../data/${dataname}_Vectors.txt

	datafn=../Categorical/${dataname}_Labels.txt
	python unify_csv.py $datafn $tmpfn
	resdir=disdat/${dataname}_L
	python -m pydida.dizo -c '.. :: DIS NOM' -n GEN $tmpfn $resdir
	mv $resdir/dat ../data/${dataname}_Labels.txt
done
rm $tmpfn