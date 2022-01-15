import sys

wychowawcy = []
nauczyciele = []
uczniowie = []
grupy = {}


class GrupaSzkolna:
    def __init__(self, numer):
        self.numer = numer
        self.wychowawca = None
        self.nauczyciele = []
        self.uczniowie = []

    def numer_klasy(self):
        self.numer = True

    def drukuj(self):
        print(self.numer)
        print(self.wychowawca)
        print(self.nauczyciele)
        print(self.uczniowie)


"""def pobierz_numer_grupy(numer):
    if numer not in grupy:
        grupa = GrupaSzkolna(numer)
        grupy[numer] = grupa
    return grupy[numer]
print(grupy)"""


class Wychowawca:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasy = []

    def wczytanie_wychowawcy(self):
        imie_nazwisko = input()
        klasy = []
        self.imie_nazwisko = imie_nazwisko
        self.klasy = klasy
        while True:
            klasa = input()
            if not klasa:
                break
            klasy.append(klasa)
#            grupa = pobierz_numer_grupy(self.klasy)
#            grupa.wychowawca = self

    def drukuj(self):
        print(self.imie_nazwisko)
        print(self.klasy)


class Nauczyciel:
    def __init__(self):
        self.imie_nazwisko = ""
        self.przedmiot = ""
        self.klasy = []

    def wczytanie_nauczyciela(self):
        imie_nazwisko = input()
        przedmiot = input()
        klasy = []
        self.imie_nazwisko = imie_nazwisko
        self.przedmiot = przedmiot
        self.klasy = klasy
        while True:
            klasa = input()
            if not klasa:
                break
            klasy.append(klasa)
#            grupa = pobierz_numer_grupy(self.klasy)
#            grupa.nauczyciel.append(self)

    def drukuj(self):
        print(self.imie_nazwisko)
        print(self.przedmiot)
        print(self.klasy)


class Uczen:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasa = ""

    def wczytywanie_ucznia(self):
        imie_nazwisko = input()
        klasa = input()
        self.imie_nazwisko = imie_nazwisko
        self.klasa = klasa
#        grupa = pobierz_numer_grupy(self.klasa)
#        grupa.uczniowie.append(self)

    def drukuj(self):
        print(self.imie_nazwisko)
        print(self.klasa)


while True:
    typ_uzytkownika = input()
    if typ_uzytkownika == "wychowawca":
        wychowawca = Wychowawca()
        wychowawca.wczytanie_wychowawcy()
        wychowawcy.append(wychowawca)
    if typ_uzytkownika == "nauczyciel":
        nauczyciel = Nauczyciel()
        nauczyciel.wczytanie_nauczyciela()
        nauczyciele.append(nauczyciel)
    if typ_uzytkownika == "uczen":
        uczen = Uczen()
        uczen.wczytywanie_ucznia()
        uczniowie.append(uczen)
    if typ_uzytkownika == "koniec":
        break


if sys.argv[1] in wychowawcy:
    for wychowawca in wychowawcy:
        wychowawca.drukuj()
        print(wychowawca)
"""    
for nauczyciel in nauczyciele:
    nauczyciel.drukuj()
print(nauczyciele)
for uczen in uczniowie:
    uczen.drukuj()
print(uczniowie)
"""