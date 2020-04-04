#### Simulation of the Randless circuit
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
from scipy.integrate import cumtrapz

import waveforms as wf
import solver as sol
import plots as plot

#%% User parameters

Vapp = 2    # V, applied potential
C = 20e-6   # C/cm2, capacitance
Rs = 5e3    # ohms, solution resistance
A = 1       # cm2, electroactive area

# Potential waveform with default parameters
t, E = wf.step(Estep = Vapp, dt = 0.001)

dt = t[1] - t[0] # s, time step
nt = np.size(t)

Vc = np.zeros(nt) # V, array for the potential at the capacitor
i = np.zeros(nt) # A, array for the current

Vc[0] = 0 # V, initial condition

for k in range(0, nt-1):
    Vc[k+1] = Vc[k] + (dt/(C*Rs))*(E[k] - Vc[k])
    i[k] = A*(C/dt)*(Vc[k+1] - Vc[k])

q = cumtrapz(i, t) # C, accumulative charge

#%% Plots
plot.tE(t, Vc)
plot.ti(t, i)
plot.tq(t[1:], q)



























