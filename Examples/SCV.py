#### Simulation of sampled current voltammetry
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
import waveforms as wf
import solver as sol
import plots as plot

## User parameters for the potential waveform:
Eini = -0.3     # V, initial potential
Efin = 0.5      # V, final potential
nE = 80         # number of potential steps
tini = 0        # s, initial time for each step
ttot = 1        # s, total time for each step
dt = 0.01        # s, time step

## User parameters for the simulation:
n = 1           # number of electrons
A = 1           # cm2, geometrical area
E0 = 0          # V, standard potential
COb = 0         # mol/cm3, bulk concentration of O
CRb = 5e-6      # mol/cm3, bulk concentraion of R
DO = 1e-5       # cm2/s, diffusion coefficient of O
DR = 1e-5       # cm2/s, diffusion coefficient of R
ks = 1e3        # cm/s, standard rate constant
alpha = 0.5     # transfer coefficient

# Creates array of potentials:
nt = int(ttot/dt) # number of time elements, required to create E and i arrays
Estep = np.linspace(Eini, Efin, nE)
E = np.zeros([nt, np.size(Estep)]) # Creates E array
i = np.zeros([nt, np.size(Estep)]) # Creates i array

## Iterate over each potential step:
for e in range(0, np.size(Estep)):
    ## Creating potential waveform:
    t, E[:,e] = wf.step(Estep[e], tini, ttot, dt)
    
    ## Solving:
    i[:,e], x, cR, cO = sol.fd(t, np.asarray(E[:,e]), n, A, E0, COb, CRb, DO, DR, ks, alpha)

## Plotting:
#nt = np.array([1, nt-1]) # Time indexes to plot first and last SCVs
plot.tE(t, E) # Waveform
plot.ti(t, i) # Chronoamperograms
plot.Ei(E.T, i.T) # SCVs