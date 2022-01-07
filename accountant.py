import sys

historia = []
magazyn = {}
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
        zdarzenie = nazwa, ilosc
        historia.append("zakup")
        historia.append(nazwa)
        historia.append(cena)
        historia.append(ilosc)
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
print(historia)
print(magazyn)
print(saldo)
if len(sys.argv) < 3:
    if sys.argv[1] == "saldo":
        print(saldo)
    if sys.argv[1] == "historia":
        for i in historia:
            print(i)
    if sys.argv[1] == "magazyn":
        for k, v in magazyn.items():
            print("{}: {}" .format(k, v))




"""historia == sys.argv[1]
for i in range(1,len(historia)):
    print(historia)

#dostep = sys.argv[1]

log = [historia,saldo,magazyn]
for nr in sys.argv[1]:
saldo = sys.argv[1]
print(sys.argv[1])
#historia = sys.argv[1]
"""
