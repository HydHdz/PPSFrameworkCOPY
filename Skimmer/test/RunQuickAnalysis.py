#flake8: noqa

import sys
import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.Eras.Modifier_ctpps_2016_cff import ctpps_2016
from Configuration.Eras.Modifier_ctpps_2017_cff import ctpps_2017
from Configuration.Eras.Modifier_ctpps_2018_cff import ctpps_2018
from Configuration.ProcessModifiers.run2_miniAOD_UL_cff import run2_miniAOD_UL

# Setting Input Parameters from Line Command
options = VarParsing ('analysis')
options.register('physics','muon',VarParsing.multiplicity.singleton, VarParsing.varType.string,"physics(string): muon, electron, zerobias or emu. Default is muon.")
options.register('year','2018',VarParsing.multiplicity.singleton, VarParsing.varType.string,"year(string): 2017 or 2018. Default is 2017.")
options.register('prescale',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"prescale(bool): enable/disable trigger prescales values. Default is False (it works only for data).")
options.register('trigger',True,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"trigger(bool): enable/disable the trigger. Default is True.")
options.register('debugging',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"debugging(bool): \n\t\tTrue: enabling skimmer debugger.\n\t\tFalse: otherwise\n. Default is False.")
options.register('enableBtag',False,VarParsing.multiplicity.singleton, VarParsing.varType.bool,"enableBtag(bool): \n\t\tTrue: leading and second leading jets with bTag evaluator < 0.2\n\t\tFalse: otherwise\n. Default is False.")
options.parseArguments()


# Example of 2018 data, era C, miniAOD, DoubleMuon Stream
#fileinput = '/store/data/Run2018C/DoubleMuon/MINIAOD/ForValUL2018-v1/230000/1A9817AE-B1F4-A746-9460-34B48037B519.root'
fileinput = '/store/data/Run2018A/ZeroBias/MINIAOD/UL2018_MiniAODv2-v1/00000/0BE26B44-5D30-1340-86F5-C27FD6D69526.root'

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
  if(options.year == "2017"):
    triggerlist = 'HLT_Ele27_WPTight_Gsf_v*', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v*', 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*', 'HLT_DoubleEle33_CaloIdL_MW_v*', 'HLT_BTagMu_AK4DiJet20_Mu5_v*', 'HLT_BTagMu_AK4DiJet40_Mu5_v*', 'HLT_BTagMu_AK4DiJet70_Mu5_v*', 'HLT_BTagMu_AK4DiJet110_Mu5_v*', 'HLT_BTagMu_AK4DiJet170_Mu5_v*', 'HLT_BTagMu_AK4Jet300_Mu5_v*', 'HLT_BTagMu_AK8DiJet170_Mu5_v*', 'HLT_BTagMu_AK8Jet300_Mu5_v*', 'HLT_PFHT380_SixJet32_DoubleBTagCSV_p075_v*', 'HLT_PFHT430_SixJet40_BTagCSV_p080_v*','HLT_PFMET100_PFMHT100_IDTight_CaloBTagCSV_3p1_v*', 'HLT_PFMET110_PFMHT110_IDTight_CaloBTagCSV_3p1_v*', 'HLT_PFMET120_PFMHT120_IDTight_CaloBTagCSV_3p1_v*', 'HLT_PFMET130_PFMHT130_IDTight_CaloBTagCSV_3p1_v*','HLT_PFMET140_PFMHT140_IDTight_CaloBTagCSV_3p1_v*', 'HLT_Ele15_IsoVVVL_PFHT450_CaloBTagCSV_4p5_v*', 'DST_HT250_CaloBTagScouting_v*','HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v*'
  if(options.year == "2018"):
    triggerlist = 'HLT_PFMET120_PFMHT120_IDTight_v*','HLT_Ele32_WPTight_Gsf_v*','HLT_IsoMu24_v*','HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v*','HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v*','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_v*','HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*'

elif options.physics == "displacedjet":
  print("")
  print("##############")
  print("Displaced Jets")
  print("##############")
  print("")
  if(options.year == "2017"):
    print("\n Please, there is no displaced jets for 2017!\n")
    sys.exit(0)
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
  sys.exit(0)

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

if options.debugging:
  print("################")
  print("debugging active")
  print("################")
  print("")

if options.enableBtag:
  print("#################")
  print("enableBtag active")
  print("#################")
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

if options.year=="2017":
 process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v22') # global tag which includes PPS alignment and optics. Default: auto:run2_data
if options.year=="2018":
 process.GlobalTag = GlobalTag(process.GlobalTag, '106X_dataRun2_v32') # global tag which includes PPS alignment and optics. Default: auto:run2_data

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")

#---------------
# Analyzer     
#---------------
process.QuickProtonsAnalysis = cms.EDAnalyzer("QuickProtonsAnalysis",
                          l1tAlgBlkInputTag = cms.InputTag('gtStage2Digis'),
                          l1tExtBlkInputTag = cms.InputTag('gtStage2Digis'),
                          enableBtag = cms.bool(options.enableBtag),
                          debugging = cms.bool(options.debugging),
                          tier = cms.string('miniAOD'),
                          ppslite = cms.bool(True),
                          includeProtonsReco = cms.bool(True),
                          includePPSInfo = cms.bool(True),
                          enableTrigger = cms.bool(options.trigger),
                          enablePrescales = cms.bool(True),
                          triggersList = process.hltFilter.HLTPaths,
                          triggerResults = cms.InputTag('TriggerResults', '', 'HLT'),
                          vertexTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
                          protonTag = cms.InputTag('ctppsLocalTrackLiteProducer'),
                          protonSingleTag = cms.InputTag("ctppsProtons", "singleRP"),
                          protonMultiTag = cms.InputTag("ctppsProtons", "multiRP"),
                          patJetAlgoA = cms.InputTag('slimmedJets'),
                          pixelsppsTag = cms.InputTag('ctppsPixelLocalTracks'),
                          timingppsTag = cms.InputTag('ctppsDiamondLocalTracks'),
                          stripstotemTag = cms.InputTag('totemRPLocalTrackFitter'),
                          lhcInfoLabel = cms.string('')
			)


# prepare the output file
process.TFileService = cms.Service('TFileService',
    fileName = cms.string("output.root"),
    closeFileFast = cms.untracked.bool(True)
)

process.MiniAOD = cms.Sequence(
                                        process.hltFilter
                                        *process.QuickProtonsAnalysis
                                )

if not options.trigger:
   process.MiniAOD.remove(process.hltFilter)

process.p = cms.Path(process.MiniAOD)
