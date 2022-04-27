import sys
import csv
from os import listdir, path
zawartosc = []
def sprawdz_wczytaj():
    path.exists(sys.argv[1])
    print(path.exists(sys.argv[1]))
    if not path.exists(sys.argv[1]):
        print(f"Niewłasciwa nazwa pliku lub plik o tej nazwie nie istnieje "
              f"Pliki dostępne w tym katalogu to: {listdir()}\n "
              f"scieżka do katalogu to: {path.dirname(path.abspath(__file__))}"
            )
    with open(sys.argv[1], newline="", encoding="utf-8")as plik:
        reader = csv.reader(plik)
        print(reader)
        for linia in reader:
            print(linia)
            zawartosc.append(linia)

def write():
    with open(sys.argv[2], "w", newline="", encoding="utf-8") as plik:
        writer = csv.writer(plik)
        writer.writerows(zawartosc)

def wykonaj():
    if len(sys.argv) >= 3:
        akcja1 = []
        for n in sys.argv[3:]:
            print(n)
            akcja = n.split(",")
            akcja1.append(akcja)
            for akcja in akcja1:
                y = akcja[0]
                x = akcja[1]
                wartosc = akcja[2]
                if len(zawartosc) <= int(y):
                    print("Plik jest za krótki")
                elif len(zawartosc[int(y)]) <= int(x):
                    print("Kolumna po za zasiegiem")
                else:
                    zawartosc[int(y)][int(x)] = wartosc


sprawdz_wczytaj()
wykonaj()
write()
