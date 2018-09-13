#!/bin/bash
rundir=$PWD;
cd /afs/cern.ch/work/s/sosen/public/isocorrection;
setupATLAS;
cd build;
asetup --restore;
source */setup.sh;
cd ${rundir};
