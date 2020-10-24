#!/usr/bin/python3

import numpy as np

class E:

    def __init__(self, wf, spc, E0=0, n=1, DO=1e-5, DR=1e-5, cOb=1e-6, cRb=0, ks=1e8, alpha=0.5):
        
        self.nT = spc.nT
        self.nX = spc.nX
        self.dX = spc.dX
        self.lamb = spc.lamb
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
    
    def fd(self, k, CR1kb, CO1kb, eps): # Finite Differences
        
        # Boundary condition, Butler-Volmer:
        self.CR[k,0] = (CR1kb + self.dX*self.K0*np.exp(-self.alpha*eps)*(CO1kb + CR1kb/self.DOR))/(
                        1 + self.dX*self.K0*(np.exp((1-self.alpha)*eps) + np.exp(-self.alpha*eps)/self.DOR))
        self.CO[k,0] = CO1kb + (CR1kb - self.CR[k,0])/self.DOR

        # Solving finite differences:
        for j in range(1,self.nX-1):
            self.CR[k,j] = self.CR[k-1,j] + self.lamb*(self.CR[k-1,j+1] - 2*self.CR[k-1,j] + self.CR[k-1,j-1])
            self.CO[k,j] = self.CO[k-1,j] + self.DOR*self.lamb*(self.CO[k-1,j+1] - 2*self.CO[k-1,j] + self.CO[k-1,j-1])
        
        