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
if sys.argv[0] == "przeglad.py":
    with open("przeglad.txt", "w") as plik:
        for akcja in historia[int(sys.argv[2]): int(sys.argv[3]) + 1]:
            print(akcja.zapisz(plik))
