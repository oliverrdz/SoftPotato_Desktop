#### Functions for easy plotting
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

import matplotlib.pyplot as plt
import numpy as np

def plotFormat():
    """ 
    
    Reusable code for plotting

    """
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid()
    plt.tight_layout()
    plt.show

def tE(t, E): # For potential waveform
    """ 
    
    Plots t vs E (potential waveform)
    
    Parameters
    ----------
    t:  s, time array
    E:  V, potential array
        
    """
    plt.figure()
    plt.plot(t, E, '-')
    plt.xlabel("$t$ / s", fontsize = 18)
    plt.ylabel("$E$ / V", fontsize = 18)
    plotFormat()

def ti(t, i):
    """ 
    
    Plots t vs i (current transients)
    
    Parameters
    ----------
    t:  s, time array
    i:  A, current array
        
    """
    plt.figure()
    plt.plot(t, i, '-')
    plt.xlabel("$t$ / s", fontsize = 18)
    plt.ylabel("$i$ / A", fontsize = 18)
    plotFormat()
    
def xC(x, C): # For concentration profiles
    """ 
    
    Plots x vs C (concentration profile)
    
    Parameters
    ----------
    x:  cm, distance array
    C:  mol/cm3, concentration matrix (or array)
        
    """
    plt.figure()
    plt.plot(x, C, '-')
    plt.xlabel("$x$ / cm", fontsize = 18)
    plt.ylabel("$C$ / mol cm$^{-3}$", fontsize = 18)
    plotFormat()
    
def Ei(E, i): # For voltammetry
    """ 
    
    Plots E vs i (voltammetry)
    
    Parameters
    ----------
    E:  V, potential array
    i:  A, current array
        
    """
    plt.figure()
    plt.plot(E, i, '-')
    plt.xlabel("$E$ / V", fontsize = 18)
    plt.ylabel("$i$ / A", fontsize = 18)
    plotFormat()
    
def tiCottrell(t, i): # Cottrell plot
    """ 
    
    Plots 1/sqrt(t) vs i (Cottrell plot)
    
    Parameters
    ----------
    t:  s, time array
    i:  A, current array
        
    """
    plt.figure()
    plt.plot(1/np.sqrt(t), i, '-')
    plt.xlabel("$t^{-1/2}$ / s$^{-1/2}$", fontsize = 18)
    plt.ylabel("$i$ / A", fontsize = 18)
    plotFormat()