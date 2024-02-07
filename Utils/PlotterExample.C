void PlotterExample(){

  // Example how to weight the MC

  gStyle->SetOptStat(1001100);
  Double_t w = 1200;
  Double_t h = 350;
  TCanvas * c1 = new TCanvas("plotter", "plotter", w, h);
  c1->SetWindowSize(w + (w - c1->GetWw()), h + (h - c1->GetWh()));
  c1->Divide(2);

  TCut * ncut = new TCut("nVertex>1");

  //TFile *f = new TFile("/eos/cms/store/group/phys_exotica/PPS-Exo/Ntuples/Ntuples_v35/doublemuon-2018-unmatching.root");
  TFile *f = new TFile("NTuple_mc_bjet.root");
  TTree *T = (TTree*)f->Get("Events");

  // Case 1
  c1->cd(1);
  TH1F * hnVertex = new TH1F("hnVertex", "nVertex", 100, 0, 100);
  T->Project("hnVertex","nVertex*weight",*ncut);
  hnVertex->SetLineColor(kRed);
  hnVertex->GetXaxis()->SetTitle("nVertex");
  hnVertex->GetYaxis()->SetTitle("Multiplicity");
  hnVertex->Draw(); 

  // Case 2
  c1->cd(2);
  T->Draw("nVertex*weight>>h2(60,0,60)",*ncut);
  TH1 *h2 = (TH1*)gPad->GetPrimitive("h2");
  h2->SetLineColor(kBlue);
  h2->GetXaxis()->SetTitle("nVertex");
  h2->GetYaxis()->SetTitle("Multiplicity");

}
