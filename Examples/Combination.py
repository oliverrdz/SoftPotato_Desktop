#### Simulation of a combination of sweeps and steps
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

## Creating potential waveform by sections:
t1, E1 = wf.sweep(Eini = -0.5, Efin = 0.5, sr = 0.5, dE = 0.001, ns = 7, tini = 0)
t2, E2 = wf.step(Estep = -0.5, tini = t1[-1], ttot = 10, dt = 0.01)
t3, E3 = wf.step(Estep = 0.5, tini = t2[-1], ttot = 10, dt = 0.01)

## Assembling potential waveform
t = np.concatenate([t1, t2, t3])
E = np.concatenate([E1, E2, E3])

## Solving:
i, x, cR, cO = sol.fd(t, E) # The rest of the parameters left with their default values

#%% Plotting:
plot.Et(t, E, nFig = 1) # Waveform
plot.it(t, i, nFig = 2) # Current vs t
plot.iE(E1, i[0:np.size(E1)], nFig = 3) # CVs
plot.it(t2, i[np.size(E1):np.size(E1) + np.size(E2)], nFig = 4) # First step
plot.it(t3, i[np.size(E1) + np.size(E2):], nFig = 5) # Second step
