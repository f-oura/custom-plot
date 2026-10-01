#pragma once
#include "generated.h"
#include <TStyle.h>
#include <TColor.h>
#include <TExec.h>
#include <TLatex.h>
#include <TPad.h>
#include <string>
int rootFont=43;
void style(bool slides,bool grid){auto p=preset(slides);gStyle->SetOptStat(0);gStyle->SetOptTitle(0);gStyle->SetCanvasColor(0);gStyle->SetPadColor(0);gStyle->SetFrameFillColor(0);gStyle->SetTextFont(rootFont);gStyle->SetLabelFont(rootFont,"XYZ");gStyle->SetTitleFont(rootFont,"XYZ");gStyle->SetLabelSize(p.fontPx*.85,"XYZ");gStyle->SetTitleSize(p.fontPx,"XYZ");gStyle->SetTitleOffset(offsets[0],"X");gStyle->SetTitleOffset(offsets[1],"Y");gStyle->SetPadLeftMargin(margins[0]);gStyle->SetPadRightMargin(margins[1]);gStyle->SetPadBottomMargin(margins[2]);gStyle->SetPadTopMargin(margins[3]);gStyle->SetPadTickX(1);gStyle->SetPadTickY(1);gStyle->SetPadGridX(grid);gStyle->SetPadGridY(grid);gStyle->SetGridColor(kGray);gStyle->SetGridStyle(3);gStyle->SetNumberContours(128);}
void title(const char*s,double px){TLatex l;l.SetNDC();l.SetTextFont(rootFont);l.SetTextSize(px);l.DrawLatex(.12,.92,s);}
void palette(int taste,bool diverge){const double (*rgb)[3]=taste==0?(diverge?pal_0_diverging:pal_0_sequential):(taste==1?(diverge?pal_1_diverging:pal_1_sequential):(diverge?pal_2_diverging:pal_2_sequential)); int ids[128]; for(int j=0;j<128;j++)ids[j]=TColor::GetColor(float(rgb[j][0]),float(rgb[j][1]),float(rgb[j][2]));gStyle->SetPalette(128,ids);std::string cmd="int ids[]={";for(int j=0;j<128;j++){if(j)cmd+=",";cmd+=std::to_string(ids[j]);}cmd+="};gStyle->SetPalette(128,ids);";auto ex=new TExec(Form("palette_%d_%d_%d",taste,diverge,gPad->GetNumber()),cmd.c_str());ex->Draw();}
