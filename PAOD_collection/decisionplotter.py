import ROOT
import numpy as np
import root_numpy as rnp
import glob



def flattenrnparray(rnparr):
  d = []
  for l in rnparr:
    d = d + l.tolist()
  return np.array(d)


def lepton_isodec(t, lep, isoWP):
  d = np.array([])
  if (t.GetListOfBranches().Contains("HWW%sAuxDyn.passIso%sCloseByCorrected"%(lep, isoWP))):
    Muon_passIsoCloseByCorrected = flattenrnparray(rnp.tree2array(t, "HWW%sAuxDyn.passIso%sCloseByCorrected"%(lep, isoWP)))
    Muon_passIso = flattenrnparray(rnp.tree2array(t, "HWW%sAuxDyn.passIso%s"%(lep, isoWP)))
    #print Muon_passIsoCloseByCorrected
    #print Muon_passIso
    d = (Muon_passIsoCloseByCorrected - Muon_passIso)
  return d

def fill_hist(h, arr, xbinlabels, Xtitle, Ytitle):
  [h.GetXaxis().SetBinLabel(i+1, xbinlabels[i]) for i in range(len(xbinlabels))]
  h.GetXaxis().SetTitle(Xtitle)
  h.GetYaxis().SetTitle(Ytitle)
  [h.Fill(_) for _ in arr]

def main():
  lep = "Electrons"
  #lep = "Muons" 
  isoWPlist = ["LooseTrackOnly", "Loose", "GradientLoose", "Gradient", "FixedCutTight", "FixedCutTightTrackOnly", "FixedCutLoose" ]
  mega_T = [[] for i in range(len(isoWPlist))]
  for xaod in glob.iglob("*root*"):
    f = ROOT.TFile(xaod, 'r')
    t = f.Get('CollectionTree')
    if (type(t)==ROOT.TTree): 
      mega_T = [mega_T[i]+lepton_isodec(t, lep, isoWPlist[i]).tolist() for i in range(len(isoWPlist))]
    #print mega_T
  ROOT.gROOT.SetBatch(1)
  ROOT.gStyle.SetOptStat(0)
  c = ROOT.TCanvas('c', 'c', 800, 600)
  xbinlabels = ["No correction needed", "Needs correction"]
  fout = open(lep+"flag.txt", 'w')
  fout.write("IsoWP\tneeds_correction\ttotal\n")
  for i in range(len(isoWPlist)):
    hist = ROOT.TH1F(lep+"_"+isoWPlist[i], lep+"_"+isoWPlist[i], 2, -0.5, 1.5)
    fill_hist(hist, mega_T[i], xbinlabels, Xtitle=lep+"_"+isoWPlist[i], Ytitle="Frequency")
    hist.Draw()
    c.Print("Decision_correct_%s_%s.eps"%(lep,isoWPlist[i]))
    fout.write("%s\t%i\t%i\n"%(isoWPlist[i], mega_T[i].count(1), len(mega_T[i])))
  fout.close()

if __name__ == '__main__':
  main()
