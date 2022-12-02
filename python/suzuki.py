import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import expm
from qutip import *

superop_1 = liouvillian(sigmax(),c_ops =[sigmap()]) # superoperator 1 using QuTiP
superop_2 = liouvillian(sigmay(),c_ops =[sigmam()]) # superoperator 2 using QuTiP
rho0 = ket2dm(basis(2,0)) # initial state

# plot
fig, ax = plt.subplots()
alpha = [0.2,0.5,1]
    
# number of time steps m for three possible values of m = 50,100 and 1000
for km,m in enumerate([50,100,1000]):
    dt = 10/m # time-step
    d = len(rho0.full()) # dimension or the state
    P_1, P_2 = expm(superop_1.full() * dt), expm(superop_2.full() * dt) # propgators
    P = P_1.dot(P_2) # suzuki-trotter expansion for small times dt
    times_0, pops_0 = [], [] # allocate sets
    t, rho = 0., rho0 # initialise
    # propagate
    for k in range(m):
        pops_0.append( (rho * ket2dm(basis(2,0)) ).tr() ) # append current population
        times_0.append(t) # append current time
        # propagate time and state
        t, rho = t+dt, Qobj(np.reshape(P.dot(np.reshape(rho.full(),(d**2,1))),(d,d)))
    # plot    
    ax.plot(times_0, pops_0, 'b-', label = 'w/ ST @ m = '+str(m), alpha = alpha[km]);

# Hamiltonian and Lindblad operators for exact solution
H, c_ops = sigmax()+sigmay(), [sigmap(),sigmam()]
# time steps
times_1 = np.linspace(times_0[0],times_0[-1],20)
# usig mesolve
pops_1 = mesolve(H,rho0,times_1,c_ops = c_ops, e_ops = [ket2dm(basis(2,0))]).expect[0] 
# plot
ax.plot(times_1, pops_1, 'k.', label = 'exact w/ mesolve', alpha = 0.5);
ax.legend();