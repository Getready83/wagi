import sys
from accountant1 import wczytaj_parametry, Saldo, Zakup, Sprzedaz


historia = []
magazyn = {}
konto = 0

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









