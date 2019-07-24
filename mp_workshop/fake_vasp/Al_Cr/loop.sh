#!/bin/bash
cur=$(pwd)
for fold in lau*
do
  cd $fold
  cd inputs
  n1=$(head -n1 POSCAR | sed 's/\ //g')
  n2=$(head -n3 POSCAR | tail -n1 | awk "{print  \$1}")
  name=$(printf '%s_%0.2f\n'  $n1 $n2)
  echo $name
  cd ..
  cd $cur
  cp -r $fold $name
done
