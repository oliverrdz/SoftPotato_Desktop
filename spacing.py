#!/usr/bin/python3

import numpy as np

class Equal:

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
        