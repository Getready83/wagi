import sys

waga_paczki = 0
suma_kilogramow = 0
paczki_zamkniete = 0
puste_kilogramy = 0
max_pustych = 0
nr_paczki_zamknietej = 0
suma_pustych_kilogramow = 0
blad = False
print("Witamy w uniwersalnym zautomatyzowanym pakowaczu")
for nr in range(int(sys.argv[1])):

    print("podaj wagę: ")
    waga_elementu = float(input())
    suma_kilogramow = suma_kilogramow + waga_elementu

    if waga_elementu == 0:
        print("Koniec wysłania")
        break
    if waga_elementu < 1:
        blad = True
        print("Blad !!! niewłaściwa waga przedmiotu, prosze podac wage "
              "w przedziale od 1 kg do 10 kg\n Zacznij od początku !!!")
        break
    if waga_elementu > 10:
        blad = True
        print("Blad !!! niewłaściwa waga przedmiotu, prosze podac wage "
              "w przedziale od 1 kg do 10 kg\n Zacznij od początku !!!")
        break

    if waga_paczki + waga_elementu <= 20:
        waga_paczki = waga_paczki + waga_elementu
    else:
        paczki_zamkniete = paczki_zamkniete + 1
        puste_kilogramy = 20 - waga_paczki
        waga_paczki = 0 + waga_elementu
        print("nr paczki", paczki_zamkniete)
        print("waga:", waga_paczki)
        if puste_kilogramy > max_pustych:
            nr_paczki_zamknietej = paczki_zamkniete
            max_pustych = puste_kilogramy

if waga_paczki > 0:
    paczki_zamkniete += 1
    puste_kilogramy = 20 - waga_paczki
    suma_pustych_kilogramow = paczki_zamkniete * 20 - suma_kilogramow
    if puste_kilogramy > max_pustych:
        nr_paczki_zamknietej = paczki_zamkniete
        max_pustych = puste_kilogramy

if not blad:
    print(f"Ilośc wysłanych paczek {paczki_zamkniete} szt")
    print(f"Waga wysłanych paczek {suma_kilogramow} kg")
    print(f"Pustych kilogramów: {suma_pustych_kilogramow} kg")
    print(f"Paczka nr {nr_paczki_zamknietej} miała najwieciej pustych kg.")
