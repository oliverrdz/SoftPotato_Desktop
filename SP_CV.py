#### Nernstian CV simulated with finite differences
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

import numpy as np
import matplotlib.pyplot as plt

## User parameters
sr = np.array([0.001, 0.01, 0.1,1]) # V/s, scan rate
Eini = -0.5 # V, initial potential
Efin = 0.5 # V, final potential
dE = 0.005 # V, potential increment
E0 = 0 # V, equilibrium potential
DO = 1e-5 # cm/s, diffusion coefficient of species O
DR = 1e-5 # cm/s, diffusion coefficient of species R
COb = 0 # mol/cm3, concentration of species O
CRb = 5e-6 # mol/cm3, concentration of species R
A = 1 # cm2, electrode area

## Electrochemistry constants
n = 1 # Number of electrons
F = 96485 # C/mol, Faraday constant
R = 8.315 # J/mol K, Gas constant
Temp = 298 # K, Temperature
nFRT = n*F/(R*Temp)

## Simulation parameters
DOR = DO/DR
lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
#dT = 1e-3 # time incement
dT = dE # time increment = potential increment
nT = int(1/dT) # number of time elements
Xmax = 6*np.sqrt(nT*dT) # Infinite distance
dX = np.sqrt(dT/lamb) # distance increment
nX = int(Xmax/dX) # number of distance elements
nsr = np.size(sr) # number of scan rates

## Discretisation of variables and initialisation
CR = np.ones([nX,nT*2,nsr]) # Initial condition for R
CO = np.zeros([nX,nT*2,nsr]) # Initial condition fo O
X = np.linspace(0,Xmax,nX) # Discretisation of distance
T = np.linspace(0,1,nT*2) # Discretisation of time

## Creating empty arrays
tMax = np.zeros([nsr])
iNorm = np.zeros([nT*2,nsr])
E = np.zeros([nT*2,nsr])
eps = np.zeros([nT*2,nsr])

## Iterate over scan rate
for s in range(0,np.size(sr)):
	## Creating waveform, only one cycle
	tMax[s] = (Efin-Eini)/sr[s] # s, maximum time
	E[:,s] = np.concatenate([Eini + sr[s]*np.linspace(0,tMax[s],nT), Efin-sr[s]*np.linspace(0,tMax[s],nT)]) # V, potential waveform
	eps[:,s] = (E[:,s]-E0)*nFRT # adimensional potential waveform

	## Finite differences
	for k in range(1,nT*2): # k = time index
		CR[0,k,s] = (CR[1,k-1,s]+DOR*CO[1,k-1,s])/(1+np.exp(eps[k,s]))
		CO[0,k,s] = CR[0,k,s]*np.exp(eps[k,s])
		for i in range(1,nX-1): # i = distance index
			CR[i,k,s] = CR[i,k-1,s] + lamb*(CR[i+1,k-1,s] - 2*CR[i,k-1,s] + CR[i-1,k-1,s])
			CO[i,k,s] = CO[i,k-1,s] + DOR*lamb*(CO[i+1,k-1,s] - 2*CO[i,k-1,s] + CO[i-1,k-1,s])
		iNorm[k,s] = (CR[1,k,s] - CR[0,k,s])/dX

delta = np.sqrt(DR*(Efin-Eini)/sr) # diffusion layer thickness for each scan rate
iDim = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current

iPkAn = np.max(iDim[5:-1,:],0) # Anodic simulated peak current
iPkCa = np.min(iDim[5:-1,:],0) # Cathodic simulated peak current
iRS = 2.69e5*A*np.sqrt(DR)*CRb*np.sqrt(sr) # Randles-Sevcik
error = (1-iRS/iPkAn)*100

print("Scan rates V/s:")
print(sr)
print("Simulated peak currents:")
print(iPkAn)
print("Randles-Sevcik currents:")
print(iRS)
print("Error / %")
print(error)

## Plotting
plt.figure(1)
plt.subplot(1,2,1)
fig = plt.plot(E, iDim*1e3)
plt.legend(fig, ["0.001 V s$^{-1}$", "0.01 V s$^{-1}$", "0.1 V s$^{-1}$", "1 V s$^{-1}$"])
plt.xlabel("$E$ / V")
plt.ylabel("$i$ / mA")
plt.grid()
plt.subplot(1,2,2)
plt.plot(np.sqrt(sr), iPkAn*1e3, '-o', np.sqrt(sr), iPkCa*1e3, '-o')
plt.xlabel("$sr^{1/2}$ / V$^{1/2}$ s$^{-1/2}$")
plt.ylabel("$i_{peak}$ / mA")
plt.grid()
plt.show()
