#!/usr/bin/python3

import waveform as wf
import simulation as sim
import plots as p
import numpy as np
import matplotlib.pyplot as plt

##### Create sweep waveform
swp = wf.Sweep(dE=0.005)

##### Simulate
sim_FD = sim.FD(swp, cOb=0, cRb=1e-6)

##### Plots
# Potential waveform
plt.figure(1)
p.plot(swp.t, swp.E, xlab="$t$ / s", ylab="$E$ / V")
# Cyclic voltammogram
plt.figure(2)
p.plot(sim_FD.E, sim_FD.i*1e3, xlab="$E$ / V", ylab="$i$ / mA")
plt.show()
