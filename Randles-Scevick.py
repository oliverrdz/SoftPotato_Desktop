#### Simulates CVs at different scan rates and plots iPk vs sr
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
import time

import waveforms as wf
import solver as sol

## Parameters
Eini = -0.7                         # V, initial potential
Efin = 0.7                          # V. final potential
dE = 0.01                           # V, potential step
ns = 2                              # number of sweeps

n = 1                               # number of electrons
A = 1                               # cm2, area
E0 = 0                              # V, standard potential
COb = 0                             # mol/cm3, bulk concentration of O
CRb = 5e-6                          # mol/cm3, bulk concentration of R
DO = 1e-5                           # cm2/s, diffusion coefficient of O
DR = 1e-5                           # cm2/s, diffusion coefficient of R
ks = 1e3                            # cm/s, standard rate constant
alpha = 0.5                         # transfer coefficient

F = 96485                           # C/mol, Faraday constant
R = 8.315                           # J/mol K, Gas constant
T = 298                             # K, Temperature
nFRT = n*F/(R*T)

Ewin = abs(Efin - Eini)             # V, potential window
nt = int(Ewin/dE)*ns                # number of time and potential elements

sr = np.logspace(-3, 3, 7)          # V/s, scan rates logarithmically spaced between 1e-3 and 1e3
nsr = np.size(sr)                   # number of scan rates to iterate over

#%% Solver
## Create arrays with the correct shapes
t = np.zeros([nt, nsr])             
E = np.zeros([nt, nsr])
i = np.zeros([nt, nsr])

start = time.time()                 # Starts measuring time
for nu in range(0, nsr):
    
    t[:, nu], E[:, nu] = wf.sweep(Eini = Eini, Efin = Efin, sr = sr[nu], dE = dE, ns = ns)
    i[:, nu], x, cr, co = sol.fd(t[:,nu], E[:,nu], n, A, E0, COb, CRb, DO, DR, ks, alpha)

end = time.time()                   # Finishes measuring time
print("Simulation time: " + str(end - start) + " s.")

#%% Analysis
iPk_max = np.max(i, axis = 0)
## Randles-Sevcik
iP_RS = 0.4463*F*A*CRb*np.sqrt(F*sr*DR/(R*T))

#%% Plots

fig1 = plt.figure(1)
lines = plt.plot(E, i)
plt.legend(iter(lines), ("1e$^{-3}$ mV s$^{-1}$", "1e$^{-2}$ mV s$^{-1}$", "1e$^{-1}$ mV s$^{-1}$", "1e$^{0}$ mV s$^{-1}$", "1e$^{1}$ mV s$^{-1}$", "1e$^{2}$ mV s$^{-1}$", "1e$^{3}$ mV s$^{-1}$"))
plt.xlabel("$E$ / V", fontsize = 18)
plt.ylabel("$i$ / A", fontsize = 18)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.grid()
plt.tight_layout()

fig2 = plt.figure(2)
ax = plt.subplot(111)
ax.plot(np.sqrt(sr), iP_RS, '--', label = "Randles-Sevcik")
ax.plot(np.sqrt(sr), iPk_max, 'o', label = "Anodic, $\Delta E$ = 10 mV")
#ax.plot(np.sqrt(sr), iPk_min, '-r', label = "Cathodic")
plt.xlabel("$sr^{1/2}$ / V$^{1/2}$ s$^{-1/2}$", fontsize = 18)
plt.ylabel("$i_{peak}$ / A", fontsize = 18)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.grid()
plt.tight_layout()
ax.legend(fontsize = 14)

plt.show

save = 1
if save:
    fig1.savefig("CVs_dE10mV.png")
    fig2.savefig("CVs_dE10mV_validation.png")
