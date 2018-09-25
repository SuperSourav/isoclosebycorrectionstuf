import ROOT
import numpy as np
import root_numpy as rnp
import glob



def flattenrnparray(rnparr):
  d = []
  for l in rnparr:
    d = d + l.tolist()
  return np.array(d)


def lepton_isoV(t, lep, isovar):
  var = np.array([])
  if (t.GetListOfBranches().Contains("HWW%sAuxDyn.%s"%(lep, isovar))):
    var = flattenrnparray(rnp.tree2array(t, "HWW%sAuxDyn.%s"%(lep, isovar)))
    #pT = flattenrnparray(rnp.tree2array(t, "HWW%sAuxDyn.%s"%(lep, "pt")))
    #print isovar, var
    #print pT
    #var = [var[i]*1./pT[i] for i in range(len(var))]
    var = [v/1000. for v in var] #convert to GeV
  return list(var)

def fill_hist(h, arr, xbinlabels, Xtitle, Ytitle):
  [h.GetXaxis().SetBinLabel(i+1, xbinlabels[i]) for i in range(len(xbinlabels))]
  h.GetXaxis().SetTitle(Xtitle)
  h.GetYaxis().SetTitle(Ytitle)
  [h.Fill(_) for _ in arr]

def fill_h(h, arr, Xtitle, Ytitle):
  h.GetXaxis().SetTitle(Xtitle)
  h.GetYaxis().SetTitle(Ytitle)
  [h.Fill(_) for _ in arr]


def correctioncounter(T, Tcorrected):
  diffcount = 0
  for i in range(len(T)):
    if (T[i] != Tcorrected[i]): diffcount += 1
  return diffcount
 
def ploth(isovar, lep, T, Tcorrected):
  ROOT.gROOT.SetBatch(1)
  ROOT.gStyle.SetOptStat(0)
  c = ROOT.TCanvas('c', 'c', 800, 600)
  if (isovar[:-2] == "topoetcone"):  #Et
    min_x = -5
    max_x = 50
  else: #Pt
    min_x = 0
    max_x = 300

  hist = ROOT.TH1F(lep+"_"+isovar, "", 50, min_x, max_x)
  histcorrected = ROOT.TH1F(lep+"_"+isovar+"corrected", "", 50, min_x, max_x)
  fill_h(hist, T, Xtitle=isovar, Ytitle="Entries")
  fill_h(histcorrected, Tcorrected, Xtitle=isovar, Ytitle="Entries")
  #fill_h(hist, T, Xtitle=isovar+"/pt", Ytitle="Entries")
  #fill_h(histcorrected, Tcorrected, Xtitle=isovar+"/pt", Ytitle="Entries")
  ymax = max(hist.GetMaximum(), histcorrected.GetMaximum())
  histcorrected.SetLineColor(2) #red
  hist.SetMaximum(ymax+10)
  hist.Draw()
  histcorrected.Draw("same")
  leg = ROOT.TLegend(0.65, 0.7, 0.90, 0.8)
  leg.SetBorderSize(0)
  leg.AddEntry(hist, "before correction", "l")
  leg.AddEntry(histcorrected, "after correction", "l")
  c.SetLogy()
  leg.Draw()
  #text = ROOT.TText(max_x/5., ymax*0.2, "fraction of %s with corrected %s= (%i/%i)"%(lep, isovar, correctioncounter(T, Tcorrected), len(T)))
  #text.SetTextSize(100)
  #ptext = ROOT.TPaveText(.05,.1,.95,.8)
  #ptext.AddText("fraction of %s corrected = (%i/%i)"%(lep, correctioncounter(T, Tcorrected), len(T)))
  #text.Draw()
  text = ROOT.TPaveText(0.2,0.8,0.8,0.85,"NDC")
  text.SetTextSize(0.02)
  text.SetBorderSize(0)
  text.SetFillColor(0)
  text.SetTextAlign(12)
  corrlep = correctioncounter(T, Tcorrected)
  text.AddText("%s corrected for %i out of %i %s (~%.1f"%(isovar, corrlep, len(T), lep.lower(), (corrlep*1./len(T))) + "%)")
  text.Draw()
  c.Print("%s_%s.eps"%(lep,isovar))




def main():
  lep = "Electrons"
  #lep = "Muons" 
  isoVarlist = ["ptcone20",     "ptcone30",     "ptcone40",
                "topoetcone20", "topoetcone30", "topoetcone40",
                "ptvarcone20",  "ptvarcone30",  "ptvarcone40"]
  mega_T = [[] for i in range(len(isoVarlist))]
  mega_Tcorrected = [[] for i in range(len(isoVarlist))]
  for xaod in glob.iglob("*root*"):
    f = ROOT.TFile(xaod, 'r')
    t = f.Get('CollectionTree')
    if (type(t)==ROOT.TTree): 
      #print ">T>: ", mega_T
      mega_T = [list(mega_T[i])+list(lepton_isoV(t, lep, isoVarlist[i])) for i in range(len(isoVarlist))]
      #print ">Tcorrected>: ", mega_Tcorrected
      mega_Tcorrected = [list(mega_Tcorrected[i])+list(lepton_isoV(t, lep, isoVarlist[i]+"CloseByCorrected")) for i in range(len(isoVarlist))]
      print xaod+":"
      #for i in range(len(isoVarlist)):
        #print "\t", len(mega_T[i]), "\t", len(mega_Tcorrected[i])
    #print mega_T
    #break
  [ploth(isoVarlist[i], lep, mega_T[i], mega_Tcorrected[i]) for i in range(len(isoVarlist))]

if __name__ == '__main__':
  main()
