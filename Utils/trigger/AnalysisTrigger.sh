#/bin/bash

#Setting BRICALC
source /cvmfs/cms-bril.cern.ch/cms-lumi-pog/brilws-docker/brilws-env

triggerlist=("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*" "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*" "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*" "HLT_IsoMu24_eta2p1_v*" "HLT_IsoMu24_v*" "HLT_IsoMu27_v*" "HLT_Mu18_Mu9_SameSign_v*" "HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v*" "HLT_BTagMu_AK8Jet300_Mu5_v*" "HLT_BTagMu_AK8DiJet170_Mu5_v*" "HLT_BTagMu_AK4Jet300_Mu5_v*" "HLT_BTagMu_AK4DiJet70_Mu5_v*" "HLT_BTagMu_AK4DiJet40_Mu5_v*" "HLT_BTagMu_AK4DiJet20_Mu5_v*" "HLT_BTagMu_AK4DiJet170_Mu5_v*" )

runlist=( "315257" "325172" )

for run in "${runlist[@]}"; do for trigger in "${triggerlist[@]}";
      do
         printf "\n\n\nRun: $run, Trigger: $trigger"
         brilcalc lumi -b "STABLE BEAMS" -i combined_RPIN_CMS_2018.json --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json --begin $run --end $run --hltpath $trigger -u /pb
         brilcalc trg -r $run --hltpath $trigger --prescale
      done;
done
