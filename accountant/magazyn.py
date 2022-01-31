import sys
from accountant1 import Saldo, Zakup, Sprzedaz

konto = 0
magazyn = {}
historia = []

with open(sys.argv[1], 'r') as plik:
    while True:
        linia = plik.readline()
        if not linia:
            break
        linia = linia.strip()
        if linia == "saldo":
            akcja = Saldo()
            status = akcja.dostep("plik", plik)
            if not status:
                break
            status, konto = akcja.wykonaj(konto, magazyn)
            if not status:
                break
            historia.append(akcja)
        if linia == "zakup":
            akcja = Zakup()
            status = akcja.dostep("plik", plik)
            if not status:
                break
            status, konto, magazyn = akcja.wykonaj(konto, magazyn)
            if not status:
                break
            historia.append(akcja)
        if linia == "sprzedaz":
            akcja = Sprzedaz()
            status = akcja.dostep("plik", plik)
            if not status:
                break
            status, konto, magazyn = akcja.wykonaj(konto, magazyn)
            if not status:
                break
            historia.append(akcja)
if sys.argv[0] == "magazyn.py":
    nazwa = sys.argv[2]
    nazwa1 = sys.argv[3]
    nazwa2 = sys.argv[4]
    if (nazwa, nazwa1, nazwa2) not in magazyn:
        magazyn[nazwa] = 0
        magazyn[nazwa1] = 0
        magazyn[nazwa2] = 0
    if nazwa in magazyn:
        for nazwa, ilosc in magazyn.items():
            print("{}: {}".format(nazwa, ilosc))
        historia.append(akcja)
with open('ddd.txt', "w") as plik:
    for nazwa, ilosc in magazyn.items():
        plik.write("{} , {} \n".format(nazwa, ilosc))
