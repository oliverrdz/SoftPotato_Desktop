#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

## Electrochemistry constants
F = 96485 # C/mol, Faraday constant    
R = 8.315 # J/mol K, Gas constant
T = 298 # K, Temperature
FRT = F/(R*T)

########## Potential Waveforms

class Sweep:
    """ 
    
    Returns t and E for a sweep potential waveform.
    All the parameters are given a default value.
    
    Parameters
    ----------
    Eini:   V, initial potential (-0.5 V)
    Efin:   V, final potential V (0.5 V)
    sr:     V/s, scan rate (1 V/s)
    dE:     V, potential increments (0.01 V)
    ns:     number of sweeps (2)
    
    Returns
    -------
    t:      time array in s
    E:      potential array in E
    
    Examples
    --------
    >>> import softpotato as sp
    >>> wf = sp.sweep(Eini, Efin, sr, dE, ns)
    
    Returns t and E calculated with the parameters given
        
    """

    def __init__(self, Eini = 0.5, Efin = -0.5, sr = 1, dE = 0.005, ns = 2):
        Ewin = abs(Efin-Eini)
        tsw = Ewin/sr # total time for one sweep
        nt = int(Ewin/dE)

        E = np.array([])
        t = np.linspace(0, tsw*ns, nt*ns)

        for n in range(1, ns+1):
            if (n%2 == 1):
                E = np.append(E, np.linspace(Eini, Efin, nt))
            else:
                E = np.append(E, np.linspace(Efin, Eini, nt))

        self.E = E
        self.t = t



class Step:
    """ 
    
    Returns t and E for a step potential waveform.
    All the parameters are given a default value.
    
    Parameters
    ----------
    Estep:  V, potential step in V (0.5 V)
    ttot:   s, total time of the step (1 s)
    dt:     s, time increment (0.01 s)
    
    Returns
    -------
    t:      s, time array
    E:      V, potential array
    
    Examples
    --------
    >>> import softpotato as sp
    >>> wf = sp.step(Estep, tini, ttot, dt)
    
    
    Returns t and E calculated with the parameters given
    """

    def __init__(self, Estep = 0.5, ttot = 1, dt = 0.01):
        nt = int(ttot/dt)

        self.E = np.ones([nt])*Estep
        self.t = np.linspace(0, ttot, nt)



class Construct_wf:
    """ 
    
    Returns t and E for a customised potential waveform.
    
    Parameters
    ----------
    wf:     list containing the waveform object
    
    Returns
    -------
    t:      s, time array
    E:      V, potential array
    
    Examples
    --------
    >>> import softpotato as sp
    >>> wf1 = sp.step(Estep, tini, ttot, dt)
    >>> wf2 = sp.sweep(Eini, Efin, sr, dE, ns)
    >>> wf = sp.Construct_wf([wf1, wf2])
    
    Returns t and E calculated with the parameters given
    """

    def __init__(self, wf):
        n = len(wf)
        t = np.array([0])
        E = np.array([0])

        for i in range(n):
            t = np.concatenate([t,wf[i].t+t[-1]])
            E = np.concatenate([E,wf[i].E])

        # Remove first data point to prevent repeating time
        self.t = t[1:]
        self.E = E[1:]
        


########## Spacing:

class Equal_spc:
    """ 
    
    Creates equal spacing in X and T
    
    Parameters
    ----------
    wf:     waveform object
    lamb:   dT/dX^2 > 0.5 for stability (0.45)
    
    Returns
    -------
    lamb:   dT/dX^2 > 0.5 for stability (0.45)
    nT:     normalised time, nT = t/tMax
    dX:     normalised distance increment, dX = np.sqrt(dT/lamb)
    nX:     number of distance elements, nX = Xmax/dX
    X:      normalised distance, X = to Xmax = 6*np.sqrt(nT*lamb)
    
    Examples
    --------
    >>> import softpotato as sp
    >>> wf1 = sp.step(Estep, tini, ttot, dt)
    >>> wf2 = sp.sweep(Eini, Efin, sr, dE, ns)
    >>> wf = sp.Construct_wf([wf1, wf2])
    >>> space = Equal_spc(wf, lamb=0.45)
    
    Returns t and E calculated with the parameters given
    """
    
    def __init__(self, wf, lamb=0.45):
        t = wf.t
        self.lamb = lamb

        #%% Simulation parameters
        nT = np.size(t) # number of time elements
        dT = 1/nT # adimensional step time
        Xmax = 6*np.sqrt(nT*lamb) # Infinite distance
        dX = np.sqrt(dT/lamb) # distance increment
        nX = int(Xmax/dX) # number of distance elements
        X = np.linspace(0,Xmax,nX) # Discretisation of distance
        
        self.lamb = lamb
        self.nT = nT
        self.nX = nX
        self.dX = dX
        self.X = X


########## Mechanisms:

class E_mec:

    def __init__(self, wf, space, E0=0, n=1, DO=1e-5, DR=1e-5, cOb=1e-6, cRb=0, ks=1e8, alpha=0.5):
        
        self.nT = space.nT
        self.nX = space.nX
        self.dX = space.dX
        self.lamb = space.lamb
        self.n = n
        self.E0 = E0
        self.delta = np.sqrt(DR*wf.t[-1]) # cm, diffusion layer thickness
        self.K0 = ks*self.delta/DR # Normalised standard rate constant
        self.alpha = alpha
        self.DOR = DO/DR
        self.cRb = cRb
        self.cOb = cOb
        self.DO = DO
        self.DR = DR
        
        ## Discretisation of variables and initialisation
        if cRb == 0: # In case only O present in solution
            CR = np.zeros([self.nT,self.nX])
            CO = np.ones([self.nT,self.nX])
        else:
            CR = np.ones([self.nT,self.nX])
            CO = np.ones([self.nT,self.nX])*cOb/cRb
            
        self.CR = CR
        self.CO = CO
        
        

########## Simulation:
        
class Simulate:

    def __init__(self, wf, space, mec, Ageo=1):
        self.wf = wf
        self.space = space
        self.mec = mec
        self.Ageo = Ageo
        self.eps = (self.wf.E-mec.E0)*mec.n*FRT # adimensional potential waveform
        self.CO = mec.CO
        self.CR = mec.CR
        
    def fd(self): # Finite Differences
        
        for k in range(1,self.space.nT):
            # Boundary condition, Butler-Volmer:
            self.CR[k,0] = (self.CR[k-1,1] + self.mec.dX*self.mec.K0*np.exp(-self.mec.alpha*self.eps[k-1])*(self.CO[k-1,1] + self.CR[k-1,1]/self.mec.DOR))/(
                            1 + self.mec.dX*self.mec.K0*(np.exp((1-self.mec.alpha)*self.eps[k-1]) + np.exp(-self.mec.alpha*self.eps[k-1])/self.mec.DOR))
            self.CO[k,0] = self.CO[k-1,1] + (self.CR[k-1,1] - self.CR[k,0])/self.mec.DOR

            # Solving finite differences:
            for j in range(1,self.mec.nX-1):
                self.CR[k,j] = self.CR[k-1,j] + self.mec.lamb*(self.CR[k-1,j+1] - 2*self.CR[k-1,j] + self.CR[k-1,j-1])
                self.CO[k,j] = self.CO[k-1,j] + self.mec.DOR*self.mec.lamb*(self.CO[k-1,j+1] - 2*self.CO[k-1,j] + self.CO[k-1,j-1])

            self.denorm()

    def denorm(self): # Denormalisation, I believe this can be optimised
        
        if self.mec.cRb:
            I = -self.CR[:,2] + 4*self.CR[:,1] - 3*self.CR[:,0]
            D = self.mec.DR
            c = self.mec.cRb
            cR = self.CR*self.mec.cRb
            if self.mec.cOb:
                cO = self.CO*self.mec.cOb
            else: # In case only R present in solution
                cO = (1-self.CR)*self.mec.cRb
        else: # In case only O present in solution
            I = self.CO[:,2] - 4*self.CO[:,1] + 3*self.CO[:,0]
            D = self.mec.DO
            c = self.mec.cOb
            cO = self.CO*self.mec.cOb
            cR = (1-self.CO)*self.mec.cOb
        i = self.mec.n*F*self.Ageo*D*c*I/(2*self.space.dX*self.mec.delta)
        x = self.space.X*self.mec.delta

        self.E = self.wf.E
        self.t = self.wf.t
        self.i = i
        self.cR = cR
        self.cO = cO
        self.x = x
            
########## Plots:
        
class Plot_all:
    def __init__(self, sim):
        plt.subplot(221)
        Plot(sim.t, sim.E, "$t$ / s", "$E$ / V")
        plt.subplot(222)
        Plot(sim.E, sim.i, "$E$ / V", "$i$ / A")
        plt.subplot(223)
        Plot(sim.t, sim.i, "$t$ / s", "$i$ / A")
        plt.subplot(224)
        Plot2(sim.x, sim.cR[-1,:], sim.x, sim.cO[-1,:], "$x$ / cm", "$c$ / mol cm$^{-3}$", "$c_R$", "$c_O$")
        plt.show()
        
    
class Plot:
    def __init__(self, x, y, xlab, ylab, mark="-"):
        plt.plot(x, y, mark)
        plt.xlabel(xlab, fontsize=18)
        plt.ylabel(ylab, fontsize=18)
        Plot_format()
class Plot2:
    def __init__(self, x1, y1, x2, y2, xlab, ylab, lab1, lab2, mark1="-", mark2="-"):
        plt.plot(x1, y1, mark1, label=lab1)
        plt.plot(x2, y2, mark2, label=lab2)
        plt.xlabel(xlab, fontsize=18)
        plt.ylabel(ylab, fontsize=18)
        plt.legend()
        Plot_format()

class Plot_format:
    def __init__(self):
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        plt.grid()
        plt.tight_layout()
