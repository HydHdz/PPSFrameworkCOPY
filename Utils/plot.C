#include "Canvas.h"

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <stdexcept>

#include <string>
#include <limits>
#include <iomanip>
#include <cstring>
#include <numeric>

//#include <filesystem>
//namespace fs = std::filesystem;

#include <glob.h>

//#include <iostream>  



std::vector<std::string> glob(const std::string& pattern) {
    using namespace std;

    // glob struct resides on the stack
    glob_t glob_result;
    memset(&glob_result, 0, sizeof(glob_result));

    // do the glob operation
    int return_value = glob(pattern.c_str(), GLOB_TILDE, NULL, &glob_result);
    if(return_value != 0) {
        globfree(&glob_result);
        stringstream ss;
        ss << "glob() failed with return_value " << return_value << endl;
        throw std::runtime_error(ss.str());
    }

    // collect all the filenames into a std::list<std::string>
    vector<string> filenames;
    for(size_t i = 0; i < glob_result.gl_pathc; ++i) {
        filenames.push_back(string(glob_result.gl_pathv[i]));
    }
    
    // cleanup
    globfree(&glob_result);

    // done
    return filenames;
}

std::string ReplaceString(std::string subject, const std::string& search,
                          const std::string& replace) {
    size_t pos = 0;
    while((pos = subject.find(search, pos)) != std::string::npos) {
         subject.replace(pos, search.length(), replace);
         pos += replace.length();
    }
    return subject;
}//input string not changed.. 

struct event
{
    double genmissEt;
    double genleadingJetPt;
    double gensecondJetPt;
    double gendijetPt;
};
event e;

void plot() {

    std::string path = "/eos/cms/store/group/phys_exotica/PPS-Exo/Ntuples/Ntuples_v36/";
    std::string dirname = path + "sd*";
    std::vector<std::string> g = glob(dirname);
    //std::vector<std::string> g = glob(path);

    //gStyle->SetPalette(kDarkRainBow);
    std::vector<Color_t>NmCl = {kBlack, kBlue+3, kGreen+3, kRed+2, kViolet+1, kGray+2};

    for (auto & element : g){
        std::cout << element << std::endl;
        std::string filename = element;
        std::string treename = "Events";
        TFile *f = new TFile(filename.c_str());
        TTree *t = (TTree*) f->Get(treename.c_str());

        t->SetBranchAddress("genmissEt",&e.genmissEt);
        t->SetBranchAddress("genleadingJetPt",&e.genleadingJetPt);
        t->SetBranchAddress("gensecondJetPt",&e.gensecondJetPt);
        t->SetBranchAddress("gendijetPt",&e.gendijetPt);

        std::string hname = ReplaceString(element, path, "");
        std::string sname = ReplaceString(hname, "NTuple_mc_muon_", "");
        std::string ssname = ReplaceString(sname, "_B1_TF.root", "");
        std::vector<std::string> cname = {"genmissEt", "genleadingJetPt", "gensecondJetPt", "gendijetPt"};
        std::cout << ssname << std::endl;

        //TCanvas *c1 = new TCanvas(("c1"+sname).c_str(),("c1"+sname).c_str());
        std::string top_label = "13 TeV - 2018";// + En_par;// + " " + beam1 + beam2;
      //Canvas c( plname.c_str(),top_label.c_str(), "DESY",  "with 4.6 GeV/c e^{-}" );
        Canvas c( (ssname+"_"+cname[1]).c_str(),top_label.c_str(), "CMS",  "Simulation Preliminary", false, Canvas::Align::right );
      //Canvas c( plname.c_str(),top_label.c_str(), (angle + "," + En_par).c_str(),  (beam1 + beam2).c_str(), false, Canvas::Align::right );

        vector<TH1D*> H1;
        THStack *hs2 = new THStack(ssname.c_str(),ssname.c_str());
        TH1D *h1 = new TH1D(cname[1].c_str(), cname[1].c_str(), 1000, 0, 500);
            
            for (size_t i = 0; i < t->GetEntries(); i++)
            {
                    t->GetEntry(i);
                    h1->Fill(e.genmissEt);
            }
        h1->SetLineColor(NmCl[0]);
        h1->SetFillColorAlpha(NmCl[0], 0.40);
        H1.emplace_back(h1);
        hs2->Add(h1,"sames");            

            std::vector<double> cutl = {0.,50.,100.,150.,200.};
            std::vector<double> cuth = {50.,100.,150.,200.,250.};

            for (size_t i = 0; i < cutl.size(); i++)
            {
            
            std::ostringstream os;
            os << cutl[i];
            os << "-";
            os << cuth[i];
            std::string s = os.str();
                        
            TH1D *h2 = new TH1D(s.c_str(), s.c_str(), 1000, 0, 500);
            
                for (size_t k = 0; k < t->GetEntries(); k++)
                {
                    t->GetEntry(k);
                    //std::cout << e.genmissEt << std::endl;
                        if (e.genleadingJetPt>cutl[i] && e.genleadingJetPt<cuth[i])
                        {
                            h2->Fill(e.genmissEt);
                        }
                }
            h2->SetLineColor(NmCl[i+1]);
            h2->SetFillColorAlpha(NmCl[i+1], 0.40);
            H1.emplace_back(h2);
            
            hs2->Add(h2,"sames");
            }

        //hs2->Draw("nostack, e1p");
        hs2->Draw("nostack");
        hs2->GetXaxis()->SetTitle("E_{T}^{miss} [GeV/c]");
        hs2->GetYaxis()->SetTitle("Entries");

        //c.SetFillStyle(4050);
        gPad->BuildLegend();
        gPad->Update();

        for (int i = 0; i < H1.size(); ++i)
        {

          TPaveStats *stat1 = (TPaveStats*) H1[i]->FindObject("stats");
          stat1->SetX1NDC( 0.75 );
          stat1->SetX2NDC( 0.90 );
          //stat1->SetY1NDC( ((.1+(.2*i))+.3)-.2);
          //stat1->SetY2NDC( ((.2+(.2*i))+.3)-.2);

          stat1->SetY1NDC( 0.62+(1-i)*0.10 );
          stat1->SetY2NDC( 0.72+(1-i)*0.10 );
          //stat1->SetLineColor( H1[i]->GetFillColor()+2 );  //h1->GetLineColor()
          //stat1->SetTextSize( 0.03 );
          stat1->Draw();
        }
        c.Prettify(hs2->GetHistogram());
        c.SetLogy();
        c.SetLogx();
        c.Save("pdf");
        //c->Draw();
    }


}
