#!/usr/bin/python

import numpy as np
import softpotato as sp

##### Construct potential waveform:
wf = sp.Sweep()

##### Equal spacing:
space = sp.Equal_spc(wf)

##### E mechanism:
Emec = sp.E_mec(wf, space)

##### Simulate:
sim = sp.Simulate(wf, space, Emec, Ageo=1)
sim.fd() # Use explicit finite diferences

##### Plot;:
sp.Plot_all(sim)


