#!/bin/bash

if [ $# != 4 ]
then
   echo "usage: " $@ " maxnumofthread modeltouse schedulingtouse maxrun"
   exit
fi

. /opt/intel/oneapi/setvars.sh 

ulimit -s unlimited

export OMP_SCHEDULE=$2
export BERTHA_DFINIT_MODEL=$3
export OMP_STACKSIZE=400M

for numth in $(seq 1 $1)
do
  export OMP_NUM_THREADS=$numth
  echo "Num. of Threads: " $OMP_NUM_THREADS
  for n in  $(seq 1 $4)
  do
     /usr/bin/time -v  ./bertha.serial 1> run_"$n".out 2> run_"$n".err
     grep "total fitted density" run_"$n".out  | tail -n 1
     grep "functional energy" run_"$n".out  | tail -n 1
     grep "vxc\[fit\]\*rho\[fit\] =" run_"$n".out  | tail -n 1
     grep "total energy =" run_"$n".out  | tail -n 1
     grep "convergence obtained in" run_"$n".out
     grep "Total time for iteration" run_"$n".err
     grep "Maximum resident set size (kbytes):" run_"$n".err
  done
done
