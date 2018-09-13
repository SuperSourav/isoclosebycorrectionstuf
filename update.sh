#!/bin/bash
for d in $( ls -d Dir*/); do
  echo $d;
  ln -sf $PWD/SHARED/* $PWD/$d;
  ls -larth $d;
done

