#!/bin/bash

if [ $# != 3 ]
then
   echo "usage: " $@ " numofthread krgrid kagrid"
   exit
fi

ulimit -s unlimited

export numth=$1

export OMP_STACKSIZE=400M
export OMP_NUM_THREADS=$numth

export BERTHA_KRGRID=$2
export BERTHA_KAGRID=$3

echo "Num. of Threads: " $OMP_NUM_THREADS

./bertha.serial 1> run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out 2> run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".err
grep "total fitted density" run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out  | tail -n 1
grep "functional energy" run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out  | tail -n 1
grep "total analytical fitted density" run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out  | tail -n 1 
grep "convergence obtained in" run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out .out  | tail -n 1
grep "total energy =" run_"$numth"_"$BERTHA_KRGRID"_"$BERTHA_KAGRID".out  | tail -n 1

rm -f fittcoeff.restart ovap.out fockmtx.txt vct.out 
