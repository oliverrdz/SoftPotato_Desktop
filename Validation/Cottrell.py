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

## Parameters:
n = 1           # number of electrons
F = 96485 # C/mol, Faraday constant
R = 8.315 # J/mol K, Gas constant
A = 1           # cm2, area
CRb = 5e-6      # mol/cm3, bulk concentration of R
DO = 1e-5       # cm2/s, diffusion coefficient of D
DR = 1e-5       # cm2/s, diffusion coefficient of R

#%% Calculating:

## Simulation:
t, E = wf.step()
i, X, CR, CO = sol.fd(t, E, n = n, A = A, CRb = CRb, DO = DO, DR = DR)

## Cottrell equation
iCot = n*F*A*CRb*np.sqrt(DR)/np.sqrt(np.pi*t)

#%% Plotting:
plt.figure(1)
ax = plt.subplot(111)
ax.plot(t, i, 'o', label = "Simulated")
ax.plot(t, iCot, label ="Analytical")
ax.legend(fontsize = 18)
plt.xlabel("$t$ / s", fontsize = 18)
plt.ylabel("$i$ / A", fontsize = 18)
plot.plotFormat()

plt.figure(2)
plt.plot(t, i - iCot, label = "$i$ - $i_{cot}$")
plt.xlabel("$t$ / s", fontsize = 18)
plt.ylabel("($i$ - $i_{cot}$) / A", fontsize = 18)
plot.plotFormat()
