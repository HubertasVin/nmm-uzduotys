def logistinis(x, r):
    return r * x * (1 - x)


def baito_intervalas(s):
    return s / 256, (s + 1) / 256


def sifruoti(data, r, x0):
    c, x = [], x0
    for s in data:
        n = 0
        lo, hi = baito_intervalas(s)
        while not (lo <= x < hi):
            x = logistinis(x, r)
            n += 1
        c.append(n)
    return c


def ivestis():
    r = float(input("raktas r: "))
    x0 = float(input("raktas x0: "))
    return r, x0


def nuskaityti_duomenis():
    pasirinkimas = input("b = byla, f = frazė: ")
    if pasirinkimas == "b":
        return open(input("Bylos pavadinimas: "), "rb").read()
    else:
        return input("Frazė: ").encode()


def main():
    r, x0 = ivestis()
    c = sifruoti(nuskaityti_duomenis(), r, x0)
    open("sifras.txt", "w").write(" ".join(map(str, c)))
    print("Šifras -> sifras.txt:", " ".join(map(str, c[:15])), "...")


if __name__ == "__main__":
    main()
