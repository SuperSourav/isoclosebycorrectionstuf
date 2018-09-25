#!/bin/bash
submitGridJobs.py --nFilesPerJob=1 --merge --useNewCode --oneOutDS --inDSTextFile samplelist_HIGG3D1_data16_R21.txt --doWH --writePAOD_WH --version V1;
submitGridJobs.py --nFilesPerJob=1 --merge --useNewCode --oneOutDS --inDSTextFile samplelist_HIGG3D1_data16_R21.txt --doWH --writePAOD_WH --version V1 --run;
