#!/usr/bin/python

import waveform as wf
import simulation as sim
import matplotlib.pyplot as plt

## Create waveform object
#stp = wf.Step(Estep=0.5, ttot=2)
swp = wf.Sweep(Eini=0.5, Efin=-0.5, dE=0.005, ns=2)
wf1 = wf.Construct([swp])

# Simulate
sim_FD = sim.FD(wf1, cOb=1e-6, cRb=0)
#sim_BI = sim.BI(wf1)

plt.figure(1)
plt.plot(wf1.t, wf1.E)
plt.xlabel("$t$ / s")
plt.ylabel("$E$ / V")
plt.grid()

plt.figure(2)
plt.plot(sim_FD.E, sim_FD.i*1e3, label="FD")
#plt.plot(sim_BI.E, sim_BI.i*1e3, label="BI")
plt.xlabel("$E$ / V")
plt.ylabel("$i$ / mA")
plt.legend()
plt.grid()

plt.show()
