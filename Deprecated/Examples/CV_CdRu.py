#### Simulation of cyclic voltammetry of the Randless circuit
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
import waveforms as wf
import solver as sol
import plots as plot
import numpy as np
import matplotlib.pyplot as plt
import time


#%% Waveform parameters
Eini = -0.5                         # V, initial potential
Efin = 0.5                          # V. final potential
dE = 0.001                           # V, potential step
ns = 2                              # number of sweeps

Ewin = abs(Efin - Eini)             # V, potential window
nt = int(Ewin/dE)*ns                # number of time and potential elements

sr = np.array([0.01, 0.2, 0.5])     # V/s, scan rate
nsr = np.size(sr)                   # number of scan rates to iterate over


#%% Simulation parameters
Cd = 20e-4                          # F, capacitance
Ru = 100                            # ohms, solution resistance


#%% Solver
t = np.zeros([nt, nsr])             
E = np.zeros([nt])
i = np.zeros([nt, nsr])

start = time.time()
for nu in range(0, nsr):
    t[:, nu], E = wf.sweep(Eini = Eini, Efin = Efin, sr = sr[nu], dE = dE, ns = ns)
    i[:, nu], x, cr, co = sol.fd_CdRu(t[:,nu], E, Cd = Cd, Ru = Ru)
end = time.time()
print(end - start)


#%% Plotting:

iPk = np.max(i, axis = 0)

fig1 = plt.figure(1)
lineObj = plt.plot(E, i/iPk)
plt.legend(iter(lineObj), ("10 mV s$^{-1}$", "20 mV s$^{-1}$", "50 mV s$^{-1}$"), fontsize = 12, loc = 2)
plt.xlabel("$E$ / V", fontsize = 18)
plt.ylabel("$i/i_{peak}$", fontsize = 18)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 14)
plt.grid()
plt.tight_layout()
plt.show()

fig1.savefig("CV_CdRu.png")
