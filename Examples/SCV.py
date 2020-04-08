#### Simulates sampled current voltammograms
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
Eini = -0.3     # V, initial potential
Efin = 0.5      # V, final potential
nE = 80         # number of potential steps
ttot = 1        # s, total time for each step
dt = 0.01        # s, time step

#%% Creates array of potentials:
nt = int(ttot/dt) # number of time elements, required to create E and i arrays
Estep = np.linspace(Eini, Efin, nE)
E = np.zeros([nt, np.size(Estep)]) # Creates E array
i = np.zeros([nt, np.size(Estep)]) # Creates i array

#%% Iterate over each potential step:
for e in range(0, np.size(Estep)):
    ## Creating potential waveform:
    t, E[:,e] = wf.step(Estep[e], ttot = ttot, dt = dt)
    
    ## Solving:
    i[:,e], x, cR, cO = sol.fd(t, E[:,e])


#%% Plotting

plot.Et(t, E, nFig = 1) # Waveform
plot.it(t, i, nFig = 2) # Chronoamperograms
plot.iE(E.T, i.T, nFig = 3) # SCVs


















