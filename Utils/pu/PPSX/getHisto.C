void getHisto(){

        TFile *MC_file = new TFile("../../../Skimmer/test/output_QCD_HT700to1000.root");
        TFile* file = TFile::Open("pileup_mc.root", "RECREATE");
        TH1D* hMC = (TH1D*)MC_file->Get("missing_mass/MCInfo/pileup");
        hMC->Write();
        file->Write();

}
