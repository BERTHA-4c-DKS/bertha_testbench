#!/bin/bash

if [ $# != 1 ]
then
   echo "usage: " $@ " numofthread"
   exit
fi

ulimit -s unlimited

export numth=$1

export OMP_STACKSIZE=400M
export OMP_NUM_THREADS=$numth
echo "Num. of Threads: " $OMP_NUM_THREADS

./bertha.serial 1> run_"$numth".out 2> run_"$numth".err
grep "total fitted density" run_"$numth".out  | tail -n 1
grep "functional energy" run_"$numth".out  | tail -n 1
grep "total analytical fitted density" run_"$numth".out  | tail -n 1
grep "total energy =" run_"$numth".out  | tail -n 1

rm -f fittcoeff.restart ovap.out fockmtx.txt vct.out 