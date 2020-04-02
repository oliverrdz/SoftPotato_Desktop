#### Cottrell simulated with finite differences
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
#### It assumes an oxidation process and that DR = RO, 
#### @author oliverrdz
#### https://oliverrdz.xyz

import numpy as np
import matplotlib.pyplot as plt

#### Experimental parameters:
tMax = 1 # s, total time
n = 1 # number of electrons
A = 1 # cm2, electrode geometrical area
cBulk = 5e-6 # mol/cm3, bulk concentration of the species
D = 1e-5 # cm2/s, diffusion coefficient
F = 96485 # C/mol, Faraday constant

#### Simulation parameters:
nk = 100 # number of time divisions per second
kMax = tMax*nk # number of time elements in total
lamb = 0.45 # lamb = dT/dX²
dt = 1/kMax
dX = np.sqrt(dt/lamb)
iMax = int(6*np.sqrt(lamb*kMax))

C = np.ones([kMax,iMax]) # normalised concentration, initialised to 1
C[:,0] = 0 # boundary condition at the electrode surface

#### Finite differences to calculate the normalised concentration
# Calculate concentrations in time (k) and space(i)
for k in range(0,kMax-1):
    for i in range(1,iMax-1):
        C[k+1,i] = lamb*C[k,i+1] + (1-2*lamb)*C[k,i] + lamb*C[k,i-1]

#### Calculate normalised current from normalised concentrations:
iNorm = (C[:,1] - C[:,0])/dX

#### Changing to dimensional values:
delta = np.sqrt(D*tMax) # diffusion layer thicness
t = np.linspace(0,tMax,kMax) # s, time array
x = np.linspace(0,6*delta,iMax)*10000 # um, distance from electrode
c = cBulk*C # mol/cm3, concentration as a function of time and distance
iDim = iNorm*n*F*A*D*cBulk/delta # A, dimensional current

#### Plots
plt.figure(1)
plt.subplot(1,2,1)
plt.plot(x,c.T*1e6, '-o') # 1e6 changes C to umol/cm3
plt.xlabel('$x$ / $\mu$m')
plt.ylabel('$c$ / $\mu$mol cm$^{-3}$')
plt.subplot(1,2,2)
plt.plot(t, iDim*1e3, '-o') # 1e3 changes i to mA
plt.xlabel('$t$ / s')
plt.ylabel('$i$ / mA')
plt.show()
