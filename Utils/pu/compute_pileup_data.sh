#!/bin/sh
JSON_FILE=/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/DarkMatterSearch/2023/NTuplizer/CMSSW_10_6_17_patch1/src/PPSFramework/Skimmer/test/json_dpg/combined_RPIN_CMS_2018.json
PILEUP_FILE=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/PileUp/pileup_latest.txt
pileupCalc.py -i ${JSON_FILE} --inputLumiJSON ${PILEUP_FILE} --calcMode true --minBiasXsec 69200 --maxPileupBin 98 --numPileupBins 99 pileup_Collisions18_CMS_PPS.root
