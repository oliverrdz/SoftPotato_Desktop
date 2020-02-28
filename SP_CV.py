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
fileName = "1mVs_ks1e3_a05" # Name to save the data
save = True # False to prevent saving
ks = 1e3 # standard rate constant
alpha = 0.5 # Transfer coefficient
sr = 0.001 # V/s, scan rate
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
dT = dE # time increment = potential increment
nT = int(1/dT) # number of time elements
Xmax = 6*np.sqrt(nT*dT) # Infinite distance
dX = np.sqrt(dT/lamb) # distance increment
nX = int(Xmax/dX) # number of distance elements

## Discretisation of variables and initialisation
CR = np.ones([nX,nT*2]) # Initial condition for R, nT*2 refers to two sweeps
CO = np.zeros([nX,nT*2]) # Initial condition fo O
X = np.linspace(0,Xmax,nX) # Discretisation of distance
T = np.linspace(0,1,nT*2) # Discretisation of time
iNorm = np.zeros([nT*2])
tMax = (Efin-Eini)/sr # s, maximum time
E = np.concatenate([Eini + sr*np.linspace(0,tMax,nT), Efin-sr*np.linspace(0,tMax,nT)])
eps = (E-E0)*nFRT # adimensional potential waveform
delta = np.sqrt(DR*(Efin-Eini)/sr) # diffusion layer thickness for each scan rate
K0 = ks*delta/DR

## Finite differences
for k in range(1,nT*2): # k = time index
	CR[0,k] = (CR[1,k-1] + dX*K0*np.exp(-alpha*eps[k])*(CO[1,k-1] + CR[1,k-1]/DOR))/(1 + dX*K0*(np.exp((1-alpha)*eps[k]) +np.exp(-alpha*eps[k]/DOR)))
	CO[0,k] = CO[1,k-1] + (CR[1,k-1] - CR[0,k])/DOR
	for i in range(1,nX-1): # i = distance index
		CR[i,k] = CR[i,k-1] + lamb*(CR[i+1,k-1] - 2*CR[i,k-1] + CR[i-1,k-1])
		CO[i,k] = CO[i,k-1] + DOR*lamb*(CO[i+1,k-1] - 2*CO[i,k-1] + CO[i-1,k-1])
	iNorm[k] = (CR[1,k] - CR[0,k])/dX # Adimensional current

iDim = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current

iPkAn = np.max(iDim,0) # Anodic simulated peak current
iRS = 2.69e5*A*np.sqrt(DR)*CRb*np.sqrt(sr) # Randles-Sevcik
error = (1-iRS/iPkAn)*100

print("Scan rate V/s:")
print(sr)
print("Simulated peak current:")
print(iPkAn)
print("Randles-Sevcik currents:")
print(iRS)
print("Error / %:")
print(error)

if save == True:
	np.savetxt("iE_" + fileName + ".txt", np.column_stack((E, iDim)), delimiter = ",", header = "E / V, i / A")

## Plotting
plt.figure(1)
fig = plt.plot(E, iDim*1e3)
plt.xlabel("$E$ / V")
plt.ylabel("$i$ / mA")
plt.grid()
plt.show()
