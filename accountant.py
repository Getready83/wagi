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
        przeglad == historia
    if dostep == "zakup":  #and sys.argv[1] == "zakup":
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
        zdarzenie = nazwa, ilosc
        historia.append("zakup")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        przeglad = "zakup", nazwa, cena, ilosc
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
                saldo -= cena * ilosc
                print("za mała ilosc w magazynie")
        historia.append("sprzedaz")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        if sys.argv[1] == "zakup":
            nazwa = sys.argv[2]
            cena = int(sys.argv[3])
            ilosc = int(sys.argv[4])
            if saldo - (cena * ilosc) < 0:
                print("Nie masz wystarczających środków finansowych."
                      "Twoje saldo to:", saldo)
                continue
            if nazwa in magazyn:
                magazyn[nazwa] += ilosc
            else:
                magazyn[nazwa] = ilosc
            saldo -= cena * ilosc
            zdarzenie = nazwa, ilosc
            historia.append("zakup")
            historia.append(nazwa)
            historia.append(cena)
            historia.append(ilosc)
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
                    saldo -= cena * ilosc
                    print("za mała ilosc w magazynie")
            historia.append("sprzedaz")
            historia.append(nazwa)
            historia.append(cena)
            historia.append(ilosc)
print(przeglad)

"""print(historia)
print(magazyn)
print(saldo)"""
#while True:
a = len(sys.argv)
for nr in range(a - 1):
#if len(sys.argv) < 5:
    if sys.argv[1] == "saldo":
        print(saldo)
    if sys.argv[1] == "historia" or "zakup" or "sprzedaz":
        for i in historia:
            print(i)
    if sys.argv[1] == "magazyn":
        for k, v in magazyn.items():
            print("{}: {}" .format(k, v))
    if sys.argv[1] == "przeglad":
        print(przeglad)

