# Netiesinio modeliavimo metodai, 2 užduotis, Nr. 26
# Lygtis H:  u_t = (a^2 + i) u_xx + beta * (|u|^2 u)_x + f(x,t),  0 < x < 1
# Algoritmas H1, kraštinės sąlygos II:  u_0 = u_1,  u_N = u_{N-1}
import argparse

import numpy as np

parser = argparse.ArgumentParser(description="NMM 2 užduotis, Nr. 26 (H, H1, II)")
parser.add_argument("--a", type=float, default=1.0)
parser.add_argument("--beta", type=float, default=1.0)
parser.add_argument("--T", type=float, default=1.0)
parser.add_argument("--delta", type=float, default=1e-8)
parser.add_argument("--N", type=int, default=100)
parser.add_argument("--tau", type=float, default=0.01)
args = parser.parse_args()

a = args.a
beta = args.beta
T = args.T
delta = args.delta


def u_tikslus(x, t):
    return (1 + 1j * t) * np.sin(np.pi * x) ** 2


def f(x, t):
    # f = u_t - (a^2+i) u_xx - beta (|u|^2 u)_x, kai u = u_tikslus
    z = 1 + 1j * t
    s = np.sin(np.pi * x)
    c = np.cos(np.pi * x)
    u_t = 1j * s ** 2
    u_xx = 2 * np.pi ** 2 * z * np.cos(2 * np.pi * x)
    netiesinis_x = 6 * np.pi * (1 + t ** 2) * z * s ** 5 * c
    return u_t - (a ** 2 + 1j) * u_xx - beta * netiesinis_x


def perkelties_metodas(C, F):
    # Sprendžia y_{j-1} - C y_j + y_{j+1} = -F_j (j = 1..N-1), y_0 = y_1, y_N = y_{N-1}.
    # F[j] naudojami tik j = 1..N-1.
    N = len(F) - 1
    alfa = np.zeros(N + 1, dtype=complex)
    beta_k = np.zeros(N + 1, dtype=complex)
    alfa[1] = 1.0  # y_0 = 1 * y_1 + 0
    beta_k[1] = 0.0
    for j in range(1, N):
        alfa[j + 1] = 1 / (C - alfa[j])
        beta_k[j + 1] = (beta_k[j] + F[j]) / (C - alfa[j])

    y = np.zeros(N + 1, dtype=complex)
    y[N] = beta_k[N] / (1 - alfa[N])  # iš y_N = y_{N-1}
    for j in range(N - 1, -1, -1):
        y[j] = alfa[j + 1] * y[j + 1] + beta_k[j + 1]
    return y


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
        u_old = u.copy()  # pirmoji iteracija: û_old = u
        while True:
            w = (u_old + u) / 2
            g = np.abs(w) ** 2 * w
            F = np.zeros(N + 1, dtype=complex)
            F[1:N] = (u[2:] - 2 * u[1:N] + u[:N - 1]
                      + 2 * h ** 2 / (k * tau) * u[1:N]
                      + 2 * h ** 2 / k * (beta * (g[2:] - g[:N - 1]) / (2 * h) + f_vid[1:N]))
            u_new = perkelties_metodas(C, F)
            if np.max(np.abs(u_new - u_old)) < delta:
                break
            u_old = u_new
        u = u_new
        t += tau
        max_paklaida = max(max_paklaida, np.max(np.abs(u - u_tikslus(x, t))))
    return max_paklaida


def testas1_netiktis():
    # Įstatome tikslų sprendinį į algoritmą viename taške (x, t)
    print("1 testas. Algoritmo netiktis taške x = 0.39, t = 0.57")
    x, t = 0.39, 0.57
    h = tau = 0.1
    k = a ** 2 + 1j
    ankstesne = None
    for _ in range(5):
        u_m, u_0, u_p = u_tikslus(x - h, t), u_tikslus(x, t), u_tikslus(x + h, t)
        v_m, v_0, v_p = u_tikslus(x - h, t + tau), u_tikslus(x, t + tau), u_tikslus(x + h, t + tau)
        w_m, w_p = (v_m + u_m) / 2, (v_p + u_p) / 2
        netiktis = abs((v_0 - u_0) / tau
                       - k / 2 * ((v_p - 2 * v_0 + v_m) / h ** 2 + (u_p - 2 * u_0 + u_m) / h ** 2)
                       - beta * (abs(w_p) ** 2 * w_p - abs(w_m) ** 2 * w_m) / (2 * h)
                       - (f(x, t + tau) + f(x, t)) / 2)
        santykis = f"  sumažėjo {ankstesne / netiktis:.1f} kartų" if ankstesne else ""
        print(f"  h = tau = {h:.0e}:  netiktis = {netiktis:.3e}{santykis}")
        ankstesne = netiktis
        h /= 10
        tau /= 10


def testas2_perkelties_metodas():
    print("\n2 testas. Perkelties metodas")
    N = 20
    C = 2.5 + 1j
    y_tikslus = np.array([np.cos(j) + 1j * j for j in range(N + 1)], dtype=complex)
    y_tikslus[0] = y_tikslus[1]
    y_tikslus[N] = y_tikslus[N - 1]
    F = np.zeros(N + 1, dtype=complex)
    for j in range(1, N):
        F[j] = -(y_tikslus[j - 1] - C * y_tikslus[j] + y_tikslus[j + 1])
    y = perkelties_metodas(C, F)
    print(f"  max |y - y_tikslus| = {np.max(np.abs(y - y_tikslus)):.3e}")


def testas3_paklaida():
    print(f"\n3 testas. Maksimali paklaida, kai T = {T}")
    ankstesne = None
    for N in [10, 20, 40, 80, 160]:
        tau = 1 / N
        paklaida = sprendimas(N, tau)
        santykis = f"  sumažėjo {ankstesne / paklaida:.2f} kartų" if ankstesne else ""
        print(f"  N = {N:4d}, h = tau = {1 / N:.5f}:  paklaida = {paklaida:.3e}{santykis}")
        ankstesne = paklaida


testas1_netiktis()
testas2_perkelties_metodas()
testas3_paklaida()

print(f"\nSkaičiavimas su N = {args.N}, tau = {args.tau}: "
      f"paklaida = {sprendimas(args.N, args.tau):.3e}")
