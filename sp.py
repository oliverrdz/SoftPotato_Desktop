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
    """

    def __init__(self, params):
        self.Eini = params[0]
        self.Efin = params[1]
        self.sr = params[2]
        self.dE = params[3]
        self.ns = params[4]

        Ewin = abs(self.Efin-self.Eini)
        tsw = Ewin/self.sr # total time for one sweep
        nt = int(Ewin/self.dE)

        self.E = np.array([])
        self.t = np.linspace(0, tsw*self.ns, nt*self.ns)

        for n in range(1, self.ns+1):
            if (n%2 == 1):
                self.E = np.append(self.E, np.linspace(self.Eini, self.Efin, nt))
            else:
                self.E = np.append(self.E, np.linspace(self.Efin, self.Eini, nt))



class Step:
    """
    Returns t and E for a step potential waveform.
    All the parameters are given a default value.
    """

    def __init__(self, params):

        self.Es = params[0]
        self.ttot = params[1]
        self.dt = params[2]
        self.nt = int(self.ttot/self.dt)

        self.E = np.ones([self.nt])*self.Es
        self.t = np.linspace(0, self.ttot, self.nt)



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

    def __init__(self, wf, space, params):

        self.nT = space.nT
        self.nX = space.nX
        self.dX = space.dX
        self.lamb = space.lamb

        self.E0 = params[0]
        self.n = params[1]
        self.DO = params[2]
        self.DR = params[3]
        self.cOb = params[4]
        self.cRb = params[5]
        self.ks = params[6]
        self.alpha = params[7]
        self.BV = params[8]

        self.delta = np.sqrt(self.DR*wf.t[-1]) # cm, diffusion layer thickness
        self.K0 = self.ks*self.delta/self.DR # Normalised standard rate constant
        self.DOR = self.DO/self.DR

        ## Discretisation of variables and initialisation
        if self.cRb == 0: # In case only O present in solution
            CR = np.zeros([self.nT,self.nX])
            CO = np.ones([self.nT,self.nX])
        else:
            CR = np.ones([self.nT,self.nX])
            CO = np.ones([self.nT,self.nX])*self.cOb/self.cRb

        self.CR = CR
        self.CO = CO



########## Simulation:

class Simulate:

    def __init__(self, wf, space, mec, Ageo=1):
        self.wf = wf
        self.space = space
        self.mec = mec
        self.Ageo = Ageo
        self.eps = (wf.E-mec.E0)*mec.n*FRT # adimensional potential waveform
        self.CO = mec.CO
        self.CR = mec.CR
        self.BV = mec.BV
        print('Simulate ' + self.BV)

    ## Set boundary conditions:
    def bc(self, CR1kb, CO1kb, eps):
        #if self.BV == 'QR': # Quasi reversible
        #    CR = (CR1kb + self.mec.dX*self.mec.K0*np.exp(-self.mec.alpha*eps)*(
        #          CO1kb + CR1kb/self.mec.DOR))/(1 + self.mec.dX*self.mec.K0*(
        #          np.exp((1-self.mec.alpha)*eps) + np.exp(-self.mec.alpha*eps)/self.mec.DOR))
        #    CO = CO1kb + (CR1kb - CR)/self.mec.DOR
        #elif self.BV == 'RO': # R -> O
        #    CR = CR1kb/(1 + self.mec.dX*self.mec.K0*np.exp((1-self.mec.alpha)*eps))
        #    CO = CO1kb + (CR1kb - CR)/self.mec.DOR
        #elif self.BV == 'OR': # O -> R
        #    CR = (CR1kb + self.mec.DOR*CO1kb)/(1 + np.exp(eps))
        #    CO = CR*np.exp(eps)

        dX = self.mec.dX
        K0 = self.mec.K0
        alpha = self.mec.alpha
        DOR = self.mec.DOR

        if self.BV == "QR": # O <-> R
            CR = (CR1kb + dX*K0*np.exp(-alpha*eps)*(CO1kb + CR1kb/DOR))/(
                  1 + dX*K0*(np.exp((1-alpha)*eps) + np.exp(-alpha*eps)/DOR))
            CO = CO1kb + (CR1kb - CR)/DOR
        elif self.BV =="RO": # R -> O
            CR = CR1kb/(1 + dX*K0*np.exp((1-alpha)*eps))
            CO = CO1kb + (CR1kb - CR)/DOR
        else: # O -> R
            #CR = CR1kb/(1 + dX*K0*np.exp((alpha)*eps))
            #CO = CO1kb + (CR1kb - CR)/DOR
            CO = CO1kb/(1 + dX*K0*np.exp((-alpha)*eps))
            CR = CR1kb + (CO1kb - CO)/DOR

        return CR, CO

    def fd(self, progressBar=False): # Finite Differences
        for k in range(1,self.space.nT):

            if progressBar: # Active only when using GUI, updates progress bar
                progressBar.setValue(int(100*k/self.space.nT))

            # Boundary condition, Butler-Volmer:
            self.CR[k,0], self.CO[k,0] = self.bc(self.CR[k-1,1], self.CO[k-1,1], self.eps[k])
            # Apply finite-differenc
            self.CR[k,1:-1] = self.CR[k-1,1:-1] + self.mec.lamb*(self.CR[k-1,2:]\
                            - 2*self.CR[k-1,1:-1] + self.CR[k-1,:-2])
            self.CO[k,1:-1] = self.CO[k-1,1:-1] + self.mec.lamb*(self.CO[k-1, 2:]\
                            - 2*self.CO[k-1, 1:-1] + self.CO[k-1,:-2])

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
