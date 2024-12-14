from sympy import *

# real variables
a, Gamma, Omega, Delta = symbols("a Gamma Omega Delta", real=True)
# complex variables
b = symbols("b")
# general TLS density operator
rho = Matrix([[a, b], [conjugate(b), 1 - a]])
# Hamiltonian
H_s = Matrix([[0, Omega], [Omega, Delta]])
# Linblad operator
L = Matrix([[0, 1], [0, 0]])
# Generator
rho_dot = (-1j) * (H_s * rho - rho * H_s) + Gamma * (
    L * rho * L.H - (1 / 2) * (L.H * L * rho + rho * (L.H) * L)
)
# Steady state solution for Omega = 0
rho_dot = rho_dot.subs(Omega, 0)
sol = solve(flatten(rho_dot), [a, b], dict=True)
# steady state
rho_ss = rho.subs(sol[0])
