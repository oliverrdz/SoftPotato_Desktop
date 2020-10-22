#!/usr/python3

import waveform as wf
import simulation as sim
import numpy as np
import matplotlib.pyplot as plt

##### Parameters #####
sr = np.array([0.1, 0.2, 0.5, 1, 2, 5, 10]) # V/s, scan rate
A = 1
C = 1e-6
D = 1e-5
Eini = 0.5
Efin = -0.5
dE = 0.005
ns = 2

##### Simulation #####
Ewin = abs(Efin-Eini)
nt = int(Ewin/dE)*ns
nsr = np.size(sr)

E = np.zeros([nt, nsr])
t = np.zeros([nt, nsr])
i = np.zeros([nt, nsr])

for n in range(nsr):
    print("Simulation " + str(n+1) + " of " + str(nsr))
    swp = wf.Sweep(sr=sr[n], Eini=Eini, Efin=Efin, dE=dE)
    simFD = sim.FD(swp, cOb=C, cRb=0, DO=D, DR=D)
    t[:,n] = swp.t
    E[:,n] = swp.E
    i[:,n] = simFD.i

# Potential waveform
plt.figure(1)
plt.plot(t, E)
plt.xlabel("$t$ / s")
plt.ylabel("$E$ / V")
plt.grid()

# Cyclic voltammograms
plt.figure(2)
plt.plot(E, i*1e3)
plt.xlabel("$E$ / V")
plt.ylabel("$i$ / mA")
plt.grid()


##### Analysis #####
iPkCat = np.min(i,axis=0)
iRS = -2.69e5*A*C*np.sqrt(D*sr)

# Randles-Sevcik plot
plt.figure(3)
plt.plot(np.sqrt(sr), iPkCat*1e3, "o", label="Simulation")
plt.plot(np.sqrt(sr), iRS*1e3, "-", label="Randles-Sevick")
plt.xlabel(r"$\nu^{1/2}$ / V$^{1/2}$ s$^{-1/2}$")
plt.ylabel("$i_{pk}$ / mA")
plt.legend(loc=1)
plt.grid()



plt.show()
