import sys

osoby = {}
grupy = {}


def pobierz_numer_grupy(numer):
    if numer not in grupy:
        grupa = GrupaSzkolna(numer)
        grupy[numer] = grupa
    return grupy[numer]


class GrupaSzkolna:
    def __init__(self, numer):
        self.numer = numer
        self.wychowawca = None
        self.nauczyciele = []
        self.uczniowie = []
        self.wychowawcy = []

    def numer_klasy(self):
        self.numer = True

    def drukuj(self):
        print(self.wychowawca.imie_nazwisko)
        for uczen in self.uczniowie:  # wyszukujemy danych dla ucznia
            print(uczen.imie_nazwisko)


class Wychowawca:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasy = []

    def wczytanie(self):
        self.imie_nazwisko = input()
        self.klasy = []
        while True:
            klasa = input()
            if not klasa:
                break
            self.klasy.append(klasa)
            grupa = pobierz_numer_grupy(klasa)
            grupa.wychowawca = self
            grupa.wychowawcy.append(self)

    def drukuj(self):
        for klasa in self.klasy:
            print(klasa)
            for uczen in grupy[klasa].uczniowie:
                print(uczen.imie_nazwisko)


class Nauczyciel:
    def __init__(self):
        self.imie_nazwisko = ""
        self.przedmiot = ""
        self.klasy = []

    def wczytanie(self):
        self.imie_nazwisko = input()
        self.przedmiot = input()
        self.klasy = []
        while True:
            klasa = input()
            if not klasa:
                break
            self.klasy.append(klasa)
            grupa = pobierz_numer_grupy(klasa)
            grupa.nauczyciele.append(self)

    def drukuj(self):
        for klasa in self.klasy:
            for wychowawca in grupy[klasa].wychowawcy:
                print(wychowawca.imie_nazwisko)


class Uczen:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasa = ""

    def wczytanie(self):
        self.imie_nazwisko = input()
        self.klasa = input()
        grupa = pobierz_numer_grupy(self.klasa)
        grupa.uczniowie.append(self)

    def drukuj(self):
        for nauczyciel in grupy[self.klasa].nauczyciele:
            print(nauczyciel.przedmiot, "\n", nauczyciel.imie_nazwisko)

while True:

    typ_uzytkownika = input()
    if typ_uzytkownika == "koniec":
        break
    if typ_uzytkownika == "wychowawca":
        osoba = Wychowawca()
        grupa = Wychowawca()
    if typ_uzytkownika == "nauczyciel":
        osoba = Nauczyciel()
    if typ_uzytkownika == "uczen":
        osoba = Uczen()

    osoba.wczytanie()
    osoby[osoba.imie_nazwisko] = osoba

phrase = (sys.argv[1])
if phrase in grupy:
    grupy[phrase].drukuj()
if phrase in osoby:
    osoby[phrase].drukuj()