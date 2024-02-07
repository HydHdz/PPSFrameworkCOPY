#!/usr/bin/python

from ROOT import TH1D
from SimGeneral.MixingModule.mix_2018_25ns_UltraLegacy_PoissonOOTPU_cfi import mix

prob = TH1D('pileup', '', 99, 0., 98.)

i = 0
for value in mix.input.nbPileupEvents.probValue:
    prob.Fill(i, value)
    i += 1

prob.SaveAs('pileup_2018_UltraLegacy_25ns_PoissonOOTPU.root')
