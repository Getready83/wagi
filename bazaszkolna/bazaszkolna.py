
class Wychowawca:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasy = []

    def wczytanie_wychowawcy(self):
        imie_nazwisko = input()
        klasy = []
        while True:
            klasa = input()
            if not klasa:
                break
            klasy.append(klasa)
        self.klasy = klasy
        self.imie_nazwisko = imie_nazwisko

class Nauczyciel:
    def __init__(self):
        self.imie_nazwisko = ""
        self.przedmiot = ""
        self.klasy = []

    def wczytanie_nauczyciela(self):
        imie_nazwisko = input()
        przedmiot = input()
        klasy = []
        while True:
            klasa = input()
            if not klasa:
                break
            klasy.append(klasa)
        self.imie_nazwisko = imie_nazwisko
        self.przedmiot = przedmiot
        self.klasy = klasy

class Uczen:
    def __init__(self):
        self.imie_nazwisko = ""
        self.klasa = ""

    def wczytywanie_ucznia(self):
        imie_nazwisko = input()
        klasa = input()
        self.imie_nazwisko = imie_nazwisko
        self.klasa = klasa

wychowawcy = []
nauczyciele = []
przedmioty = []
uczniowie = []
numer_klasy = []

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
print(uczniowie)
