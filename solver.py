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

## Electrochemistry constants
F = 96485 # C/mol, Faraday constant
R = 8.315 # J/mol K, Gas constant
Temp = 298 # K, Temperature
FRT = F/(R*Temp)

def fd(t, E, n = 1, A = 1, E0 = 0, COb = 0, CRb = 5e-6, DO = 1e-5, DR = 1e-5, ks = 1e3, alpha = 0.5):
    """ 
    
    Solves the Fick's laws for planar diffusion using explicit finite differences.
    Returns the calculated arrays of the current (i), distance (X) and concentration profiles of O and R (CO and CR respectively)
        
    Parameters
    ----------
    t:      s, time array
    E:      V, potential array
    n:      number of electrons (n = 1)
    A:      cm2, geometrical area of the electrode (A = 1 cm2)
    E0:     V, standard potential (E0 = 0 V)
    COb:    mol/cm3, bulk concentration of species O (0 mol/cm3)
    CRb:    mol/cm3, bulk concentration of species R (5e-6 mol/cm3)
    DO:     cm2/s, diffusion coefficient of species O (1e-5 cm2/s)
    DR:     cm2/s, diffusion coefficient of species R (1e-5 cm2/s)
    ks:     cm/s, standard rate constant for electron transfer (1e3 cm/s)
    alpha:  transfer coefficient (0.5)
    
    Returns
    -------
    i:      A, current array
    X:      cm, distance array
    CR:     mol/cm3, concentration matrix of species R [X, t]
    CO:     mol/cm3, concentration matrix of species O [X, t]
    
    Examples
    --------
    >>> import solver as sol
    >>> i, X, CR, CO = sol.fd(t, E, n, A, E0, COb, CRb, DO, DR, ks, alpha)
        
    """
          

    ## Simulation parameters:
    nT = np.size(t) # number of time elements
    dT = 1/nT # adimensional step time
    DOR = DO/DR
    lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
    nT = np.size(t) # number of time elements
    Xmax = 6*np.sqrt(nT*lamb) # Infinite distance
    dX = np.sqrt(dT/lamb) # distance increment
    nX = int(Xmax/dX) # number of distance elements
    
    ## Discretisation of variables and initialisation
    CR = np.ones([nX,nT]) # Initial condition for R, nT*2 refers to two sweeps
    CO = np.zeros([nX,nT]) # Initial condition for O
    X = np.linspace(0,Xmax,nX) # Discretisation of distance
    iNorm = np.zeros([nT])
    eps = (E-E0)*n*FRT # adimensional potential waveform
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
    
    i = iNorm*n*F*A*DR*CRb/delta # Convert to dimensional current
    x = X*np.sqrt(DR*t[-1])
    return i, x, CR*CRb, (1-CR)*CRb ## CHECK!!!!!!

def fd_CdRu(t, E, n = 1, A = 1, E0 = 0, COb = 0, CRb = 5e-6, DO = 1e-5, DR = 1e-5, ks = 1e3, alpha = 0.5, Cd = 20e-4, Ru = 100):
    """ 
    
    Solves the Randless circuit with planar diffusion using explicit finite differences.
    Returns the calculated arrays of the current (i), distance (X) and concentration profiles of O and R (CO and CR respectively)
        
    Parameters
    ----------
    t:      s, time array
    E:      V, potential array
    n:      number of electrons (n = 1)
    A:      cm2, geometrical area of the electrode (A = 1 cm2)
    E0:     V, standard potential (E0 = 0 V)
    COb:    mol/cm3, bulk concentration of species O (0 mol/cm3)
    CRb:    mol/cm3, bulk concentration of species R (5e-6 mol/cm3)
    DO:     cm2/s, diffusion coefficient of species O (1e-5 cm2/s)
    DR:     cm2/s, diffusion coefficient of species R (1e-5 cm2/s)
    ks:     cm/s, standard rate constant for electron transfer (1e3 cm/s)
    alpha:  transfer coefficient (0.5)
    Cd:     F, capacitance
    Ru:     ohms, solution resistance
    
    Returns
    -------
    i:      A, current array
    X:      cm, distance array
    CR:     mol/cm3, concentration matrix of species R [X, t]
    CO:     mol/cm3, concentration matrix of species O [X, t]
    
    Examples
    --------
    >>> import solver as sol
    >>> i, X, CR, CO = sol.fd(t, E, n, A, E0, COb, CRb, DO, DR, ks, alpha)
        
    """
          

    ## Simulation parameters:
    nT = np.size(t) # number of time elements
    dT = 1/nT # adimensional step time
    dt = t[1] - t[0] # dimensional step time
    DOR = DO/DR
    lamb = 0.45 # For the algorithm to be stable, lamb = dT/dX^2 < 0.5
    nT = np.size(t) # number of time elements
    Xmax = 6*np.sqrt(nT*lamb) # Infinite distance
    dX = np.sqrt(dT/lamb) # distance increment
    nX = int(Xmax/dX) # number of distance elements
    
    ## Discretisation of variables and initialisation
    CR = np.ones([nX,nT]) # Initial condition for R, nT*2 refers to two sweeps
    CO = np.zeros([nX,nT]) # Initial condition for O
    V = np.zeros([nT])  # V, capacitor voltage
    V[0] = E[0] # Initial condition for the capacitor voltage
    X = np.linspace(0,Xmax,nX) # Discretisation of distance
    iTot = np.zeros([nT])
    iF = np.zeros([nT])
    eps = (E-E0)*n*FRT # adimensional potential waveform
    delta = np.sqrt(DR*t[-1]) # diffusion layer thickness for each scan rate, CHECK!!!!
    K0 = ks*delta/DR
    
    ## Finite differences
    for k in range(1,nT): # k = time index
        CR[0,k] = (CR[1,k-1] + dX*K0*np.exp(-alpha*eps[k])*(CO[1,k-1] + CR[1,k-1]/DOR))/(1 + dX*K0*(np.exp((1-alpha)*eps[k]) +np.exp(-alpha*eps[k]/DOR)))
        CO[0,k] = CO[1,k-1] + (CR[1,k-1] - CR[0,k])/DOR
        for i in range(1,nX-1): # i = distance index
            CR[i,k] = CR[i,k-1] + lamb*(CR[i+1,k-1] - 2*CR[i,k-1] + CR[i-1,k-1])
            CO[i,k] = CO[i,k-1] + DOR*lamb*(CO[i+1,k-1] - 2*CO[i,k-1] + CO[i-1,k-1])
        
        ## Solving Randless circuit:
        iTot[k] = (E[k] - V[k-1])/Ru # A, i = (Vapp - V)/Ru
        iF[k] = n*F*A*DR*CRb*(CR[1,k] - CR[0,k])/(dX*delta) # A, Faradaic current
        V[k] = V[k-1] + (dt/Cd)*(iTot[k] - iF[k]) # V, solving for the capacitor voltage
    
    x = X*np.sqrt(DR*t[-1])
    return iTot, x, CR*CRb, (1-CR)*CRb ## CHECK!!!!!!
