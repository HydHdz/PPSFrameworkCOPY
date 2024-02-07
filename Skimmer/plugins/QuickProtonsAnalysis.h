// -*- C++ -*-
//
// Package:    CTPPSAnalysisCode/QuickProtonsAnalysis
// Class:      QuickProtonsAnalysis
// 
/**\class QuickProtonsAnalysis QuickProtonsAnalysis.cc CTPPSAnalysisCode/QuickProtonsAnalysis/plugins/QuickProtonsAnalysis.cc

Description: [one line class summary]

Implementation:
[Notes on implementation]
*/
//
// Original Author:  Diego Figueiredo and Nicola Turini
//         Created:  Fri, 05 Oct 2018 09:08:27 GMT
//
//


// system include files
#include <memory>
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TProfile.h"
#include "TAxis.h"
#include <iostream>  
#include <typeinfo>
#include "TLorentzVector.h"

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "CondFormats/RunInfo/interface/LHCInfo.h"
#include "CondFormats/DataRecord/interface/LHCInfoRcd.h"

// HLT
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "HLTrigger/HLTcore/interface/HLTPrescaleProvider.h"

// CMS Calorimeters IDs
#include "DataFormats/HcalRecHit/interface/HcalRecHitCollections.h"
#include "DataFormats/HcalDetId/interface/HcalGenericDetId.h"
#include "DataFormats/HcalDetId/interface/HcalElectronicsId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/EcalDetId/interface/EcalTrigTowerDetId.h"
#include "DataFormats/EcalDetId/interface/EBDetId.h"
#include "CalibFormats/HcalObjects/interface/HcalCoderDb.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"

// Event
#include "TriggerEvent.h"
#include "JetsEvent.h"
#include "ElectronsEvent.h"
#include "MuonsEvent.h"
#include "PhotonsEvent.h"
#include "METEvent.h"
#include "ParticleFlowEvent.h"
#include "VerticesEvent.h"
#include "ProtonsEvent.h"
#include "GenProtonsEvent.h"
#include "GenParticlesEvent.h"
#include "GenMETEvent.h"
#include "GenJetsEvent.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"

//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class QuickProtonsAnalysis : public edm::one::EDAnalyzer<edm::one::SharedResources, edm::one::WatchRuns> {

  public:
    explicit QuickProtonsAnalysis(const edm::ParameterSet&);
    ~QuickProtonsAnalysis();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    virtual void beginJob() override;
    virtual void cleaning();
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endJob() override;
    void endRun(const edm::Run&, const edm::EventSetup&);
    void beginRun(const edm::Run&, const edm::EventSetup&);

    // Creating CMS Physics Object
    void fetchVertices(const edm::Event&, const edm::EventSetup&);
    void fetchPPSInfo(const edm::Event&, const edm::EventSetup&);
    void fetchLHCInfo(const edm::Event&, const edm::EventSetup&);
    void fetchProtonsReco(const edm::Event&, const edm::EventSetup&);
    bool fetchTrigger(const edm::Event&, const edm::EventSetup&);
    bool CheckBTag(const edm::Event& iEvent, const edm::EventSetup& iSetup);

    // ----------member data ---------------------------

    // Interface to the HLT information
    HLTPrescaleProvider hltPrescaleProvider_;

    // Switches
    edm::InputTag const& l1tAlgBlkInputTag;
    edm::InputTag const& l1tExtBlkInputTag;
    bool enableBtag_;
    bool debug_;
    std::string tier_;
    bool ppslite_;
    bool includeVertices_;
    bool includeProtonsReco_;
    bool includePPSInfo_;
    bool enableTrigger_;
    bool enablePrescales_;

    // Trigger
    std::vector<std::string> triggersList_;
    edm::EDGetTokenT<edm::TriggerResults> triggerResultsToken_;

    // Vertex
    edm::EDGetTokenT<edm::View<reco::Vertex> > vertexToken_;

    // Protons Lite
    edm::EDGetTokenT<std::vector<CTPPSLocalTrackLite> > protonToken_;

    // Protons Reco
    edm::EDGetTokenT<reco::ForwardProtonCollection > protonSingleToken_;
    edm::EDGetTokenT<reco::ForwardProtonCollection > protonMultiToken_;

    // Jets
    edm::EDGetTokenT<edm::View<pat::Jet> > patjetTokenA_;

    // PPS/TOTEM Detectors
    edm::EDGetTokenT<edm::DetSetVector<CTPPSPixelLocalTrack> > pixelsppsToken_;
    edm::EDGetTokenT<edm::DetSetVector<CTPPSDiamondLocalTrack> > timingppsToken_;
    edm::EDGetTokenT<edm::DetSetVector<TotemRPLocalTrack> > stripstotemToken_;

    //PileUpSummaryInfo 
    edm::EDGetTokenT<std::vector<PileupSummaryInfo>> puToken_;

    // LHC Info Label
    std::string lhcInfoLabel_;

    // Vectors with Collections
    std::vector<int> triggerVec;
    std::vector<int> prescalesL1Vec;
    std::vector<int> prescalesHLTVec;

    std::vector<const reco::Vertex*> vtxVec;
    std::vector<const CTPPSLocalTrackLite*> ppsVec;
    std::vector<const reco::ForwardProton*> protonSingleVec;
    std::vector<const reco::ForwardProton*> protonMultiVec;
    std::vector<const pat::Jet*> jetsVecA;
    std::vector<std::pair<const CTPPSPixelLocalTrack*, const CTPPSDetId>> pixelsVec;
    std::vector<std::pair<const CTPPSDiamondLocalTrack*, const CTPPSDetId>> timingVec;
    std::vector<std::pair<const TotemRPLocalTrack*, const CTPPSDetId>> stripsVec;

    // Cross-check histograms
    TH1F *hltTriggerNamesHisto_;
    TH1F *hXiRp210Arm45_;
    TH1F *hXiRp210Arm56_;
    TH1F *hXiRp220Arm45_;
    TH1F *hXiRp220Arm56_;
    TH1F *hXiMultiArm45_;
    TH1F *hXiMultiArm56_;

    TProfile *hProtonsMultiplicityMultiArm45_;
    TProfile *hProtonsMultiplicityMultiArm56_;
    TProfile *hProtonsMultiplicitySingleArm45_;
    TProfile *hProtonsMultiplicitySingleArm56_;

    TProfile *hInstLumi_;
    TProfile *hCrossingAngle_;
    TProfile *hBetaStar_;

    int nevents;

    // To be used with i.e. std::sort(v.begin(), v.end(), orderPT()), vector will be organized by pt.
    struct orderPt
    {
      template <class T, class W>
	inline bool operator() (T vec1, W vec2)
	{
	  return (vec1->pt() > vec2->pt());
	}
    };

    struct orderEta
    {
      template <class T, class W>
	inline bool operator() (T vec1, W vec2)
	{
	  return (vec1->eta() > vec2->eta());
	}
    };

    struct orderAbsolutPz
    {
      template <class T, class W>
	inline bool operator() (T vec1, W vec2)
	{
	  return (fabs(vec1->pz()) > fabs(vec2->pz()));
	}
    };

    struct orderVz
    {
      template <class T, class W>
	inline bool operator() (T vec1, W vec2)
	{
	  return (fabs(vec1->z()) > fabs(vec2->z()));
	}
    };

};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

