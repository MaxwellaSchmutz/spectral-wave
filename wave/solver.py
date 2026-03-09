import numpy as np

def build_hamiltonian(A, V_func, lattice_points):
    """
    Build full Hamiltonian matrix for finite lattice.
    """

    L = A.shape[0]
    N = len(lattice_points)

    dim = L * N
    H = np.zeros((dim, dim), dtype=complex)

    for idx, n in enumerate(lattice_points):

        # Block index
        i = idx * L

        # Potential term
        Vn = V_func(n)
        H[i:i+L, i:i+L] += Vn

        # Coupling to n+1
        if idx < N - 1:
            j = (idx + 1) * L
            H[i:i+L, j:j+L] += A.conj().T
            H[j:j+L, i:i+L] += A

    return H


def gaussian_packet(lattice_points, L, center, width, k0):
    """
    Initial wave packet.
    """

    psi = []

    for n in lattice_points:
        envelope = np.exp(-(n - center)**2 / (2 * width**2))
        phase = np.exp(1j * k0 * n)
        vec = envelope * phase * np.ones(L)
        psi.append(vec)

    return np.concatenate(psi)


def evolve(H, psi0, dt, steps):
    from scipy.linalg import expm

    U = expm(-1j * H * dt)

    psi = psi0.copy()
    states = [psi.copy()]

    for _ in range(steps):
        psi = U @ psi
        states.append(psi.copy())

    return states