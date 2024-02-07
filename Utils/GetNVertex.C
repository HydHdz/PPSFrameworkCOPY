void GetNVertex(){

  TFile *f = new TFile("NTuple_mc_bjet.root");
  TFile* fileout_ = TFile::Open("pileupD.root", "RECREATE");
  TTree *T = (TTree*)f->Get("Events");
  T->Draw("nVertex>>pileup(100,0,100)");
  TH1 *h1 = (TH1*)gPad->GetPrimitive("pileup");
  h1->Write();
  fileout_->Write();

}
