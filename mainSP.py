#!/usr/bin/python3

#import numpy as np
import matplotlib.pyplot as plt

import waveform as wf
import spacing as space
import mechanism as mec
import algorithm as alg
import simulation as sim
import plots as p


##### Create waveform object
swp = wf.Sweep()

##### Equal spacing:
spc = space.Equal(swp) # Spacing

##### E mechanism:
Emec = mec.E(swp, spc)

#Emec = alg.FD(swp, spc)

##### Simulation:
sim_FD = sim.Simulate(swp, spc, Emec, Ageo=1)

##### Plots:
plt.figure(1)
p.plot(sim_FD.E, sim_FD.i*1e3, "$E$ / V", "$i$ / mA")

plt.show()
