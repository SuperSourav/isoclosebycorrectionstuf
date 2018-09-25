#!/bin/bash
localSetupPandaClient;
lsetup rucio;
voms-proxy-init -voms atlas;
source restart.sh;
