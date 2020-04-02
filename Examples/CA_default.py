#### Simulation of chronoamperometry with default parameters
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

## Creating potential waveform:
t, E = wf.step()

## Solving:
i, x, cR, cO = sol.fd(t, E)

## Plotting:
plot.tE(t, E) # Waveform
plot.ti(t, i) # Chronoamperogram
plot.xC(x, cR) # Concentration profile for R