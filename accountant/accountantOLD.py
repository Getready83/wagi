import sys

historia = []
magazyn = {}
przeglad = []
konto = 0


while True:
    dostep = input()
    if dostep != "saldo" and dostep != "zakup" and dostep != "sprzedaz":
        break
    if dostep == "saldo":
        kwota = int(input())
        konto = konto + kwota
        if konto < 0:
            print("Brak srodkow")
            break
        komentarz = input()
        historia.append("saldo")
        historia.append(kwota)
        historia.append(komentarz)
        zdarzenie = "saldo", kwota, komentarz
        przeglad.append(zdarzenie)
    if dostep == "zakup":
        nazwa = input()
        cena = int(input())
        ilosc = int(input())
        if konto - (cena * ilosc) < 0:
            print("Nie masz wystarczających środków finansowych."
                  "Twoje saldo to:", konto)
            continue
        if nazwa in magazyn:
            magazyn[nazwa] += ilosc
        else:
            magazyn[nazwa] = ilosc
        konto -= cena * ilosc
        historia.append("zakup")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        zdarzenie = "zakup", nazwa, cena, ilosc
        przeglad.append(zdarzenie)
    if dostep == "sprzedaz":
        nazwa = input()
        if nazwa not in magazyn:
            print("Nie ma w magazynie")
            continue
        cena = int(input())
        ilosc = int(input())
        if nazwa in magazyn:
            if magazyn[nazwa] - ilosc >= 0:
                magazyn[nazwa] -= ilosc
                konto += cena * ilosc
            else:
                print("za mała ilosc w magazynie")
                continue
        historia.append("sprzedaz")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
        zdarzenie = "sprzedaz", nazwa, cena, ilosc
        przeglad.append(zdarzenie)
if len(sys.argv) > 1:
    if sys.argv[1] == "historia":
        for a in historia:
            print(a)
    if sys.argv[1] == "magazyn":
        nazwa = sys.argv[2] and sys.argv[3] and sys.argv[4]
        if nazwa not in magazyn:
            magazyn[nazwa] = 0
        if nazwa in magazyn:
            for nazwa, ilosc in magazyn.items():
                print("{}: {}".format(nazwa, ilosc))
    if sys.argv[1] == "konto":
        print(konto)
    if sys.argv[1] == "przeglad":
        od = int(sys.argv[2])
        do = int(sys.argv[3])
        for wiersz in przeglad[od:do+1]:
            for element in wiersz:
                print(element)
    if sys.argv[1] == "zakup":
        nazwa = sys.argv[2]
        cena = int(sys.argv[3])
        ilosc = int(sys.argv[4])
        if konto - (cena * ilosc) < 0:
            print("Nie masz wystarczających środków finansowych."
                  "Twoje saldo to:", konto)
        if nazwa in magazyn:
            magazyn[nazwa] += ilosc
        else:
            magazyn[nazwa] = ilosc
        konto -= cena * ilosc
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
        else:
            cena = int(sys.argv[3])
            ilosc = int(sys.argv[4])
            if nazwa in magazyn:
                if magazyn[nazwa] - ilosc >= 0:
                    magazyn[nazwa] -= ilosc
                    konto += cena * ilosc
                else:
                    print("za mała ilosc w magazynie")
            historia.append("sprzedaz")
            historia.append(nazwa)
            historia.append(cena)
            historia.append(ilosc)
            zdarzenie = "sprzedaz", nazwa, cena, ilosc
            przeglad.append(zdarzenie)
    if sys.argv[1] in ("zakup", "sprzedaz"):
        for b in historia:
            print(b)
    if dostep == "stop":
        print("stop")
