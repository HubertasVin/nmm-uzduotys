import numpy as np
from mpi4py import MPI


a = 1.0
beta = 1.0
T = 1.0
delta = 1e-8
N_sarasas = [15, 40, 80, 160, 320, 640, 1280, 2560, 5120]


def u_tikslus(x, t):
    return (1 + 1j * t) * np.cos(2 * np.pi * x)


def f(x, t):
    z = 1 + 1j * t
    c = np.cos(2 * np.pi * x)
    s = np.sin(2 * np.pi * x)
    u_t = 1j * c
    u_xx = -4 * np.pi ** 2 * z * c
    netiesinis_x = -6 * np.pi * (1 + t ** 2) * z * c ** 2 * s
    return u_t - (a ** 2 + 1j) * u_xx - beta * netiesinis_x


def perkelties_metodas(C, F):
    N = len(F) - 1
    alfa = np.zeros(N + 1, dtype=complex)
    beta_k = np.zeros(N + 1, dtype=complex)
    alfa[1] = 1.0

    for j in range(1, N):
        alfa[j + 1] = 1 / (C - alfa[j])
        beta_k[j + 1] = (beta_k[j] + F[j]) / (C - alfa[j])

    y = np.zeros(N + 1, dtype=complex)
    y[N] = beta_k[N] / (1 - alfa[N])
    for j in range(N - 1, -1, -1):
        y[j] = alfa[j + 1] * y[j + 1] + beta_k[j + 1]
    return y


def sudaryti_F(u, g, f_vid, h, tau, k):
    F = np.zeros(len(u), dtype=complex)
    u_sena = u[2:] - 2 * u[1:-1] + u[:-2]
    g_x = (g[2:] - g[:-2]) / (2 * h)
    F[1:-1] = (
        u_sena
        + 2 * h ** 2 / (k * tau) * u[1:-1]
        + 2 * h ** 2 / k * (beta * g_x + f_vid[1:-1])
    )
    return F


def sprendimas(N, tau):
    h = 1 / N
    x = np.linspace(0, 1, N + 1)
    k = a ** 2 + 1j
    C = 2 + 2 * h ** 2 / (k * tau)
    u = u_tikslus(x, 0)
    t = 0.0
    max_paklaida = 0.0

    while t < T - tau / 2:
        f_vid = (f(x, t) + f(x, t + tau)) / 2
        u_senas = u.copy()

        while True:
            u_vid = (u_senas + u) / 2
            g = np.abs(u_vid) ** 2 * u_vid
            F = sudaryti_F(u, g, f_vid, h, tau, k)
            u_naujas = perkelties_metodas(C, F)
            if np.max(np.abs(u_naujas - u_senas)) < delta:
                break
            u_senas = u_naujas

        u = u_naujas
        t += tau
        max_paklaida = max(
            max_paklaida,
            np.max(np.abs(u - u_tikslus(x, t))),
        )

    return max_paklaida


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    parametru_poros = [(N, 1 / N) for N in N_sarasas]
    mano_poros = parametru_poros[rank::size]

    comm.Barrier()
    pradzia = MPI.Wtime()
    mano_rezultatai = [
        (rank, N, tau, sprendimas(N, tau))
        for N, tau in mano_poros
    ]
    visi_rezultatai = comm.gather(mano_rezultatai, root=0)

    if rank == 0:
        trukme = MPI.Wtime() - pradzia
        rezultatai = sorted(
            (rezultatas for dalis in visi_rezultatai for rezultatas in dalis),
            key=lambda rezultatas: rezultatas[1],
        )
        print(f"4 testas. MPI procesų: {size}; skaičiavimo laikas: {trukme:.2f} s")
        print(f"{'rangas':>6} | {'N':>5} | {'h':>10} | {'tau':>10} | {'didžiausia paklaida':>20}")
        print("-" * 65)
        for rankas, N, tau, paklaida in rezultatai:
            print(
                f"{rankas:>6} | {N:>5} | {1 / N:>10.5f} | {tau:>10.5f} | {paklaida:>20.3e}"
            )


if __name__ == "__main__":
    main()
