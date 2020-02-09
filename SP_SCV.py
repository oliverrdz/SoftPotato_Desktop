#### Nernstian SCV simulated with finite differences
#### It assumes an oxidation process and that DR = RO, 
#### @author oliverrdz
#### https://oliverrdz.xyz

import numpy as np
import matplotlib.pyplot as plt

#### Experimental parameters that can be changed:
tMax = 1 # s, total time
A = 1 # cm2, electrode geometrical area
cBulk = 5e-6 # mol/cm3, bulk concentration of the species
D = 1e-5 # cm2/s, diffusion coefficient, assumes DO = DR
n = 1 # number of electrons
F = 96485 # C/mol, Faraday constant
R = 8.315 # J/mol K, Gas constant
T = 298 # K, temperature
E0 = 0 # V, Equilibrium potential
dE = 0.01 # V, Potential increments
Eini = -0.2 # V, Initial potential
Efin = 0.2 # V, Final potential

#### Simulation parameters, change if needed:
nk = 100 # number of time divisions per second
kMax = tMax*nk # number of time elements in total
lamb = 0.45 # lamb = dT/dX²
dt = 1/kMax
dX = np.sqrt(dt/lamb)
iMax = int(6*np.sqrt(lamb*kMax))

#### Definitions and initializations
Ewin = Efin - Eini # Potential window
nE = int(Ewin/dE) # number of potential elements in total
E = np.linspace(Eini,Efin,nE) # Potential array
nFRT = n*F/(R*T)
eps = (E - E0)*nFRT # Normalised potential
C = np.ones([kMax,iMax, nE]) # normalised concentration, initialised to 1
iNorm = np.zeros([kMax,nE])

#### Finite differences to calculate the normalised concentration
# Calculate concentrations in time (k), space (i) and potential (e)
for e in range(0,nE):
	C[:,0,e] = 1/(1+np.exp(eps[e])) # boundary condition for each potential
	for k in range(0,kMax-1):
		for i in range(1,iMax-1):
			C[k+1,i,e] = lamb*C[k,i+1,e] + (1-2*lamb)*C[k,i,e] + lamb*C[k,i-1,e]
	#### Calculate normalised current from normalised concentrations:
	iNorm[:,e] = (C[:,1,e] - C[:,0,e])/dX

#### Changing to dimensional values:
delta = np.sqrt(D*tMax) # diffusion layer thicness
t = np.linspace(0,tMax,kMax) # s, time array
x = np.linspace(0,6*delta,iMax)*1e4 # um, distance from electrode
c = cBulk*C # mol/cm3, concentration as a function of time and distance
iDim = iNorm*n*F*A*D*cBulk/delta # A, dimensional current

#### Plots
plt.figure(1)
plt.subplot(1,2,1)
# Change value -1 to the time indexes desired. -1 refers to the longest time. Change it also in subplot 2
plt.plot(E, iDim[-1,:].T*1e3, '-o') # 1e3 changes i to mA
plt.xlabel('$E$ / V')
plt.ylabel('$i$ / mA')
plt.grid()
plt.subplot(1,2,2)
plt.plot(E, (iDim[-1,:].T/iDim[-1,-1]), '-o') 
plt.xlabel('$E$ / V')
plt.ylabel('$i / i_{lim}$')
plt.grid()

plt.show()
