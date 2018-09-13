#!/bin/bash
for f in $( ls file*); do
  setname=$(echo $f |cut -d "e" -f2);
  mkdir WHDir${setname};
  mv $f WHDir${setname};
  ln -s $PWD/SHARED/* $PWD/WHDir${setname}/;
  ls -larth WHDir${setname};
done
