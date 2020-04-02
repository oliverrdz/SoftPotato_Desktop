#### Function that solves the diffusion equations through finite differences
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

def fd(t, E, n = 1, A = 1, E0 = 0, COb = 0, CRb = 5e-6, DO = 1e-5, DR = 1e-5, ks = 1e3, alpha = 0.5):
    
    ## Electrochemistry constants
    F = 96485 # C/mol, Faraday constant
    R = 8.315 # J/mol K, Gas constant
    Temp = 298 # K, Temperature
    nFRT = n*F/(R*Temp)

    ## Simulation parameters:
    DOR = DO/DR
    lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
    dT = t[1] - t[0] # time increment
    nT = np.size(t) # number of time elements
    Xmax = 6*np.sqrt(nT*dT) # Infinite distance
    dX = np.sqrt(dT/lamb) # distance increment
    nX = int(Xmax/dX) # number of distance elements
    
    ## Discretisation of variables and initialisation
    CR = np.ones([nX,nT]) # Initial condition for R, nT*2 refers to two sweeps
    CO = np.zeros([nX,nT]) # Initial condition for O
    X = np.linspace(0,Xmax,nX) # Discretisation of distance
    iNorm = np.zeros([nT])
    eps = (E-E0)*nFRT # adimensional potential waveform
    delta = np.sqrt(DR*t[-1]) # diffusion layer thickness for each scan rate, CHECK!!!!
    K0 = ks*delta/DR
    
    ## Finite differences
    for k in range(1,nT): # k = time index
    	CR[0,k] = (CR[1,k-1] + dX*K0*np.exp(-alpha*eps[k])*(CO[1,k-1] + CR[1,k-1]/DOR))/(1 + dX*K0*(np.exp((1-alpha)*eps[k]) +np.exp(-alpha*eps[k]/DOR)))
    	CO[0,k] = CO[1,k-1] + (CR[1,k-1] - CR[0,k])/DOR
    	for i in range(1,nX-1): # i = distance index
    		CR[i,k] = CR[i,k-1] + lamb*(CR[i+1,k-1] - 2*CR[i,k-1] + CR[i-1,k-1])
    		CO[i,k] = CO[i,k-1] + DOR*lamb*(CO[i+1,k-1] - 2*CO[i,k-1] + CO[i-1,k-1])
    	iNorm[k] = (CR[1,k] - CR[0,k])/dX # Adimensional current
    
    iDim = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current
    
    return iDim, X, CR, CO
