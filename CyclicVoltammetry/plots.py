import numpy as np
import matplotlib.pyplot as plt

##### Parameters
A = 1
n = 1
E0 = 0
cO = 0
cR = 1e-6
DO = 1e-5
DR = 1e-5
ks = 1e8
alpha = 0.5

##### Reversible system, O + e <=> R, ks = 1e8 cm/s
data = np.loadtxt('CV10mVs.txt', delimiter=',')
E10 = data[:,1]
i10 = data[:,2]
data = np.loadtxt('CV100mVs.txt', delimiter=',')
E100 = data[:,1]
i100 = data[:,2]
data = np.loadtxt('CV1000mVs.txt', delimiter=',')
E1000 = data[:,1]
i1000 = data[:,2]
data = np.loadtxt('CV10000mVs.txt', delimiter=',')
E10000 = data[:,1]
i10000 = data[:,2]

data = np.loadtxt('CV10mVs_dE0.005.txt', delimiter=',')
E10_005 = data[:,1]
i10_005 = data[:,2]
data = np.loadtxt('CV100mVs_dE0.005.txt', delimiter=',')
E100_005  = data[:,1]
i100_005  = data[:,2]
data = np.loadtxt('CV1000mVs_dE0.005.txt', delimiter=',')
E1000_005  = data[:,1]
i1000_005  = data[:,2]
data = np.loadtxt('CV10000mVs_dE0.005.txt', delimiter=',')
E10000_005  = data[:,1]
i10000_005  = data[:,2]

data = np.loadtxt('CV10mVs_dE0.001.txt', delimiter=',')
E10_001 = data[:,1]
i10_001 = data[:,2]
data = np.loadtxt('CV100mVs_dE0.001.txt', delimiter=',')
E100_001  = data[:,1]
i100_001  = data[:,2]
data = np.loadtxt('CV1000mVs_dE0.001.txt', delimiter=',')
E1000_001  = data[:,1]
i1000_001  = data[:,2]
data = np.loadtxt('CV10000mVs_dE0.001.txt', delimiter=',')
E10000_001  = data[:,1]
i10000_001  = data[:,2]

plt.figure(1)
plt.plot(E10, i10*1e3, label='10 mV s$^{-1}$')
plt.plot(E100, i100*1e3, label='100 mV s$^{-1}$')
plt.plot(E1000, i1000*1e3, label='1 V s$^{-1}$')
plt.plot(E10000, i10000*1e3, label='10 V s$^{-1}$')
plt.xlabel('$E$ / V', fontsize=12)
plt.ylabel('$i$ / mA', fontsize=12)
plt.legend(loc=1, fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.tight_layout()

# Randles-Sevcik equation
sr = np.array([0.01, 0.1, 1, 10])
iPk = np.array([np.max(i10), np.max(i100), np.max(i1000), np.max(i10000)])
iPk_005 = np.array([np.max(i10_005), np.max(i100_005), np.max(i1000_005), np.max(i10000_005)])
iPk_001 = np.array([np.max(i10_001), np.max(i100_001), np.max(i1000_001), np.max(i10000_001)])

iRS = 2.69e5*A*np.sqrt(DR*sr)*cR

plt.figure(2)
plt.plot(np.sqrt(sr), iPk*1e3, 'o', markersize=8, label='$\Delta E$ = 0.01 V')
plt.plot(np.sqrt(sr), iPk_001*1e3, 'o', markersize=8, label='$\Delta E$ = 0.001 V')
plt.plot(np.sqrt(sr), iRS*1e3, 'xk--', markersize=8, label='Analytical')
plt.xlabel(r'$\nu^{1/2}$ / V$^{1/2}$ s$^{1/2}$', fontsize=12)
plt.ylabel('$i_{peak}$ / mA', fontsize=12)
plt.legend(loc=2, fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.tight_layout()


##### Quasi reversible system, O + e <=> R, ks = 1e-3 cm/s
data = np.loadtxt('CV1uVs_qr.txt', delimiter=',')
E1uVs = data[:,1]
i1uVs = data[:,2]
data = np.loadtxt('CV100mVs_qr.txt', delimiter=',')
E100mVs = data[:,1]
i100mVs = data[:,2]
data = np.loadtxt('CV100000mVs_qr.txt', delimiter=',')
E100000mVs = data[:,1]
i100000mVs = data[:,2]

sr_QR = np.array([1e-6, 1e-3, 0.1, 1, 10, 100])

plt.figure(3)
plt.plot(E1uVs, i1uVs*1e3/np.sqrt(sr_QR[0]), label='1 $\mu$V s$^{-1}$')
plt.plot(E100mVs, i100mVs*1e3/np.sqrt(sr_QR[2]), label='100 mV s$^{-1}$')
plt.plot(E100000mVs, i100000mVs*1e3/np.sqrt(sr_QR[5]), label='100 V s$^{-1}$')
plt.xlabel('$E$ / V', fontsize=12)
plt.ylabel(r'$i \nu^{-1/2}$ / mC V$^{-1/2}$ s$^{-1/2}$', fontsize=12)
plt.legend(loc=2, fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.tight_layout()


##### Irreversible system, R - e -> O, ks = 1e-3 cm/s
data = np.loadtxt('CV10mVs_ir.txt', delimiter=',')
E10mVs = data[:,1]
i10mVs = data[:,2]
data = np.loadtxt('CV100mVs_ir.txt', delimiter=',')
E100mVs = data[:,1]
i100mVs = data[:,2]
data = np.loadtxt('CV1000mVs_ir.txt', delimiter=',')
E1000mVs = data[:,1]
i1000mVs = data[:,2]
data = np.loadtxt('CV10000mVs_ir.txt', delimiter=',')
E10000mVs = data[:,1]
i10000mVs = data[:,2]

sr_ir = np.array([0.01, 0.1, 1, 10])
plt.figure(4)
plt.plot(E10mVs, i10mVs*1e3/np.sqrt(sr_ir[0]), label='10 mV s$^{-1}$')
plt.plot(E100mVs, i100mVs*1e3/np.sqrt(sr_ir[1]), label='100 mV s$^{-1}$')
plt.plot(E1000mVs, i1000mVs*1e3/np.sqrt(sr_ir[2]), label='1 V s$^{-1}$')
plt.plot(E10000mVs, i10000mVs*1e3/np.sqrt(sr_ir[3]), label='10 V s$^{-1}$')
plt.xlabel('$E$ / V', fontsize=12)
plt.ylabel(r'$i \nu^{-1/2}$ / mC V$^{-1/2}$ s$^{-1/2}$', fontsize=12)
plt.legend(loc=2, fontsize=12)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.tight_layout()



plt.show()
