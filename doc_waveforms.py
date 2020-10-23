#!/usr/bin/python3

import waveform as wf
import plots as p
import matplotlib.pyplot as plt
import numpy as np


##### Single potential step
Estep = 0.5 # V, potential step
ttot = 1 # s, total time
dt = 0.01 # time increment

stp = wf.Step(Estep=Estep, ttot=ttot, dt=dt)
plt.figure(1)
p.plot(stp.t, stp.E, xlab="$t$ / s", ylab="$E$ / V")



##### Double potential step
E1 = 0 # V, potential of first step
t1 = 1 # s, time of first step
dt1 = 0.01 # s, time increment of first step
E2 = 0.5 # V, potential of second step
t2 = 5 # s, time of second step
dt2 = 0.05 # s, time increment of second step

stp1 = wf.Step(Estep=E1, ttot=t1, dt=dt1)
stp2 = wf.Step(Estep=E2, ttot=t2, dt=dt2)
stp = wf.Construct([stp1, stp2])
plt.figure(2)
p.plot(stp.t, stp.E, xlab="$t$ / s", ylab="$E$ / V")



##### Sampled current voltammetry waveform
E1 = 0 # V, potential of first step
t1 = 1 # s, time of first step
dt1 = 0.01 # s, time increment of first step
E2 = np.array([0.1, 0.2, 0.3, 0.4, 0.5]) # V, potential of second step
t2 = 5 # s, time of second step
dt2 = 0.05 # s, time increment of second step

nt = int(t1/dt1 + t2/dt2)
nE = np.size(E2)
E = np.zeros([nt, nE])
t = np.zeros([nt, nE])

for e in range(nE):
    stp1 = wf.Step(Estep=E1, ttot=t1, dt=dt1)
    stp2 = wf.Step(Estep=E2[e], ttot=t2, dt=dt2)
    stp = wf.Construct([stp1, stp2])
    t[:,e] = stp.t
    E[:,e] = stp.E

plt.figure(3)
p.plot(t, E, xlab="$t$ / s", ylab="$E$ / V")



##### Sweeps
Eini = -0.5 # V, initial potential of first sweep
Efin = 0.5 # V, final potential of first sweep
sr = 1 # V/s, scan rate
dE = 0.01 # V, potential increment
ns = 2 # number of sweeps

swp = wf.Sweep(Eini=Eini, Efin=Efin, sr=sr, dE=dE, ns=ns)
plt.figure(4)
p.plot(swp.t, swp.E, xlab="$t$ / s", ylab="$E$ / V")



##### Multiple scan rates
sr = np.array([0.1, 0.2, 0.5]) # V/s, scan rate
Eini = -0.5 # V, initial potential of first sweep
Efin = 0.5  # V, final potential of first sweep
dE = 0.01 # V, potential increment
ns = 2 # number of sweeps

# Calculate size of the arrays
Ewin = abs(Efin-Eini)
nt = int(Ewin/dE)*ns
nsr = np.size(sr)

# Initialize arrays
E = np.zeros([nt, nsr])
t = np.zeros([nt, nsr])

# Generate sweeps
for n in range(nsr):
    swp = wf.Sweep(sr=sr[n], Eini=Eini, Efin=Efin, dE=dE, ns=ns)
    t[:,n] = swp.t
    E[:,n] = swp.E

plt.figure(5)
p.plot(t, E, xlab="$t$ / s", ylab="$E$ / V")



##### Combination of sweeps and steps
stp = wf.Step(Estep=-0.5, ttot=2)
swp = wf.Sweep(Eini=-0.5, Efin=0.5, ns=4)
wf1 = wf.Construct([stp, swp])

plt.figure(6)
p.plot(wf1.t, wf1.E, xlab="$t$ / s", ylab="$E$ / V")


plt.show()























