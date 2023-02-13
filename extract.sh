#!/bin/bash

if [ $# != 4 ]
then
   echo "usage: " $@ " maxnumofthread maxrun"
   exit
fi

for numth in $(seq 1 $1)
do
  for n in  $(seq 1 $4)
  do
     grep "total fitted density" run_"$n"_"$numth".out  | tail -n 1
     grep "functional energy" run_"$n"_"$numth".out  | tail -n 1
     grep "vxc\[fit\]\*rho\[fit\] =" run_"$n"_"$numth".out  | tail -n 1
     grep "total energy =" run_"$n"_"$numth".out  | tail -n 1
     grep "convergence obtained in" run_"$n"_"$numth".out
  done
done
