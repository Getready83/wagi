import sys

"""a = sys.argv[1]
b = sys.argv[1]
c = sys.argv[1]
if sys.argv[1] != "saldo" and sys.argv[1] != "zakup" and sys.argv[1] != "sprzedaz":
    print("Niewłaściwe polecenie")
"""

historia = []
magazyn = {}
saldo = 0
while True:
    dostep = input("podaj akcję: ")
    if dostep != "saldo" and dostep != "zakup" and dostep != "sprzedaz": #and dostep != "stop":
        print("Niewłaściwe polecenie")
        break
    if dostep == "saldo":
        kwota = int(input("Podaj kwote: "))
        saldo = saldo + kwota
        if saldo < 0:
            print("Brak srodkow")
            break
        komentarz =(input("Komentarz: "))
        historia.append("saldo")
        historia.append(kwota)
        historia.append(komentarz)
    if dostep == "zakup":
        nazwa = input("Podaj nazwę produktu: ")
        cena = int(input("Podaj cenę: "))
        ilosc = int(input("Podaj ilość:"))
        if saldo - (cena * ilosc) < 0:
            print("Nie masz wystarczających środków finansowych."
                  "Twoje saldo to:",saldo)
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
#    if dostep == "stop":
for i in historia[1:]:
    print(i)
print(saldo)
for k, v in magazyn.items():
    print("{}: {}" .format(k, v))

#dostep = sys.argv[1]

"""log = [historia,saldo,magazyn]
for nr in sys.argv[1]:
saldo = sys.argv[1]
print(sys.argv[1])
#historia = sys.argv[1]
"""
