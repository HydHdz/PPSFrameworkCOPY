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
// Original Authors:  Diego Figueiredo, Lorenzo Pagliai and Nicola Turini
//          Created:  Fri, 05 Oct 2018 09:08:27 GMT
//
//

// user include files
#include "QuickProtonsAnalysis.h"

//
// constructors and destructor
//
QuickProtonsAnalysis::QuickProtonsAnalysis(const edm::ParameterSet& iConfig):
  hltPrescaleProvider_ ( iConfig, consumesCollector(), *this),
  l1tAlgBlkInputTag    ( iConfig.getParameter<edm::InputTag>              ( "l1tAlgBlkInputTag" ) ),
  l1tExtBlkInputTag    ( iConfig.getParameter<edm::InputTag>              ( "l1tExtBlkInputTag" ) ),
  enableBtag_          ( iConfig.getParameter<bool>( "enableBtag" ) ),
  debug_               ( iConfig.getParameter<bool>( "debugging" ) ),
  tier_                ( iConfig.getParameter<std::string>( "tier" ) ),
  ppslite_             ( iConfig.getParameter<bool>( "ppslite" ) ),
  includeProtonsReco_      ( iConfig.getParameter<bool>( "includeProtonsReco" ) ),
  includePPSInfo_      ( iConfig.getParameter<bool>( "includePPSInfo" ) ),
  enableTrigger_            ( iConfig.getParameter<bool>( "enableTrigger" ) ),
  enablePrescales_            ( iConfig.getParameter<bool>( "enablePrescales" ) ),
  triggersList_        ( iConfig.getParameter<std::vector<std::string>>              ( "triggersList" ) ),
  triggerResultsToken_ ( consumes<edm::TriggerResults>                               ( iConfig.getParameter<edm::InputTag>( "triggerResults" ) ) ),
  vertexToken_         ( consumes<edm::View<reco::Vertex>>                           ( iConfig.getParameter<edm::InputTag>( "vertexTag" ) ) ),
  protonToken_         ( consumes<std::vector<CTPPSLocalTrackLite>>                  ( iConfig.getParameter<edm::InputTag>( "protonTag" ) ) ),
  protonSingleToken_   ( consumes<reco::ForwardProtonCollection>                     ( iConfig.getParameter<edm::InputTag>( "protonSingleTag" ) ) ),
  protonMultiToken_    ( consumes<reco::ForwardProtonCollection>                     ( iConfig.getParameter<edm::InputTag>( "protonMultiTag" ) ) ),
  patjetTokenA_        ( consumes<edm::View<pat::Jet>>                               ( iConfig.getParameter<edm::InputTag>( "patJetAlgoA" ) ) ),
  pixelsppsToken_      ( consumes<edm::DetSetVector<CTPPSPixelLocalTrack>>           ( iConfig.getParameter<edm::InputTag>( "pixelsppsTag" ) ) ),
  timingppsToken_      ( consumes<edm::DetSetVector<CTPPSDiamondLocalTrack>>         ( iConfig.getParameter<edm::InputTag>( "timingppsTag" ) ) ),
  stripstotemToken_    ( consumes<edm::DetSetVector<TotemRPLocalTrack>>              ( iConfig.getParameter<edm::InputTag>( "stripstotemTag" ) ) ),
  puToken_             ( consumes<std::vector<PileupSummaryInfo>>                    (edm::InputTag("slimmedAddPileupInfo"))),
  lhcInfoLabel_        ( iConfig.getParameter<std::string>("lhcInfoLabel"))         
{

  //now do what ever initialization is needed
  usesResource("TFileService");
  std::cout<<"\n<CMSSW Plugin> Missing Mass Skimmer..." << std::endl;
  std::cout<<"\t-->Enable Trigger: " << enableTrigger_ <<  std::endl;
  std::cout<<"\t-->Enable Prescale: " << enablePrescales_ <<  std::endl;
  std::cout<<"\t-->Debug: " << debug_ <<  std::endl;              
  std::cout<<"\t-->Forward Proton Reco: " << includeProtonsReco_ <<  std::endl;              
  std::cout<<"\t-->PPS Info: " << includePPSInfo_ <<  std::endl;              
  std::cout<<"\t-->PPS Lite: " << ppslite_ <<  std::endl;

}

QuickProtonsAnalysis::~QuickProtonsAnalysis()
{

  // do anything here that needs to be done at desctruction time
  // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//


// ------------ Cleaning  ------------
void QuickProtonsAnalysis::cleaning(){

  triggerVec.clear();
  vtxVec.clear();
  ppsVec.clear();
  protonSingleVec.clear();
  protonMultiVec.clear();
  jetsVecA.clear();
  pixelsVec.clear();
  timingVec.clear();
  stripsVec.clear();

}

// ------------ running over vertices  ------------
void QuickProtonsAnalysis::fetchVertices(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  VerticesEvent *vtx;
  vtx = new VerticesEvent(iEvent, iSetup, vertexToken_);
  vtxVec = vtx->GetVertices();

  if(debug_){
    for ( const auto& vtxEvt: vtxVec){
      std::cout << "Vtx (x, y, z): " << vtxEvt->x() << ", "<< vtxEvt->y() << ", " << vtxEvt->z() << std::endl;
      std::cout << "Number of tracks per vtx: " << vtxEvt->nTracks() << std::endl;
      std::cout << "Chi2: " << vtxEvt->chi2() << std::endl;
      std::cout << "ndof: " << vtxEvt->ndof() << std::endl;
    }
  }

}


// ------------ fetching over LHC info ----------------
void QuickProtonsAnalysis::fetchLHCInfo(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::ESHandle<LHCInfo> hLHCInfo;
  iSetup.get<LHCInfoRcd>().get(lhcInfoLabel_, hLHCInfo);

  if(debug_){
    std::cout << "Colliding bunches: " << hLHCInfo->collidingBunches() << std::endl;
    std::cout << "# bunches Beam1: " << hLHCInfo->bunchesInBeam1() << std::endl;
    std::cout << "# bunches Beam2: " << hLHCInfo->bunchesInBeam2() << std::endl;
    std::cout << "Intensity beam1: " << hLHCInfo->intensityForBeam1() << std::endl;
    std::cout << "Intensity beam2: " << hLHCInfo->intensityForBeam2() << std::endl;
    std::cout << "Inst. Luminosity: " << hLHCInfo->instLumi() << std::endl;
    std::cout << "XAngle (LHC) [murad]: " << hLHCInfo->crossingAngle() << std::endl;
    std::cout << "Beta Star: " << hLHCInfo->betaStar() << std::endl;
  }

  hInstLumi_ -> Fill(iEvent.luminosityBlock(), hLHCInfo->instLumi());
  hCrossingAngle_ ->Fill(iEvent.luminosityBlock(), hLHCInfo->crossingAngle());
  hBetaStar_ -> Fill(iEvent.luminosityBlock(), hLHCInfo->betaStar());


}

// ------------ running over Jets  ------------
bool QuickProtonsAnalysis::CheckBTag(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  bool check = false;

  JetsEvent *jetAlgoA;
  jetAlgoA = new JetsEvent(iEvent, iSetup, patjetTokenA_);
  jetsVecA = jetAlgoA->GetJets();

  if(jetsVecA.size()>1){
    if((jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probbb") > 0) && (jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probbb")<0.2) && (jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probbb") > 0) && (jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probbb")<0.2)){
      check = true;
      if(debug_){
	std::cout << "Leading Jet, btag: " << jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[0]->bDiscriminator("pfDeepCSVJetTags:probbb") << std::endl;
	std::cout << "Second leading Jet, btag: " << jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probb") + jetsVecA[1]->bDiscriminator("pfDeepCSVJetTags:probbb") << std::endl;
      }
    }
  }

  return check;

}

// ------------ running over reco protons  ------------
void QuickProtonsAnalysis::fetchProtonsReco(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  ProtonsEvent *protonsSingle;
  protonsSingle = new ProtonsEvent(iEvent, iSetup, protonSingleToken_);
  protonSingleVec = protonsSingle->GetProtonsReco();

  ProtonsEvent *protonsMulti;
  protonsMulti = new ProtonsEvent(iEvent, iSetup, protonMultiToken_);
  protonMultiVec = protonsMulti->GetProtonsReco();

  int nmultiarm45 = 0;
  int nmultiarm56 = 0;
  int nsinglearm45 = 0;
  int nsinglearm56 = 0;

  for ( const auto& protonEvt: protonSingleVec) {
    const CTPPSDetId det_id_single((*protonEvt->contributingLocalTracks().begin())->getRPId());  

    // Getting Xi from Pixels, det_id_single.rp()==3
    if(det_id_single.arm()==0 && det_id_single.rp()==3){
      ++nsinglearm45;
      if(det_id_single.station()==0) hXiRp210Arm45_->Fill(protonEvt->xi());
      if(det_id_single.station()==2) hXiRp220Arm45_->Fill(protonEvt->xi());
    }
    if(det_id_single.arm()==1 && det_id_single.rp()==3){
      ++nsinglearm56;
      if(det_id_single.station()==0) hXiRp210Arm56_->Fill(protonEvt->xi());
      if(det_id_single.station()==2) hXiRp220Arm56_->Fill(protonEvt->xi());
    }

    if(debug_){
      std::cout << "Single RP " << std::endl;
      std::cout << "\tArm: " << det_id_single.arm() << std::endl;
      std::cout << "\tStation: " << det_id_single.station() << std::endl;
      std::cout << "\trp: " << det_id_single.rp() << std::endl;
      std::cout << "\txi: " << protonEvt->xi() << std::endl;
      std::cout << "\tt: " << protonEvt->t() << std::endl;
      std::cout << "\ttheta x: " << protonEvt->thetaX() << std::endl;
      std::cout << "\ttheta y: " << protonEvt->thetaY() << std::endl;
    }

  }
  for ( const auto& protonEvt: protonMultiVec) {
    const CTPPSDetId det_id_multi((*protonEvt->contributingLocalTracks().begin())->getRPId());

    if(det_id_multi.arm()==0){
      hXiMultiArm45_->Fill(protonEvt->xi());
      ++nmultiarm45;
    }
    if(det_id_multi.arm()==1){
      hXiMultiArm56_->Fill(protonEvt->xi());
      ++nmultiarm56;
    }

    if(debug_){
      std::cout << "Multi RP " << std::endl;
      std::cout << "\tArm: " << det_id_multi.arm() << std::endl;
      std::cout << "\tStation: " << det_id_multi.station() << std::endl;
      std::cout << "\trp: " << det_id_multi.rp() << std::endl;
      std::cout << "\txi: " << protonEvt->xi() << std::endl;
      std::cout << "\tt: " << protonEvt->t() << std::endl;
      std::cout << "\ttheta x: " << protonEvt->thetaX() << std::endl;
      std::cout << "\ttheta y: " << protonEvt->thetaY() << std::endl;
      std::cout << "\tVz: " << protonEvt->vz() << std::endl;
      std::cout << "\tTime: " << protonEvt->time() << "+/- " <<protonEvt->timeError() <<std::endl;
    }

  }

  hProtonsMultiplicityMultiArm45_->Fill(iEvent.luminosityBlock(),nmultiarm45);
  hProtonsMultiplicityMultiArm56_->Fill(iEvent.luminosityBlock(),nmultiarm56);
  hProtonsMultiplicitySingleArm45_->Fill(iEvent.luminosityBlock(),nsinglearm45);
  hProtonsMultiplicitySingleArm56_->Fill(iEvent.luminosityBlock(),nsinglearm56);

}

// ------------ running over protons  ------------
void QuickProtonsAnalysis::fetchPPSInfo(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  if(ppslite_){
    ProtonsEvent *protons;
    protons = new ProtonsEvent(iEvent, iSetup, protonToken_);
    ppsVec = protons->GetProtonsLite();


    if(debug_){
      for ( const auto& ppsEvt: ppsVec ) {
	const CTPPSDetId det_id( ppsEvt->getRPId() );
	std::cout << "PPS Lite " << std::endl;
	std::cout << "\tArm: " << det_id.arm() << std::endl;
	std::cout << "\tStation: " << det_id.station() << std::endl;
	std::cout << "\trp: " << det_id.rp() << std::endl;
	std::cout << "\tX: " << ppsEvt->getX() << "+/-" << ppsEvt->getXUnc() << std::endl;
	std::cout << "\tY: " << ppsEvt->getY() << "+/-" << ppsEvt->getYUnc() << std::endl;
      }
    }


  }else{
    // Not in Miniaod!
    ProtonsEvent *pixels;
    pixels = new ProtonsEvent(iEvent, iSetup, pixelsppsToken_);
    pixelsVec = pixels->GetPixels();

    // Not in Miniaod!
    ProtonsEvent *timing;
    timing = new ProtonsEvent(iEvent, iSetup, timingppsToken_);
    timingVec = timing->GetTiming();

    // Not in Miniaod!
    ProtonsEvent *strips;
    strips = new ProtonsEvent(iEvent, iSetup, stripstotemToken_);
    stripsVec = strips->GetStrips();

    if(debug_){
      for ( const auto& pixelsEvt: pixelsVec ) {
	std::cout << "PPS Pixels " << std::endl;
	std::cout << "\tArm: " << pixelsEvt.second.arm() << std::endl;
	std::cout << "\tStation: " << pixelsEvt.second.station() << std::endl;
	std::cout << "\trp: " << pixelsEvt.second.rp() << std::endl;
	std::cout << "\tX: " << pixelsEvt.first->getX0() << "+/-" << pixelsEvt.first->getX0Sigma() << std::endl;
	std::cout << "\tY: " << pixelsEvt.first->getY0() << "+/-" << pixelsEvt.first->getY0Sigma() << std::endl;
      }
      for ( const auto& stripsEvt: stripsVec ) {
	std::cout << "PPS Strips " << std::endl;
	std::cout << "\tArm: " << stripsEvt.second.arm() << std::endl;
	std::cout << "\tStation: " << stripsEvt.second.station() << std::endl;
	std::cout << "\trp: " << stripsEvt.second.rp() << std::endl;
	std::cout << "\tX: " << stripsEvt.first->getX0() << "+/-" << stripsEvt.first->getX0Sigma() << std::endl;
	std::cout << "\tY: " << stripsEvt.first->getY0() << "+/-" << stripsEvt.first->getY0Sigma() << std::endl;
      }
      for ( const auto& timingEvt: timingVec ) {
	std::cout << "PPS Timing " << std::endl;
	std::cout << "\tArm: " << timingEvt.second.arm() << std::endl;
	std::cout << "\tStation: " << timingEvt.second.station() << std::endl;
	std::cout << "\trp: " << timingEvt.second.rp() << std::endl;
	std::cout << "\tX: " << timingEvt.first->getX0() << "+/-" << timingEvt.first->getX0Sigma() << std::endl;
	std::cout << "\tY: " << timingEvt.first->getY0() << "+/-" << timingEvt.first->getY0Sigma() << std::endl;
      }
    }

  }

}

// ------------ saving trigger  ------------
bool QuickProtonsAnalysis::fetchTrigger(const edm::Event& iEvent, const edm::EventSetup& iSetup){

  bool trigger_fired = false;

  TriggerEvent *trigger;
  trigger = new TriggerEvent(iEvent, iSetup, hltPrescaleProvider_, triggerResultsToken_, triggersList_, enablePrescales_);
  triggerVec = trigger->GetTrigger();

  if(enablePrescales_){
    prescalesL1Vec = trigger->GetPrescalesL1();
    prescalesHLTVec = trigger->GetPrescalesHLT();
  }

  for ( const auto& triggerEvt: triggerVec) {
    if(triggerEvt==1) trigger_fired = true;
  }

  if(!enableTrigger_) trigger_fired = true;

  return trigger_fired;

}

// ------------ method called for each event  ------------
  void
QuickProtonsAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{

  using namespace edm;

  ++nevents;

  // Cleaning vectors per event
  cleaning();

  // Trigger fired!
  if((enableBtag_ && fetchTrigger(iEvent,iSetup) && CheckBTag(iEvent,iSetup)) || (!enableBtag_ && fetchTrigger(iEvent,iSetup))){

    for (std::size_t i = 0; i != triggerVec.size(); ++i) {
      if(enableTrigger_){
	hltTriggerNamesHisto_->Fill(triggersList_[i].c_str(),triggerVec[i]);
      }      
      if(enablePrescales_){
	if(debug_){
	  std::cout << "Trigger Name: " << triggersList_[i].c_str() << std::endl; 
	  std::cout << "L1 Prescale: " << prescalesL1Vec[i] << std::endl; 
	  std::cout << "HLT Prescale: " << prescalesHLTVec[i] << std::endl; 
	}
      }
    }

    fetchLHCInfo(iEvent, iSetup);
    if(includeVertices_) fetchVertices(iEvent, iSetup);
    if(includeProtonsReco_) fetchProtonsReco(iEvent, iSetup); 
    if(includePPSInfo_) fetchPPSInfo(iEvent, iSetup); 

  } //end trigger

}


// ------------ method called when a run finishes ------------
void QuickProtonsAnalysis::endRun(const edm::Run& iRun, const edm::EventSetup& iSetup){}

// ------------ method called when a new run number begins  ------------
void QuickProtonsAnalysis::beginRun(const edm::Run& iRun, const edm::EventSetup& iSetup){

  bool debug = false;

  using namespace std;
  using namespace edm;

  bool changed(true);

  if(enableTrigger_ && enablePrescales_){
    if (hltPrescaleProvider_.init(iRun,iSetup,"HLT", changed)) {
      hltPrescaleProvider_.hltConfigProvider();
      if(debug){
	HLTConfigProvider const&  hltConfig = hltPrescaleProvider_.hltConfigProvider();
	if (changed) {
	  for(vector<string>::const_iterator triggerName_ = triggersList_.begin(); triggerName_ != triggersList_.end(); ++triggerName_) {
	    const unsigned int n(hltConfig.size());
	    const unsigned int triggerIndex(hltConfig.triggerIndex(*triggerName_));
	    if (triggerIndex>=n) {
	      hltConfig.dump("Triggers");
	    }
	  }
	  hltConfig.dump("ProcessName");
	  hltConfig.dump("GlobalTag");
	  hltConfig.dump("TableName");
	  hltConfig.dump("Streams");
	  hltConfig.dump("Datasets");
	  hltConfig.dump("PrescaleTable");
	  hltConfig.dump("ProcessPSet");
	}
      }
    }
  }

}

// ------------ method called once each job just before starting event loop  ------------
void QuickProtonsAnalysis::beginJob(){

  edm::Service<TFileService> fs;
  nevents=0;

  // Control Histograms
  if(enableTrigger_){
    TFileDirectory triggerDir = fs->mkdir("TriggerInfo");
    hltTriggerNamesHisto_ = triggerDir.make<TH1F>("HLTTriggerNames","HLTTriggerNames",1,0,1);
    hltTriggerNamesHisto_->SetCanExtend(TH1::kXaxis);
  }

  hXiRp210Arm45_ = fs->make<TH1F>("hXiRp210Arm45",";#xi;entries",500,0,0.3);
  hXiRp210Arm56_ = fs->make<TH1F>("hXiRp210Arm56",";#xi;entries",500,0,0.3);
  hXiRp220Arm45_ = fs->make<TH1F>("hXiRp220Arm45",";#xi;entries",500,0,0.3);
  hXiRp220Arm56_ = fs->make<TH1F>("hXiRp220Arm56",";#xi;entries",500,0,0.3);
  hXiMultiArm45_ = fs->make<TH1F>("hXiMultiArm45",";#xi;entries",500,0,0.3);
  hXiMultiArm56_ = fs->make<TH1F>("hXiMultiArm56",";#xi;entries",500,0,0.3);

  hProtonsMultiplicityMultiArm45_ = fs->make<TProfile>("hProtonsMultiplicityMultiArm45","Proton Multi SEC45;LS;Multiplicity",3000,0,3000,0,20);
  hProtonsMultiplicityMultiArm56_ = fs->make<TProfile>("hProtonsMultiplicityMultiArm56","Proton Multi SEC56;LS;Multiplicity",3000,0,3000,0,20);
  hProtonsMultiplicitySingleArm45_ = fs->make<TProfile>("hProtonsMultiplicityMultiArm45","Proton Single SEC45;LS;Multiplicity",3000,0,3000,0,20);
  hProtonsMultiplicitySingleArm56_ = fs->make<TProfile>("hProtonsMultiplicityMultiArm56","Proton Single SEC56;LS;Multiplicity",3000,0,3000,0,20);

  hInstLumi_ = fs->make<TProfile>("hInstLumi","Inst. Lumi vs LS;LS;Inst. Lumi",3000,0,3000,0,200);
  hCrossingAngle_ = fs->make<TProfile>("hCrossingAngle","Crossing Angle;LS;#alpha_x",3000,0,3000,0,200);
  hBetaStar_ = fs->make<TProfile>("hBetaStar","Beta Star;LS;#beta",3000,0,3000,0,200);


}

// ------------ method called once each job just after ending the event loop  ------------
  void 
QuickProtonsAnalysis::endJob() 
{

  if(enableTrigger_){
    hltTriggerNamesHisto_->Scale(1./float(nevents));
  }

}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
QuickProtonsAnalysis::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


//define this as a plug-in
DEFINE_FWK_MODULE(QuickProtonsAnalysis);
