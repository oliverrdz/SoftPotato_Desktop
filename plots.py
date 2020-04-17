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
    
def Et(t, E): # For potential waveform
    """ 
    
    Plots E vs t (potential waveform)
    
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

def it(t, i):
    """ 
    
    Plots i vs t (current transients)
    
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
    
def qt(t, q):
    """ 
    
    Plots q vs t (charge transients)
    
    Parameters
    ----------
    t:  s, time array
    q:  C, charge array
        
    """
    plt.figure()
    plt.plot(t, q, '-')
    plt.xlabel("$t$ / s", fontsize = 18)
    plt.ylabel("$q$ / C", fontsize = 18)
    plotFormat()
    
def Cx(x, C): # For concentration profiles
    """ 
    
    Plots C vs x (concentration profile)
    
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
    
def iE(E, i): # For voltammetry
    """ 
    
    Plots i vs E  (voltammetry)
    
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
    
def qE(E, q): 
    """ 
    
    Plots q vs E
    
    Parameters
    ----------
    E:  V, potential array
    q:  C, charge array
        
    """
    plt.figure()
    plt.plot(E, q, '-')
    plt.xlabel("$E$ / V", fontsize = 18)
    plt.ylabel("$q$ / C", fontsize = 18)
    plotFormat()
    
def itCottrell(t, i): # Cottrell plot
    """ 
    
    Plots i vs 1/sqrt(t) (Cottrell plot)
    
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