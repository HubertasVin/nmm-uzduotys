import argparse

intervalu_sk = 256
iteraciju_sk = 100000


def logistinis(x, r):
    return r * x * (1 - x)


def baito_intervalas(s):
    return s / intervalu_sk, (s + 1) / intervalu_sk


def orbitos_ribos(r):
    hi = r / 4
    return logistinis(hi, r), hi


def sifruoti(data, r, x0):
    olo, ohi = orbitos_ribos(r)
    rez = []
    for s in data:
        n = 0
        x = x0
        lo, hi = baito_intervalas(s)
        while not (lo <= (x - olo) / (ohi - olo) < hi):
            x = logistinis(x, r)
            n += 1
            if n > iteraciju_sk:
                raise ValueError(f"Per {n} iteraciju nepavyko rasti tinkamo intervalo; Pasirinkite kitus raktus.")
        rez.append(n)
    return rez


def desifruoti(data, r, x0):
    olo, ohi = orbitos_ribos(r)
    baitai = bytearray()
    for n in data:
        xi = x0
        for _ in range(n):
            xi = logistinis(xi, r)
        s = int(((xi - olo) / (ohi - olo)) * intervalu_sk) % intervalu_sk
        baitai.append(s)

    return baitai.decode("utf-8", "replace")


def ivestis(r, x0):
    if not (3.57 < r <= 4) or not (0 < x0 < 1):
        raise ValueError("Raktai turi buti 3.57 < r <= 4 ir 0 < x0 < 1")
    return r, x0


def nuskaityti_duomenis(failas, fraze):
    if failas:
        return open(failas, "rb").read()
    return fraze.encode()


def main():
    parser = argparse.ArgumentParser(description="Logistine saros sifravimo programa")
    parser.add_argument("-r", type=float, required=True, help="raktas r (3.57 < r <= 4)")
    parser.add_argument("-x0", type=float, required=True, help="raktas x0 (0 < x0 < 1)")
    parser.add_argument("-f", "--file", help="byla su duomenimis sifravimui")
    parser.add_argument("tekstas", nargs="?", help="sifruojama fraze")
    args = parser.parse_args()

    if not args.file and args.tekstas is None:
        parser.error("nurodykite fraze arba -f byla")

    r, x0 = ivestis(args.r, args.x0)
    c = sifruoti(nuskaityti_duomenis(args.file, args.tekstas), r, x0)
    open("sifras.txt", "w").write(" ".join(map(str, c)))
    # print("Šifras -> sifras.txt:", " ".join(map(str, c)))

    # desifruotas = desifruoti(c, r, x0)
    # print("Desifruotas tekstas: ", desifruotas)


if __name__ == "__main__":
    main()
