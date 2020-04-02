#### Function that creates a potential sweep waveform
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

def sweep(Eini = -0.5, Efin = 0.5, sr = 1, dE = 0.01, ns = 2):
    """ 
    
    Returns t and E for a sweep potential waveform.
    All the parameters are given a default value.
    
    Parameters
    ----------
    Eini: Initial potential in V (-0.5 V)
    Efin: Final potential in V (0.5 V)
    sr: Scan rate in V/s (1 V/s)
    dE: Potential increments in V (0.01 V)
    ns: Number of sweeps (2)
    
    Returns
    -------
    t: time array in s
    E: potential array in E
    
    Examples
    --------
    >>> t, E = sweepE(Eini, Efin, sr, dE, ns)
    
    Returns t and E calculated with the parameters given
        
    """
    Ewin = abs(Efin-Eini) # V, potential window of one sweep
    tsw = Ewin/sr # s, total time for one sweep
    nt = int(Ewin/dE) # number of time and potential elements
    
    E = np.array([]) # potential array
    t = np.linspace(0,tsw*ns,nt*ns) # time array, it can be created outside the loop
    
    # for each sweep, test if the sweep number is odd or even and construct the respective sweep
    for n in range(1,ns+1):
        if (n%2 == 1):
            E = np.append(E, np.linspace(Eini, Efin, nt)) # odd
        else:
            E = np.append(E, np.linspace(Efin, Eini, nt)) # even
            
    return t, E
    
