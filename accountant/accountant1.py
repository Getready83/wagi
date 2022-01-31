import sys

historia = []
magazyn = {}
konto = 0


def wczytaj_parametry(ilosc_lini, zrodlo, plik=None):
    lista = []
    status = True
    if zrodlo == "plik":
        for numer_lini in range(ilosc_lini):
            linia = plik.readline()
            if not linia:
                return False, lista
            linia = linia.strip()
            lista.append(linia)
        return True, lista
    if zrodlo == "argv":
        if len(sys.argv) >= ilosc_lini + 1:
            return True, sys.argv[1:ilosc_lini+1]
        else:
            return False, sys.argv[1:]


class Saldo:
    def __init__(self):
        self.kwota = 0
        self.komentarz = ""

    def dostep(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(2, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla salda")
            return False
        self.kwota = int(lista[0])
        self.komentarz = lista[1]
        return True

    def dostep_argv(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(2, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla salda")
            return False
        self.kwota = int(sys.argv[2])
        self.komentarz = sys.argv[3]
        return True

    def wykonaj(self, konto, magazyn):
        if self.kwota + konto < 0:
            print("Blad")
            return False, konto
        konto += self.kwota
        return True, konto

    def zapisz(self, plik):
        plik.write("saldo\n")
        plik.write(f"{self.kwota}\n")
        plik.write(f"{self.komentarz}\n")
        return self.kwota, self.komentarz


class Zakup:
    def __init__(self):
        self.nazwa = ""
        self.cena = 0
        self.ilosc = 0

    def dostep(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(3, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla zakup")
            return False
        self.nazwa = (lista[0])
        self.cena = int(lista[1])
        self.ilosc = int(lista[2])
        return True

    def dostep_argv(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(3, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla zakup")
            return False
        self.nazwa = (sys.argv[2])
        self.cena = int(sys.argv[3])
        self.ilosc = int(sys.argv[4])
        return True

    def wykonaj(self, konto, magazyn):
        if konto - (self.cena * self.ilosc) < 0:
            print("Nie masz wystarczających środków finansowych.")
            return False, konto, magazyn
        else:
            if self.nazwa not in magazyn:
                magazyn[self.nazwa] = self.ilosc
                konto -= self.cena * self.ilosc
            else:
                magazyn[self.nazwa] += self.ilosc
                konto -= self.cena * self.ilosc
            return True, konto, magazyn

    def zapisz(self, plik):
        plik.write("zakup\n")
        plik.write(f"{self.nazwa}\n")
        plik.write(f"{self.cena}\n")
        plik.write(f"{self.ilosc}\n")
        return self.nazwa, self.cena, self.ilosc


class Sprzedaz:
    def __init__(self):
        self.nazwa = ""
        self.cena = 0
        self.ilosc = 0

    def dostep(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(3, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla sprzedaz")
            return False
        self.nazwa = (lista[0])
        self.cena = int(lista[1])
        self.ilosc = int(lista[2])
        return True

    def dostep_argv(self, zrodlo, plik=None):
        status, lista = wczytaj_parametry(3, zrodlo, plik)
        if not status:
            print("Blad - niewlasciwe parametry dla sprzedaz")
            return False
        self.nazwa = (sys.argv[2])
        self.cena = int(sys.argv[3])
        self.ilosc = int(sys.argv[4])
        return True

    def wykonaj(self, konto, magazyn):
        if self.nazwa not in magazyn:
            print("Nie ma na stanie magazynu.")
            return False, konto, magazyn
        else:
            if magazyn[self.nazwa] - self.ilosc < 0:
                print("Bląd - nie ma wystarczającej ilosci w magazynie")
                return False, konto, magazyn, magazyn[self.nazwa]
            else:
                magazyn[self.nazwa] -= self.ilosc
                konto += self.cena * self.ilosc
            return True, konto, magazyn

    def zapisz(self, plik):
        plik.write("sprzedaz\n")
        plik.write(f"{self.nazwa}\n")
        plik.write(f"{self.cena}\n")
        plik.write(f"{self.ilosc}\n")
        return self.nazwa, self.cena, self.ilosc
