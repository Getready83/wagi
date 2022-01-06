#import sys

"""a = sys.argv[1]
b = sys.argv[1]
c = sys.argv[1]
if sys.argv[1] != "saldo" and sys.argv[1] != "zakup" and sys.argv[1] != "sprzedaz":
    print("Niewłaściwe polecenie")
"""

saldo_lista = []
magazyn = {}
#magazyn ["raspbbery"] = 4
zdarzenie = 0
kwota = 0
saldo = 0
while True:
    dostep = input("podaj akcję: ")
    if dostep == "saldo":
        kwota = int(input("Podaj kwote: "))
        saldo = saldo + kwota
        if saldo < 0:
            print("Brak srodkow")
            break
        komentarz =(input("Komentarz: "))
        zdarzenie = kwota, komentarz
        saldo_lista.append(zdarzenie)


    if dostep != "saldo" and dostep != "zakup" and dostep != "sprzedaz":
        print("Niewłaściwe polecenie")
        break
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
#                magazyn[nazwa]
                saldo -= cena * ilosc
                print("za mała ilosc w magazynie")


 #           magazyn[nazwa] -= ilosc
 #           magazyn[nazwa] += ilosc

print(saldo_lista)
#    print(zdarzenie)
print(saldo)
print(magazyn)
