#### Butler-Volmer SCV simulated with finite differences
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
#### It assumes an oxidation process, 
#### @author oliverrdz
#### https://oliverrdz.xyz

import numpy as np
import matplotlib.pyplot as plt

## User parameters
fileName = "fileName" # Name to save the data, I suggest using parameters
save = False # False to prevent saving
ks = 1e-3 # standard rate constant
alpha = 0.5 # Transfer coefficient
Eini = -0.3 # V, initial potential
Efin = 0.5 # V, final potential
dE = 0.005 # V, potential increment
tMax = 1 # s, maximum time
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
E = np.linspace(Eini,Efin,int((Efin-Eini)/dE))
DOR = DO/DR
lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
dT = 0.005 # time increment, 10 ms for each second
nT = int(tMax/dT) # number of time elements
nE = np.size(E) # number of potential elements
Xmax = 6*np.sqrt(nT*dT) # Infinite distance
dX = np.sqrt(dT/lamb) # distance increment
nX = int(Xmax/dX) # number of distance elements

## Discretisation of variables and initialisation
CR = np.ones([nX,nT,nE]) # Initial condition for R, nT*2 refers to two sweeps
CO = np.zeros([nX,nT,nE]) # Initial condition for O
X = np.linspace(0,Xmax,nX) # Discretisation of distance
T = np.linspace(0,1,nT) # Discretisation of time
iNorm = np.zeros([nT,nE])
eps = (E-E0)*nFRT
delta = np.sqrt(DR*tMax)
K0 = ks*delta/DR

for e in range(1,nE): # e = potential index
    for k in range(1,nT): # k = time index
        CR[0,k,e] = (CR[1,k-1,e] + dX*K0*np.exp(-alpha*eps[e])*(CO[1,k-1,e] + CR[1,k-1,e]/DOR))/(1 + dX*K0*(np.exp((1-alpha)*eps[e]) +np.exp(-alpha*eps[e]/DOR)))
        CO[0,k,e] = CO[1,k-1,e] + (CR[1,k-1,e] - CR[0,k,e])/DOR
        for i in range(1,nX-1): # i = distance index
            CR[i,k,e] = CR[i,k-1,e] + lamb*(CR[i+1,k-1,e] - 2*CR[i,k-1,e] + CR[i-1,k-1,e])
            CO[i,k,e] = CO[i,k-1,e] + DOR*lamb*(CO[i+1,k-1,e] - 2*CO[i,k-1,e] + CO[i-1,k-1,e])
        iNorm[k,e] = (CR[1,k,e] - CR[0,k,e])/dX # Adimensional current

iDim = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current

if save == True:
	np.savetxt("i_" + fileName + ".txt",iDim, delimiter = ",", header = "i / A")
	
## Plotting
nt = np.array([1, nT-1]) # time indexes to plot 1st and last SCV
plt.figure(1)
fig = plt.plot(E, iDim[nt,:].T/iDim[nt,-1], '-o')
plt.xlabel("$E$ / V")
plt.ylabel("$i / i_{lim}$")
plt.grid()
plt.show()
