void TriggerAbsoluteEfficiency(){

  gStyle->SetOptStat(0);
  Double_t w = 1000;
  Double_t h = 750;
  TCanvas * c1 = new TCanvas("plotter", "plotter", w, h);
  c1->SetWindowSize(w + (w - c1->GetWw()), h + (h - c1->GetWh()));

  //TFile *f = new TFile("/eos/cms/store/group/phys_exotica/PPS-Exo/Grid/doublemuon-data-2018B-13TEV/crab_dmf_2023-10-26_UTC02-11-06/DoubleMuon/crab_crab_dmf_2023-10-26_UTC02-11-06/231026_001113/0000/output_10.root");
  TFile *f = new TFile("/afs/cern.ch/user/d/dmf/private/work/private/CMSPhysicsAnalysis/DarkMatterSearch/2023/NTuplizer/CMSSW_10_6_17_patch1/src/PPSFramework/Skimmer/test/output_muonsc_noppstag.root");
  TH1F *hCount = (TH1F*)f->Get("CounterNoCuts/NCounts");
  TH1F *hTrigger = (TH1F*)f->Get("missing_mass/TriggerInfo/HLTTriggerNames");

  c1->cd();
  hTrigger->Sumw2();
  hTrigger->Scale(1./hCount->GetBinContent(1));

  Int_t b_max = hTrigger->GetMaximumBin();
  Double_t x_max = hTrigger->GetBinCenter(b_max);
  Double_t y_max = hTrigger->GetBinContent(b_max);
  
  hTrigger->GetYaxis()->SetRangeUser(0, y_max+y_max*0.2);
  hTrigger->SetTitle("Absolute Trigger Efficiency");
//  hTrigger->GetYaxis()->SetTitle("#frac{N_{evt fired, 1 proton per RP}}{N_{tot, 1 proton per RP}}");
  hTrigger->GetYaxis()->SetTitle("#frac{N_{evt fired}}{N_{tot}}");
  hTrigger->SetMarkerStyle(20);
  hTrigger->Draw();
  c1->Print("efficiency.pdf");

}
