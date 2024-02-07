#flake8: noqa

import sys
import os
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.Eras.Modifier_ctpps_2016_cff import ctpps_2016
from Configuration.Eras.Modifier_ctpps_2017_cff import ctpps_2017
from Configuration.Eras.Modifier_ctpps_2018_cff import ctpps_2018
from Configuration.ProcessModifiers.run2_miniAOD_UL_cff import run2_miniAOD_UL

# Setting Input Parameters from Line Command
options = VarParsing ('analysis')
options.register('physics','muon',VarParsing.multiplicity.singleton, VarParsing.varType.string,"physics(string): muon, electron, zerobias or emu. Default is muon.")
options.register('mode','data',VarParsing.multiplicity.singleton, VarParsing.varType.string,"mode(string): data or mc. Default is data.")
options.register('era','C',VarParsing.multiplicity.singleton, VarParsing.varType.string,"era(string): B, C, D, E or F.")
options.register('year','2018',VarParsing.multiplicity.singleton, VarParsing.varType.string,"year(string): 2017 or 2018. Default is 2017.")
options.register('prescale',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"prescale(bool): enable/disable trigger prescales values. Default is False (it works only for data).")
options.register('trigger',True,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"trigger(bool): enable/disable the trigger. Default is True.")
options.register('unmatching',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"unmatching(bool): \n\t\tTrue: leptons and jets not associated in the same cone.\n\t\tFalse: otherwise\n. Default is False.")
options.register('ppstagging',True,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"ppstagging(bool): \n\t\tTrue: selecting events with at least one proton per arm.\n\t\tFalse: no filter.\n. Default is True.")
options.register('antifilter',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"antifilter(bool): \n\t\tTrue: selecting events with 0 events per arm.\n\t\tFalse: no filter.\n. Default is True.")
options.register('reduced',True,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"reduced(bool): \n\t\tTrue: saving only protons, jets and vertex collections\t\tFalse: full ttree.\n. Default is True.")
options.register('debugging',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"debugging(bool): \n\t\tTrue: enabling skimmer debugger.\n\t\tFalse: otherwise\n. Default is False.")
options.parseArguments()

mc = False
if options.mode == "data":
  print("################")
  print("Running for Data")
  print("################")
  print("")
elif options.mode == "mc":
  print("#######################")
  print("Running for Monte Carlo")
  print("#######################")
  print("")
  mc = True
else:
  print("")
  print("################################")
  print("Please, try mode=data or mode=mc")
  print("################################")
  print("")
  os._exit(1)

if options.year != "2017" and options.year !="2018":
          print("\n Please, use only years 2017 or 2018!\n")
          os._exit(1)

if options.year == "2018" and options.mode =="zerobias":
          print("\n Please, zerobias is not yet configured to run over 2018 data!\n")
          os._exit(1)

if mc and (options.era == "B" or options.era == "D") and (options.year == "2018"):
  print("\n######################################################################")
  print("Era B or D does not exist for 2018 MC. Please, use era=B1,B2,D1 or D2.")
  print("######################################################################\n")
  print("")
  os._exit(1)

if mc and (options.era == "B1" or options.era == "B2" or options.era == "D1" or options.era == "D2") and (options.year == "2017"):
  print("\n########################################################################")
  print("Era B1, B2 or D1, D2 does not exist for 2017 MC. Please, use era=B or D.")
  print("########################################################################\n")
  print("")
  os._exit(1)

fileinput = ''
if mc:
 # Example of Pythia SD top dataset, 2017 conditions
 #fileinput = '/store/user/dmf/PYTHIA8-SD-TOP-MINIAOD-eraB-2017-withpps-13TEV/crab_dmf_2021-06-25_UTC09-48-16/PYTHIA8-SD-TOP-GEN/PYTHIA8-SD-TOP-MINIAOD-eraB-2017-withpps-13TEV/210625_074911/0000/output_101.root'
 #fileinput = '/store/user/dmf/PYTHIA8-SD-TOP-MINIAOD-eraD-2017-withpps-13TEV/crab_dmf_2021-07-12_UTC18-52-49/PYTHIA8-SD-TOP-GEN/PYTHIA8-SD-TOP-MINIAOD-eraD-2017-withpps-13TEV/210712_165318/0000/output_1.root'
 #fileinput = '/store/user/dmf/PYTHIA8-SD-TOP-MINIAOD-eraD-2017-withpps-13TEV/crab_dmf_2021-08-09_UTC16-52-30/PYTHIA8-SD-TOP-GEN/PYTHIA8-SD-TOP-MINIAOD-eraD-2017-withpps-13TEV_2021-08-09_UTC16-52-30/210809_145244/0000/output_138.root'
 #fileinput = '/store/user/dmf/PYTHIA8-SD-TOP-MINIAOD-eraA-2018-withpps-13TEV/crab_dmf_2023-05-31_UTC15-25-49/PYTHIA8-SD-TOP-PT60-2018-GEN-13TEV_2023-05-09_UTC11-26-52/PYTHIA8-SD-TOP-MINIAOD-eraA-2018-withpps-13TEV_2023-05-31_UTC15-25-49/230531_132617/0000/output_130.root'
 # Example of ToyMC for ZX analysis
 #fileinput = '/store/user/dmf/ZXToyMC-13TeV-miniAOD_2020-03-23_UTC13-55-30/ZXToyMC-GEN_Muon_PostTS2_950_150/ZXToyMC-13TeV-miniAOD_2020-03-23_UTC13-55-30/200323_125619/0000/output_14.root'
 #fileinput = '/store/user/dmf/ZXToyMC-13TeV-miniAOD_2020-03-23_UTC13-55-30/ZXToyMC-GEN_Muon_PostTS2_950_150/ZXToyMC-13TeV-miniAOD_2020-03-23_UTC13-55-30/200323_125619/0000/output_53.root'
 #fileinput = '/store/mc/RunIISummer20UL18MiniAODv2/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/00000/0381415E-3E93-1546-835C-4C73CD974231.root'
 fileinput = '/store/mc/RunIISummer20UL18MiniAODv2/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/2430000/70D2FC35-C0CC-2144-95BC-4EE05905AB1E.root'
else:
 # Example of 2017 data, era D, miniAOD, BTAG Stream
 #fileinput = '/store/data/Run2017D/BTagCSV/MINIAOD/09Aug2019_UL2017-v1/60000/CAEC3BF9-E990-AD41-A55B-B28269E242C1.root'
 # Example of 2018 data, era B, miniAOD, BTAG Stream
 #fileinput = '/store/data/Run2018B/BTagMu/MINIAOD/UL2018_MiniAODv2-v1/260000/05EC366B-3652-144D-A34F-356F0800C937.root'
 # Example of 2018 data, era C, miniAOD, DoubleMuon Stream
 fileinput = '/store/data/Run2018C/DoubleMuon/MINIAOD/ForValUL2018-v1/230000/1A9817AE-B1F4-A746-9460-34B48037B519.root'
 # Example of 2017 data, era A, miniAOD, ZeroBias Stream
 #fileinput='/store/data/Run2017A/ZeroBias2/RAW/v1/000/294/741/00000/1A36D36B-943E-E711-A0D7-02163E01A586.root'

#-----------------------------
# PPS Direct Sim, only for MC
#-----------------------------

if mc:
   if options.year == "2016" and (options.era == "B" or options.era == "C" or options.era == "G"):
      process = cms.Process('Analysis', ctpps_2016,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2016_preTS2_cff import *
   if options.year == "2016" and (options.era == "H"):
      process = cms.Process('Analysis', ctpps_2016,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2016_postTS2_cff import *
   if options.year == "2017" and (options.era == "B" or options.era == "C" or options.era == "D"):
      process = cms.Process('Analysis', ctpps_2017,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2017_preTS2_cff import *
   if options.year == "2017" and (options.era == "E" or options.era == "F"):
      process = cms.Process('Analysis', ctpps_2017,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2017_postTS2_cff import *
   if options.year == "2018" and (options.era == "A" or options.era == "B1"):
      process = cms.Process('Analysis', ctpps_2018,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2018_cff import *
   if options.year == "2018" and (options.era == "B2" or options.era == "C" or options.era == "D1"):
      process = cms.Process('Analysis', ctpps_2018,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2018_cff import *
   if options.year == "2018" and (options.era == "D2"):
      process = cms.Process('Analysis', ctpps_2018,run2_miniAOD_UL)
      from Validation.CTPPS.simu_config.year_2018_cff import *

   if options.year == "2016" and (options.era == "B" or options.era == "C" or options.era == "G"):
      process.load("Validation.CTPPS.simu_config.year_2016_preTS2_cff")
   if options.year == "2016" and (options.era == "H"):
      process.load("Validation.CTPPS.simu_config.year_2016_postTS2_cff")
   if options.year == "2017" and (options.era == "B" or options.era == "C" or options.era == "D"):
      process.load("Validation.CTPPS.simu_config.year_2017_preTS2_cff")
   if options.year == "2017" and (options.era == "E" or options.era == "F"):
      process.load("Validation.CTPPS.simu_config.year_2017_postTS2_cff")
   if options.year == "2018" and (options.era == "A" or options.era == "B1"):
      process.load("Validation.CTPPS.simu_config.year_2018_cff")
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.MisalignedFiles = ["PPSFramework/Skimmer/data/2018_preTS1.xml"]
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.RealFiles = ["PPSFramework/Skimmer/data/2018_preTS1.xml"]
   if options.year == "2018" and (options.era == "B2" or options.era == "C" or options.era == "D1"):
      process.load("Validation.CTPPS.simu_config.year_2018_cff")
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.MisalignedFiles = ["PPSFramework/Skimmer/data/2018_TS1_TS2.xml"]
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.RealFiles = ["PPSFramework/Skimmer/data/2018_TS1_TS2.xml"]
   if options.year == "2018" and (options.era == "D2"):
      process.load("Validation.CTPPS.simu_config.year_2018_cff")
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.MisalignedFiles = ["PPSFramework/Skimmer/data/2018_postTS2.xml"]
      process.ctppsRPAlignmentCorrectionsDataESSourceXML.RealFiles = ["PPSFramework/Skimmer/data/2018_postTS2.xml"]

   if options.year == "2017":
        process.load("CalibPPS.ESProducers.ctppsOpticalFunctions_cff")
   if options.year == "2018":
       process.load("CalibPPS.ESProducers.ctppsOpticalFunctions_cff") 

   process.load("CalibPPS.ESProducers.ctppsBeamParametersFromLHCInfoESSource_cfi")
   process.ctppsBeamParametersFromLHCInfoESSource.beamDivX45 = process.ctppsBeamParametersESSource.beamDivX45
   process.ctppsBeamParametersFromLHCInfoESSource.beamDivX56 = process.ctppsBeamParametersESSource.beamDivX56
   process.ctppsBeamParametersFromLHCInfoESSource.beamDivY45 = process.ctppsBeamParametersESSource.beamDivY45
   process.ctppsBeamParametersFromLHCInfoESSource.beamDivY56 = process.ctppsBeamParametersESSource.beamDivY56

   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX45 = process.ctppsBeamParametersESSource.vtxOffsetX45
   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetX56 = process.ctppsBeamParametersESSource.vtxOffsetX56
   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY45 = process.ctppsBeamParametersESSource.vtxOffsetY45
   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetY56 = process.ctppsBeamParametersESSource.vtxOffsetY56
   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ45 = process.ctppsBeamParametersESSource.vtxOffsetZ45
   process.ctppsBeamParametersFromLHCInfoESSource.vtxOffsetZ56 = process.ctppsBeamParametersESSource.vtxOffsetZ56

   process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevX = process.ctppsBeamParametersESSource.vtxStddevX
   process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevY = process.ctppsBeamParametersESSource.vtxStddevY
   process.ctppsBeamParametersFromLHCInfoESSource.vtxStddevZ = process.ctppsBeamParametersESSource.vtxStddevZ

   process.ctppsBeamParametersESSource.vtxStddevX = 0
   process.ctppsBeamParametersESSource.vtxStddevY = 0
   process.ctppsBeamParametersESSource.vtxStddevZ = 0

   process.load("CalibPPS.ESProducers.ctppsLHCInfoRandomXangleESSource_cfi")
   process.ctppsLHCInfoRandomXangleESSource.generateEveryNEvents = 1
   if options.year == "2016":
      process.ctppsBeamParametersESSource.vtxOffsetX45 = -1.048 * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetY45 = -1.686 * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetZ45 = +10.04 * 1E-1
      process.ctppsLHCInfoRandomXangleESSource.xangleHistogramFile = "CrossingAngles2016.root"
   if options.year == "2017":
      process.ctppsBeamParametersESSource.vtxOffsetX45 = +0.24793  * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetY45 = -0.692861 * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetZ45 = -7.89895  * 1E-1
      process.ctppsLHCInfoRandomXangleESSource.xangleHistogramFile = "CrossingAngles2017.root"
   if options.year == "2018":
      process.ctppsBeamParametersESSource.vtxOffsetX45 = -0.1078 * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetY45 = -0.4189 * 1E-1
      process.ctppsBeamParametersESSource.vtxOffsetZ45 = -0.2488 * 1E-1
      process.ctppsLHCInfoRandomXangleESSource.xangleHistogramFile = "CrossingAngles2018.root"

   process.ctppsLHCInfoRandomXangleESSource.xangleHistogramObject = "hxang"
   process.ctppsLHCInfoRandomXangleESSource.beamEnergy = 6500.
   process.ctppsLHCInfoRandomXangleESSource.betaStar = 0.40
   process.esPreferLHCInfo = cms.ESPrefer("CTPPSLHCInfoRandomXangleESSource", "ctppsLHCInfoRandomXangleESSource")

   process.beamDivergenceVtxGenerator.src = cms.InputTag("")
   process.beamDivergenceVtxGenerator.srcGenParticle = cms.VInputTag(
      cms.InputTag("prunedGenParticles")
   )

else:
   process = cms.Process("analysis")

#---------
# Triggers
#---------

if options.physics == "muon":
  print("")
  print("####")
  print("Muon")
  print("####")
  print("")
  if(options.year == "2017" or options.year == "2018"):
    triggerlist = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*','HLT_IsoMu24_eta2p1_v*','HLT_IsoMu24_v*','HLT_IsoMu27_v*','HLT_Mu18_Mu9_SameSign_v*','HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v*','HLT_BTagMu_AK8Jet300_Mu5_v*', 'HLT_BTagMu_AK8DiJet170_Mu5_v*','HLT_BTagMu_AK4Jet300_Mu5_v*','HLT_BTagMu_AK4DiJet70_Mu5_v*','HLT_BTagMu_AK4DiJet40_Mu5_v*','HLT_BTagMu_AK4DiJet20_Mu5_v*','HLT_BTagMu_AK4DiJet170_Mu5_v*','HLT_BTagMu_AK8Jet300_Mu5_noalgo_v*', 'HLT_BTagMu_AK8DiJet170_Mu5_noalgo_v*','HLT_BTagMu_AK4Jet300_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet70_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet40_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet20_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet170_Mu5_noalgo_v*'

elif options.physics == "bjet":
  print("")
  print("####")
  print("BJet")
  print("####")
  print("")
  if(options.year == "2017" or options.year == "2018"):
    triggerlist = 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*','HLT_IsoMu24_eta2p1_v*','HLT_IsoMu24_v*','HLT_IsoMu27_v*','HLT_Mu18_Mu9_SameSign_v*','HLT_Dimuon0_Upsilon_L1_4p5er2p0M_v*','HLT_BTagMu_AK8Jet300_Mu5_v*', 'HLT_BTagMu_AK8DiJet170_Mu5_v*','HLT_BTagMu_AK4Jet300_Mu5_v*','HLT_BTagMu_AK4DiJet70_Mu5_v*','HLT_BTagMu_AK4DiJet40_Mu5_v*','HLT_BTagMu_AK4DiJet20_Mu5_v*','HLT_BTagMu_AK4DiJet170_Mu5_v*','HLT_BTagMu_AK8Jet300_Mu5_noalgo_v*', 'HLT_BTagMu_AK8DiJet170_Mu5_noalgo_v*','HLT_BTagMu_AK4Jet300_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet70_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet40_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet20_Mu5_noalgo_v*','HLT_BTagMu_AK4DiJet170_Mu5_noalgo_v*'

elif options.physics == "electron":
  print("")
  print("########")
  print("Electron")
  print("########")
  print("")
  if(options.year == "2017" or options.year == "2018"):
    triggerlist = 'HLT_Ele27_WPTight_Gsf_v*', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_DoubleEle33_CaloIdL_MW_v*'
elif options.physics == "displacedjet":
  print("")
  print("##############")
  print("Displaced Jets")
  print("##############")
  print("")
  if(options.year == "2017"):
    print("\n Please, there is no displaced jets for 2017!\n")
    os._exit(1)
  if(options.year == "2018"):
    triggerlist='HLT_HT400_DisplacedDijet40_DisplacedTrack_v*','HLT_HT425_v*','HLT_HT430_DisplacedDijet40_DisplacedTrack_v*','HLT_HT430_DisplacedDijet60_DisplacedTrack_v*','HLT_HT500_DisplacedDijet40_DisplacedTrack_v*','HLT_HT550_DisplacedDijet60_Inclusive_v*','HLT_HT650_DisplacedDijet60_Inclusive_v*'
elif options.physics == "zerobias":
  print("")
  print("########")
  print("ZeroBias")
  print("########")
  print("")
  triggerlist = 'HLT_ZeroBias_v*', 'HLT_ZeroBias_FirstBXAfterTrain_v*','HLT_ZeroBias_IsolatedBunches_v*','HLT_ZeroBias_Alignment_v*','HLT_ZeroBias_Beamspot_v*','HLT_L1UnpairedBunchBptxMinus_v*','HLT_L1UnpairedBunchBptxPlus_v*','HLT_Physics_v*','HLT_L1SingleMu_v*'
elif options.physics == "emu":
  print("")
  print("###")
  print("EMu")
  print("###")
  print("")
  triggerlist = 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*', 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*'
else:
  print("")
  print("########################################################################################################")
  print("Please, try physics==muon or physics=electron or physics=zerobias or physics=emu")
  print("########################################################################################################")
  print("")
  os._exit(1)

if options.prescale:
  print("#################################")
  print("Including prescales in the Ntuple")
  print("#################################")
  print("")
else:
  print("#################################")
  print("_without_ prescales in the Ntuple")
  print("#################################")
  print("")

if options.trigger:
  print("################################")
  print("Including triggers in the Ntuple")
  print("################################")
  print("")
else:
  print("#################################")
  print("_without_ triggers in the Ntuple")
  print("#################################")
  print("")

if options.unmatching:
  print("#################################################################")
  print("leading leptons not associated with jets cone (unmatching = true)")
  print("#################################################################")
  print("")
else:
  print("##################################################################")
  print("leading leptons associated with the jets cone (unmatching = false)")
  print("##################################################################")
  print("")

if options.debugging:
  print("################")
  print("debugging active")
  print("################")
  print("")

if options.antifilter:
  print("################################")
  print("Including Anti-filter")
  print("################################")
  print("")
else:
  print("#################################")
  print("_without_ Anti-filter")
  print("#################################")
  print("")


#-----------------
# General options
#-----------------

process.load("FWCore.MessageService.MessageLogger_cfi")
process.options   = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True),
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

#-------------
# Input files    
#-------------
process.source = cms.Source("PoolSource",
				fileNames = cms.untracked.vstring(fileinput),
)

#----------
# Triggers       
#----------
process.load("PPSFramework.Skimmer.HLTFilter_cfi")
process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
process.hltFilter.HLTPaths = (triggerlist)

#-------------
# Preskimming      
#-------------
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag

if mc:
 if options.year=="2017":
  process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v17') # 94X MC campaing
 if options.year=="2018":
  # 106X_upgrade2018_realistic_v20
  process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v15_L1v1')
else:
 if options.year=="2017":
  process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v22') # global tag which includes PPS alignment and optics. Default: auto:run2_data
 if options.year=="2018":
  process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v32') # global tag which includes PPS alignment and optics. Default: auto:run2_data

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

#---------------
# Proton Filter     
#---------------
process.protontagFilter = cms.EDFilter("ProtonTagFilter",
					debugging = cms.bool(options.debugging),
                                        armMode = cms.string("double"),
					includeProtonsReco = cms.bool(True),
					includeProtonsMulti = cms.bool(True),
					includeAntiTagFilter = cms.bool(options.antifilter),
				        protonSingleTag = cms.InputTag("ctppsProtons", "singleRP"),
					protonMultiTag = cms.InputTag("ctppsProtons", "multiRP"),
					pixelsppsTag = cms.InputTag('ctppsPixelLocalTracks'),
					timingppsTag = cms.InputTag('ctppsDiamondLocalTracks'),
					stripstotemTag = cms.InputTag('totemRPLocalTrackFitter')
					)

#----------
# Analysis        
#----------
process.load("PPSFramework.Skimmer.countsAnalyzer_cfi")
process.CounterNoCuts = process.countsAnalyzer.clone()
process.CounterAfterTrigger = process.countsAnalyzer.clone()
process.CounterTriggered = process.countsAnalyzer.clone()
process.CounterPPSTagged = process.countsAnalyzer.clone()

process.load("PPSFramework.Skimmer.MissingMassSearches_cfi")
process.missing_mass.physics = cms.string(options.physics) 
process.missing_mass.year = cms.string(options.year) 
process.missing_mass.enableMC = cms.bool(mc)
process.missing_mass.enableTrigger = cms.bool(options.trigger)
process.missing_mass.enablePrescales = cms.bool(options.prescale)
process.missing_mass.unmatching = cms.bool(options.unmatching) #if True, force lepton/jets to be separated
process.missing_mass.reduced = cms.bool(options.reduced)
process.missing_mass.debugging = cms.bool(options.debugging)
process.missing_mass.includeMuons = cms.bool(True)
process.missing_mass.includeElectrons = cms.bool(True)
process.missing_mass.includeJets = cms.bool(True)
process.missing_mass.includePhotons = cms.bool(True)
process.missing_mass.includeMET = cms.bool(True)
process.missing_mass.includeVertices = cms.bool(True)
process.missing_mass.includeParticleFlow = cms.bool(True)
process.missing_mass.includeProtonsReco = cms.bool(True)
process.missing_mass.includePPSInfo = cms.bool(True)
process.missing_mass.triggersList = process.hltFilter.HLTPaths
process.missing_mass.l1tAlgBlkInputTag = cms.InputTag('gtStage2Digis')
process.missing_mass.l1tExtBlkInputTag = cms.InputTag('gtStage2Digis')
process.missing_mass.tier = cms.string('miniAOD')
process.missing_mass.ppslite = cms.bool(True)
process.missing_mass.GenPartTag = cms.InputTag('prunedGenParticles')
process.missing_mass.GenMETTag = cms.InputTag('genMetTrue')
process.missing_mass.GenJetAlgoA = cms.InputTag('slimmedGenJets')
process.missing_mass.GenJetAlgoB = cms.InputTag('slimmedGenJetsAK8')
process.missing_mass.patJetAlgoA = cms.InputTag('slimmedJets')
process.missing_mass.patJetAlgoB = cms.InputTag('slimmedJetsAK8')
process.missing_mass.electronTag = cms.InputTag("slimmedElectrons")
process.missing_mass.muonTag = cms.InputTag("slimmedMuons")
process.missing_mass.pfTag = cms.InputTag('particleFlow')
process.missing_mass.packedTag = cms.InputTag('packedPFCandidates')
process.missing_mass.photonTag = cms.InputTag('slimmedPhotons')
process.missing_mass.patmetTag = cms.InputTag('slimmedMETs')
process.missing_mass.vertexTag = cms.InputTag('offlineSlimmedPrimaryVertices')
process.missing_mass.protonTag = cms.InputTag('ctppsLocalTrackLiteProducer')
process.missing_mass.protonSingleTag = cms.InputTag("ctppsProtons", "singleRP")
process.missing_mass.protonMultiTag = cms.InputTag("ctppsProtons", "multiRP")
process.missing_mass.pixelsppsTag = cms.InputTag('ctppsPixelLocalTracks')
process.missing_mass.timingppsTag = cms.InputTag('ctppsDiamondLocalTracks')
process.missing_mass.stripstotemTag = cms.InputTag('totemRPLocalTrackFitter')
process.missing_mass.caloTowerTag = cms.InputTag('towerMaker')
process.missing_mass.lhcInfoLabel = cms.string('')

# b-tagging for RECO
process.load('RecoBTag/Configuration/RecoBTag_cff')
process.load("JetMETCorrections.Type1MET.correctedMet_cff")

# prepare the output file
process.TFileService = cms.Service('TFileService',
    fileName = cms.string("output.root"),
    closeFileFast = cms.untracked.bool(True)
)

process.MiniAOD = cms.Sequence(
                                        process.CounterNoCuts
                                        *process.hltFilter
                                        *process.CounterTriggered
                                        *process.protontagFilter
                                        *process.CounterPPSTagged
                                        *process.missing_mass
                                )

if mc:
   process.MiniAOD.insert(0, process.beamDivergenceVtxGenerator)
   process.MiniAOD.insert(1, process.ctppsDirectProtonSimulation)
   process.MiniAOD.insert(2, process.reco_local)
   process.MiniAOD.insert(3, process.ctppsProtons)

if not options.trigger:
   process.MiniAOD.remove(process.CounterTriggered)
   process.MiniAOD.remove(process.hltFilter)

if not options.ppstagging:
   process.MiniAOD.remove(process.CounterPPSTagged)
   process.MiniAOD.remove(process.protontagFilter)

process.p = cms.Path(process.MiniAOD)
