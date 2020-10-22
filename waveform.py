#!/usr/bin/python

import numpy as np



class Sweep:

    def __init__(self, Eini = -0.5, Efin = 0.5, sr = 1, dE = 0.01, ns = 2, tini = 0):
        Ewin = abs(Efin-Eini)
        tsw = Ewin/sr # total time for one sweep
        nt = int(Ewin/dE)

        E = np.array([])
        t = np.linspace(tini, tini+tsw*ns, nt*ns)

        for n in range(1, ns+1):
            if (n%2 == 1):
                E = np.append(E, np.linspace(Eini, Efin, nt))
            else:
                E = np.append(E, np.linspace(Efin, Eini, nt))

        self.E = E
        self.t = t



class Step:

    def __init__(self, Estep = 0.5, tini = 0, ttot = 1, dt = 0.01):
        nt = int(ttot/dt)
        tfin = tini + ttot

        self.E = np.ones([nt])*Estep
        self.t = np.linspace(tini, tfin, nt)

class Construct:

    def __init__(self, wf):
        n = len(wf)
        t = np.array([wf[0].t[0]])
        E = np.array([wf[0].E[0]])

        for i in range(n):
            t = np.concatenate([t,wf[i].t+t[-1]])
            E = np.concatenate([E,wf[i].E])
        self.t = t
        self.E = E

