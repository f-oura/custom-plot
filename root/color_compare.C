// Same fixed synthetic CSVs and 128-entry LUTs as python/color_compare.py.
#include "gallery.C"
#include "color_options.h"
#include <TPad.h>
#include <TBox.h>
#include <fstream>
#include <iomanip>

int exact_color(double r,double g,double b) {
  int id=TColor::GetFreeColorIndex();new TColor(id,r,g,b);return id;
}
void option_palette(const double rgb[128][3],const char* name) {
  int ids[128];
  for(int i=0;i<128;i++) ids[i]=exact_color(rgb[i][0],rgb[i][1],rgb[i][2]);
  gStyle->SetPalette(128,ids);
  std::string code="int ids[]={";
  for(int i=0;i<128;i++){if(i)code+=",";code+=std::to_string(ids[i]);}
  code+="};gStyle->SetPalette(128,ids);";
  (new TExec(name,code.c_str()))->Draw();
}
TPad* panel(const char* name,double x1,double y1,double x2,double y2) {
  auto pad=new TPad(name,name,x1,y1,x2,y2);pad->Draw();pad->cd();return pad;
}
void density_panel(const std::vector<std::vector<double>>& data,int idx,bool log,bool diff,const double rgb[128][3],const char* caption,double px) {
  gPad->SetLeftMargin(.24);gPad->SetRightMargin(.17);gPad->SetBottomMargin(.26);gPad->SetTopMargin(.23);
  gStyle->SetTitleOffset(1.0,"X");gStyle->SetTitleOffset(1.1,"Y");
  auto h=new TH2D(Form("density%d",idx),"",24,-3.130434783,3.130434783,24,-3.130434783,3.130434783);
  for(auto&r:data) h->SetBinContent(h->FindBin(r[0],r[1]),r[diff?3:2]);
  h->GetXaxis()->SetTitle("x [a.u.]");h->GetYaxis()->SetTitle((idx%10==0 || idx%10==4)?"y [a.u.]":"");
  h->SetMinimum(diff?-30:(log?1:0));h->SetMaximum(diff?30:60);
  if(log){gPad->SetLogz();gPad->SetFrameFillColor(TColor::GetColor("#eeeeee"));}
  else if(diff){gPad->SetFrameFillColor(exact_color(rgb[64][0],rgb[64][1],rgb[64][2]));}
  else if(!diff){gPad->SetFrameFillColor(exact_color(rgb[0][0],rgb[0][1],rgb[0][2]));}// COL skips zero cells; fill the frame with the actual zero color, preserving vectors.
  h->Draw("AXIS");option_palette(rgb,Form("lut%d",idx));h->Draw("COLZ SAME");h->Draw("AXIS SAME");
  title(caption,px*.8);gPad->Update();
}
void color_compare() {
  gROOT->SetBatch(kTRUE);
  const auto counts=csv("data/counts.csv"),density=csv("data/density.csv");
  rootFont=tasteFonts[0];
  std::ofstream lutCheck("qa/color-root-lut.csv");
  const double (*tables[4])[3]={cmap_viridis,cmap_Blues,cmap_YlGnBu,cmap_RdBu_r};
  const char* tableNames[4]={"viridis","Blues","YlGnBu","RdBu_r"};
  for(int table=0;table<4;table++)for(int i=0;i<128;i++){auto id=exact_color(tables[table][i][0],tables[table][i][1],tables[table][i][2]);auto color=gROOT->GetColor(id);lutCheck<<std::setprecision(10)<<tableNames[table]<<","<<i<<","<<color->GetRed()<<","<<color->GetGreen()<<","<<color->GetBlue()<<"\n";}
  std::ofstream manifest("qa/color-root-manifest.txt");
  for(int slides=0;slides<2;slides++){
    style(slides,false);auto p=preset(slides);
    auto cv=new TCanvas(Form("optionCanvas%d",slides),"classic | colors 1 vs 4 | SYNTHETIC",p.width,p.height);
    cv->SetCanvasSize(p.width,p.height);
    for(int option=0;option<2;option++){
      int colors[3];for(int i=0;i<3;i++)colors[i]=exact_color(optColors[option][i].r,optColors[option][i].g,optColors[option][i].b);
      cv->cd();auto up=panel(Form("upper%d%d",slides,option),.5*option,.67,.5*(option+1),.955);
      up->SetLeftMargin(.14);up->SetRightMargin(.04);up->SetBottomMargin(.16);up->SetTopMargin(.15);
      frame(Form("overlay%d%d",slides,option),"Counts / 0.2 GeV",0,210);
      auto frameHist=(TH1*)up->GetPrimitive(Form("overlay%d%d",slides,option));frameHist->GetXaxis()->SetTitle("");frameHist->GetXaxis()->SetLabelSize(0);
      auto a=graph(counts,0,colors[0],20,1),b=graph(counts,2,colors[1],21,2);
      a->Draw("P SAME");b->Draw("P SAME");
      auto fit=new TGraph();for(size_t j=0;j<counts.size();j++)fit->SetPoint(j,counts[j][0],counts[j][4]);
      fit->SetLineColor(colors[2]);fit->SetLineStyle(3);fit->SetLineWidth(2);fit->Draw("L SAME");
      auto leg=new TLegend(.69,.58,.95,.82);leg->SetTextFont(rootFont);leg->SetTextSize(p.fontPx*.8);leg->SetBorderSize(0);leg->SetFillStyle(0);
      leg->AddEntry(a,"observed","pe");leg->AddEntry(b,"reference","pe");leg->AddEntry(fit,"fit model","l");leg->Draw();
      title(option==0?"Option 1: blue / orange / teal":"Option 4: black / blue / vermilion",p.fontPx);
      cv->cd();auto dn=panel(Form("ratio%d%d",slides,option),.5*option,.515,.5*(option+1),.67);
      dn->SetLeftMargin(.14);dn->SetRightMargin(.04);dn->SetTopMargin(.05);dn->SetBottomMargin(.3);
      gStyle->SetTitleOffset(.8,"X");frame(Form("ratframe%d%d",slides,option),"Ratio",0,5);
      graph(counts,3,colors[0],20,1)->Draw("P SAME");line(1);gStyle->SetTitleOffset(offsets[0],"X");
    }
    const double (*luts[3])[3]={cmap_viridis,cmap_Blues,cmap_YlGnBu};const char* palettes[3]={"1: viridis","4: Blues","4: YlGnBu"};
    for(int row=0;row<2;row++)for(int col=0;col<4;col++){
      cv->cd();auto pad=panel(Form("map%d%d%d",slides,row,col),.25*col,row==0?.265:.02,.25*(col+1),row==0?.505:.26);
      if(col<3)density_panel(density,slides*10+row*4+col,row==1,false,luts[col],Form("%s | %s counts",palettes[col],row?"log":"linear"),p.fontPx);
      else if(row==0)density_panel(density,slides*10+3,false,true,cmap_RdBu_r,"Shared signed diff | center=0",p.fontPx);
      else{
        TLatex note;note.SetNDC();note.SetTextFont(rootFont);note.SetTextSize(p.fontPx*.85);
        const char* lines[]={"SYNTHETIC | stat only","Log density: 261 zeros blank","Gray frame = zero / not in log","Ratio: independent Poisson errors","Fit mean=3, width=.38 fixed","Option 1 magenta: reserved","No auxiliary curve invented","Colors still awaiting selection"};
        for(int i=0;i<8;i++)note.DrawLatex(.05,.86-.105*i,lines[i]);
      }
    }
    cv->cd();TLatex heading;heading.SetNDC();heading.SetTextFont(rootFont);heading.SetTextSize(p.fontPx*1.2);
    heading.DrawLatex(.04,.979,Form("ROOT | classic | options 1 and 4 | %s | SYNTHETIC",slides?"slides":"paper"));
    cv->SaveAs(Form("output/color-root-%s.png",slides?"slides":"paper"));
    cv->SaveAs(Form("output/color-root-%s.pdf",slides?"slides":"paper"));
    manifest<<(slides?"slides":"paper")<<" counts: range 0-8, y0-210, ratio0-5; density0/1-60; signed -30..30; zero bins261\n";
  }
}
