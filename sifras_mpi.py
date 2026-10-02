import argparse
import time

from mpi4py import MPI

intervalu_sk = 256
iteraciju_sk = 100000


def logistinis(x, r):
    return r * x * (1 - x)


def baito_intervalas(s):
    return s / intervalu_sk, (s + 1) / intervalu_sk


def sifruoti(data, r, x0):
    hi = r / 4
    olo = logistinis(hi, r)
    w = (hi - olo) / intervalu_sk
    rez = []
    for s in data:
        blo = olo + s * w
        x = x0
        n = 0
        while not (blo <= x < blo + w):
            x = logistinis(x, r)
            n += 1
            if n > iteraciju_sk:
                return None
        rez.append(n)
    return rez


def vidurkis(e):
    return None if e is None else sum(e) / len(e)


def argumentai():
    parser = argparse.ArgumentParser(description="Sifro metrikos priklausomybes nuo r skenavimas su MPI")
    parser.add_argument("-r", type=float, nargs="+", required=True, help="tikrinamos r vertes")
    parser.add_argument("-x0", type=float, default=0.2, help="raktas x0")
    parser.add_argument("-f", "--file", help="byla su duomenimis")
    parser.add_argument("tekstas", nargs="?", help="sifruojama fraze (jei nera -f)")
    args = parser.parse_args()
    if not all(3.5 < r <= 4 for r in args.r) or not (0 < args.x0 < 1):
        parser.error("r-vertes turi buti 3.57 < r <= 4 ir 0 < x0 < 1")
    if not args.file and args.tekstas is None:
        parser.error("nurodykite fraze arba -f byla")
    return args


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    args = argumentai()

    data = None
    if rank == 0:
        data = open(args.file, "rb").read() if args.file else args.tekstas.encode()
        pradzia = time.time()
    data = comm.bcast(data, root=0)
    mano_r = args.r[rank::size]

    mano_rez = [(r, vidurkis(sifruoti(data, r, args.x0))) for r in mano_r]

    rezultatai = comm.gather(mano_rez, root=0)
    if rank == 0:
        pabaiga = time.time()
        visi = sorted(x for rez in rezultatai for x in rez)
        print(f"Procesu sk.: {size} | Laikas: {pabaiga - pradzia:.2f} s")
        print(f"{'r':>10} | {'vid. iteraciju':>14}")
        print("-" * 27)
        for r, e in visi:
            e_str = "-" if e is None else f"{e:.4f}"
            print(f"{r:>10.4f} | {e_str:>16}")

if __name__ == "__main__":
    main()
