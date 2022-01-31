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
    if sys.argv[0] == "saldo.py":
        akcja = Saldo()
        status = akcja.dostep_argv("argv")
        if not status:
            print("niewlasciwy status dostepu")
        status, konto = akcja.wykonaj(konto, magazyn)
        if not status:
            print('niewlasciwy status wykonaj')
        historia.append(akcja)
    print(konto)
with open('konto1.txt', "w") as plik:
    for akcja in historia:
        akcja.zapisz(plik)
