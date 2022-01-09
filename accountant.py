import sys

historia = []
magazyn = {}
przeglad = []
saldo = 0
while True:
    dostep = input("podaj akcję: ")
    if dostep != "saldo" and dostep != "zakup" and dostep != "sprzedaz":
        print("Niewłaściwe polecenie")
        break
    if dostep == "saldo":
        kwota = int(input("Podaj kwote: "))
        saldo = saldo + kwota
        if saldo < 0:
            print("Brak srodkow")
            break
        komentarz = (input("Komentarz: "))
        historia.append("saldo")
        historia.append(kwota)
        historia.append(komentarz)
        zdarzenie = "saldo", kwota, komentarz
        przeglad.append(zdarzenie)
    if dostep == "zakup":
        nazwa = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę: "))
        ilosc = int(input("Podaj ilość:"))
        if saldo - (cena * ilosc) < 0:
            print("Nie masz wystarczających środków finansowych."
                  "Twoje saldo to:", saldo)
            continue
        if nazwa in magazyn:
            magazyn[nazwa] += ilosc
        else:
            magazyn[nazwa] = ilosc
        saldo -= cena * ilosc
        historia.append("zakup")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        zdarzenie = "zakup", nazwa, cena, ilosc
        przeglad.append(zdarzenie)
    if dostep == "sprzedaz":
        nazwa = input("Podaj nazwę produktu: ")
        if nazwa not in magazyn:
            print("Nie ma takiego produktu")
            continue
        cena = int(input("Podaj cenę: "))
        ilosc = int(input("Podaj ilość:"))
        if nazwa in magazyn:
            if magazyn[nazwa] - ilosc >= 0:
                magazyn[nazwa] -= ilosc
                saldo += cena * ilosc
            else:
                print("za mała ilosc w magazynie")
                continue
        historia.append("sprzedaz")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        zdarzenie = "sprzedaz", nazwa, cena, ilosc
        przeglad.append(zdarzenie)
        if sys.argv[1] == "zakup":
            nazwa = sys.argv[2]
            cena = int(sys.argv[3])
            ilosc = int(sys.argv[4])
            if saldo - (cena * ilosc) < 0:
                print("Nie masz wystarczających środków finansowych."
                      "Twoje saldo to:", saldo)
            if nazwa in magazyn:
                magazyn[nazwa] += ilosc
            else:
                magazyn[nazwa] = ilosc
            saldo -= cena * ilosc
            historia.append("zakup")
            historia.append(nazwa)
            historia.append(cena)
            historia.append(ilosc)
            zdarzenie = "zakup", nazwa, cena, ilosc
            przeglad.append(zdarzenie)
        if sys.argv[1] == "sprzedaz":
            nazwa = sys.argv[2]
            if nazwa not in magazyn:
                print("Nie ma takiego produktu")
                continue
            cena = int(sys.argv[3])
            ilosc = int(sys.argv[4])
            if nazwa in magazyn:
                if magazyn[nazwa] - ilosc >= 0:
                    magazyn[nazwa] -= ilosc
                    saldo += cena * ilosc
                else:
                    print("za mała ilosc w magazynie")
                    continue
            historia.append("sprzedaz")
            historia.append(nazwa)
            historia.append(cena)
            historia.append(ilosc)
            zdarzenie = "sprzedaz", nazwa, cena, ilosc
            przeglad.append(zdarzenie)

"""print(historia)
print(magazyn)
print(saldo)
print(przeglad)
while True:"""

#  for i in range(len(sys.argv)):
for i in range(1):
    if sys.argv[1] == "historia":
        for a in historia:
            print(a)
    if sys.argv[1] == "magazyn":
        for k, v in magazyn.items():
            print("{}: {}" .format(k, v))
    if sys.argv[1] == "saldo":
        print(saldo)
    if sys.argv[1] == "przeglad":
        od = int(sys.argv[2])
        do = int(sys.argv[3])
        print(przeglad[od:do])
    if sys.argv[1] == "zakup" or "sprzedaz":  # ??????
        for b in historia:
            print(b)

# jak można zlikwidowac linie komend w outpucie ???
# cos nie gra z zakup i sprzedaz sys.argv ????
# przy saldzie drukuje mi sie historia
# czy konto i saldo to to samo ???
# zostało spradzenie magazynu po nazwie
