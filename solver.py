#### Functions to solve the diffusion equations through finite differences
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


## Electrochemistry constants
F = 96485 # C/mol, Faraday constant
R = 8.315 # J/mol K, Gas constant
T = 298 # K, Temperature
FRT = F/(R*T)



def main(t, E, bc_type, params, CdRu, progressBar=0):
    
    n, A, E0, COb, CRb, DO, DR = params[0:7]
        
    ## Simulation parameters:
    nT = np.size(t) # number of time elements
    dT = 1/nT # adimensional step time
    DOR = DO/DR
    lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
    Xmax = 6*np.sqrt(nT*lamb) # Infinite distance
    dX = np.sqrt(dT/lamb) # distance increment
    nX = int(Xmax/dX) # number of distance elements
    
    ## Discretisation of variables and initialisation
    CR = np.ones([nX,nT]) # Initial condition for R, nT*2 refers to two sweeps
    CO = np.zeros([nX,nT]) # Initial condition for O
    X = np.linspace(0,Xmax,nX) # Discretisation of distance
    eps = (E-E0)*n*FRT # adimensional potential waveform
    delta = np.sqrt(DR*t[-1]) # diffusion layer thickness for each scan rate, CHECK!!!!
    
    ## Choosing boundary condition type:
    if bc_type == "BV":
        ks = params[7]
        alpha = params[8]
        K0 = ks*delta/DR
        kinetic_params = [K0, alpha]
    elif bc_type == "Nernst":
        #print("\nNernstian surface concentration")
        kinetic_params = 0
    elif bc_type == "Irrev":
        ks = params[7]
        alpha = params[8]
        K0 = ks*delta/DR
        kinetic_params = [K0, alpha]
    else:
        print("No boundary condition chosen")
        return 0
        
    iNorm, CR, CO = fd(CR, CO, eps, DOR, dX, lamb, bc_type, kinetic_params, progressBar)
    i = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current
    ## Denormalisation
    
    ## Adding double layer capacitance and solution resistance
    if CdRu[0]:
        Cd = CdRu[0]
        Ru = CdRu[1]
        dt = t[1] - t[0]
        i = CdRu_fun(E, dt, i, Cd, Ru)
    
    x = X*np.sqrt(DR*t[-1])
    cR = CR*CRb
    cO = (1-CR)*CRb
    return i, x, cR, cO



## Set boundary conditions:
def bc(bc_type, CR1kb, CO1kb, DOR, dX, eps, kinetic_params):
    if bc_type == 'BV':
        K0 = kinetic_params[0]
        alpha = kinetic_params[1]
        CR = (CR1kb + dX*K0*np.exp(-alpha*eps)*(CO1kb + CR1kb/DOR))/(1 + dX*K0*(np.exp((1-alpha)*eps) + np.exp(-alpha*eps)/DOR))
        CO = CO1kb + (CR1kb - CR)/DOR
    elif bc_type == 'Irrev':
        K0 = kinetic_params[0]
        alpha = kinetic_params[1]
        CR = CR1kb/(1 + dX*K0*np.exp((1-alpha)*eps))
        CO = CO1kb + (CR1kb - CR)/DOR
    elif bc_type == 'Nernst':
        CR = (CR1kb + DOR*CO1kb)/(1 + np.exp(eps)) 
        CO = CR*np.exp(eps)
    return CR, CO



## Finite differences with only faradaic response:
def fd(CR, CO, eps, DOR, dX, lamb, bc_type, kinetic_params, progressBar = 0):
    nT = np.shape(CR)[1]
    nX = np.shape(CR)[0]
    iNorm = np.zeros([nT])
    for k in range(1,nT): # k = time index
        CR[0,k], CO[0,k] = bc(bc_type, CR[1,k-1], CO[1,k-1], DOR, dX, eps[k], kinetic_params)
        for i in range(1,nX-1): # i = distance index
            CR[i,k] = CR[i,k-1] + lamb*(CR[i+1,k-1] - 2*CR[i,k-1] + CR[i-1,k-1])
            CO[i,k] = CO[i,k-1] + DOR*lamb*(CO[i+1,k-1] - 2*CO[i,k-1] + CO[i-1,k-1])
        iNorm[k] = (CR[1,k] - CR[0,k])/dX # Adimensional current
        if progressBar != 0:
            progressBar.setValue(int(100*k/nT))
    return iNorm, CR, CO



## Add double layer capacitance and solution resistance
def CdRu_fun(E, dt, iF, Cd, Ru):
    nT = np.size(E)
    V = np.zeros([nT])  # V, capacitor voltage
    iTot = np.zeros([nT]) # A, total current
    for k in range(1, nT):
        ## Solving Randless circuit:
        iTot[k] = (E[k] - V[k-1])/Ru # A, i = (Vapp - V)/Ru
        V[k] = V[k-1] + (dt/Cd)*(iTot[k] - iF[k]) # V, solving for the capacitor voltage
    return iTot
