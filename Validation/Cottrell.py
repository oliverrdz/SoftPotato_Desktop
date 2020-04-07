#### Validation of SP with the Cottrell equation
'''
    Copyright (C) 2020 Oliver Rodriguez
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
#### @author oliverrdz
#### https://oliverrdz.xyz

## Import required modules:
import numpy as np
import matplotlib.pyplot as plt
import waveforms as wf
import solver as sol
import plots as plot

## User parameters for the potential waveform:
Estep = 0.5     # V, potential step
tini = 0        # s, initial time
ttot = 10       # s, total time
dt = 0.1        # s, time step

## User parameters for the simulation:
n = 1           # number of electrons
F = 96485       # C/mol, Faraday constant
A = 1           # cm2, geometrical area
E0 = 0          # V, standard potential
COb = 0         # mol/cm3, bulk concentration of O
CRb = 5e-6      # mol/cm3, bulk concentraion of R
DO = 1e-5       # cm2/s, diffusion coefficient of O
DR = 1e-5       # cm2/s, diffusion coefficient of R
ks = 1e3        # cm/s, standard rate constant
alpha = 0.5     # transfer coefficient

#%% Simulation

## Creating potential waveform:
t, E = wf.step(Estep, tini, ttot, dt)

## Solving:
i, x, cR, cO = sol.fd(t, E, n, A, E0, COb, CRb, DO, DR, ks, alpha)

## Cottrell equation
iCot = n*F*A*CRb*np.sqrt(DR)/np.sqrt(np.pi*t[1:])

#%% Plotting:
fig1 = plt.figure(1)
ax = plt.subplot(111)
ax.plot(t, i, 'o', label = "Simulated")
ax.plot(t[1:], iCot, label ="Cottrell")
ax.legend(fontsize = 18)
plt.xlabel("$t$ / s", fontsize = 18)
plt.ylabel("$i$ / A", fontsize = 18)
plot.plotFormat()

fig2 = plt.figure(2)
plt.plot(t[1:], 100*(i[1:] - iCot)/iCot, label = "$i$ - $i_{cot}$")
plt.xlabel("$t$ / s", fontsize = 18)
plt.ylabel("% error", fontsize = 18)
plot.plotFormat()

fig3 = plt.figure(3)
plt.plot(x, cR)
plt.xlabel("$x$ / cm", fontsize = 18)
plt.ylabel("$C_R$ / mol cm$^{-3}$", fontsize = 18)
plt.xlim([0, 0.05])
plot.plotFormat()

fig4 = plt.figure(4)
plt.plot(x, cO)
plt.xlabel("$x$ / cm", fontsize = 18)
plt.ylabel("$C_O$ / mol cm$^{-3}$", fontsize = 18)
plt.xlim([0, 0.05])
plot.plotFormat()

fig5 = plt.figure(5)
plt.plot(t, E)
plt.xlabel("$t$ / s", fontsize = 18)
plt.ylabel("$E$ / V", fontsize = 18)
plot.plotFormat()

save = 1
if save:
    fig1.savefig("it.png")
    fig2.savefig("error.png")
    #fig3.savefig("xCR.png")
    #fig4.savefig("xCO.png")
    #fig5.savefig("tE.png")

