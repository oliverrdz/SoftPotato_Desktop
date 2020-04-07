#### Simulation of multi pulse chronoamperometry
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
from scipy.integrate import cumtrapz

#%% Generate potential waveform:
t1, E1 = wf.step(Estep = -0.5, tini = 0, ttot = 0.5)
t2, E2 = wf.step(Estep = 0.5, tini = t1[-1], ttot = 2)
t3, E3 = wf.step(Estep = 0, tini = t2[-1], ttot = 2)

t = np.concatenate([t1, t2, t3])
E = np.concatenate([E1, E2, E3])

#%% Solving:
i, x, cR, cO = sol.fd(t, E)

## Integrating to obtain the charge:
q = cumtrapz(i, t) # C, charge

#%% Plotting
plot.Et(t, E, nFig = 1)
plot.it(t, i, nFig = 2)
plot.qt(t[1:], q, nFig = 3)
