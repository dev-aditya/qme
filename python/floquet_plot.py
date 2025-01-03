import matplotlib.pyplot as plt
from tqdm import tqdm

# input
measvec = np.array([1, 0])
epsilon = 0.2
Deltas = np.linspace(-6, 6, 600)
omega = 1.5
n_ph = 13
Vs = [0.05, 0.2, 1]
sx, sz = np.array([[0, 1], [1, 0]]), np.array([[1, 0], [0, -1]])

# allocate memory
abs_av = np.zeros((len(Deltas), len(Vs)))
spec = np.zeros((2, len(Deltas)))

# compute
for iD, Delta in enumerate(tqdm(Deltas)):
    for iV, V in enumerate(Vs):
        H0 = Delta / 2 * sz + epsilon * sx
        evals_un, evecs_un = sp.sparse.linalg.eigsh(H0)
        # sort
        evals = np.sort(evals_un)
        evecs = evecs_un[:, evals_un.argsort()]
        spec[:, iD] = np.sort(evals)
        Hint = V * sz / 2
        abs_av[iD, iV] = floquet(H0, Hint, omega, n_ph, measvec)

fig, ax = plt.subplots(2, 1, figsize=(8, 5))
ax[0].plot(Deltas / omega, spec[1], "b-", label=r"$\lambda_e$")
ax[0].plot(Deltas / omega, spec[0], "r-", label=r"$\lambda_g$")
ax[0].legend()
ax[0].set_ylabel(r"Energy")
ax[0].vlines(
    [k for k in range(-3, 3 + 1) if k != 0],
    -4,
    4,
    linestyles="dashed",
    linewidths=1,
    colors="black",
    alpha=0.5,
)
ax[1].vlines(
    [k for k in range(-3, 3 + 1) if k != 0],
    0,
    1,
    linestyles="dashed",
    linewidths=1,
    colors="black",
    alpha=0.5,
)
ax[1].plot(Deltas / omega, abs_av.T[0], label="V = " + str(Vs[0]))
ax[1].plot(
    Deltas / omega, abs_av.T[1], linestyle=(5, (10, 1)), label="V = " + str(Vs[1])
)
ax[1].plot(Deltas / omega, abs_av.T[2], "--", label="V = " + str(Vs[2]))
ax[1].legend()
ax[1].set_xlabel(r"detuning ($\delta$)")
ax[1].set_ylabel(r"Absorption probability")
fig.savefig("figures/floquet.pdf")
