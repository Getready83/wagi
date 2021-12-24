import sys


waga_paczki = 0
suma_kilogramow = 0
paczki_zamkniete = 0
puste_kilogramy = 0
max_pustych = 0
numer_paczki_pustych = 0

print("Witamy w uniwersalnym zautomatyzowanym pakowaczu")
for nr in range(int(sys.argv[1])):

    print("podaj wagę: ")
    waga_elementu = float(input())
    suma_kilogramow = suma_kilogramow + waga_elementu
#    waga_paczki = waga_paczki + waga_elementu
#    print("całkowita waga elementow :", suma_kilogramow)
    if waga_elementu == 0:
        print("Koniec wysłania")
        break
    if waga_elementu < 1:
        print("Blad !!! niewłaściwa waga przedmiotu, prosze podac wage "
              "w przedziale od 1 kg do 10 kg")
        break
    if waga_elementu > 10:
        print("Blad !!! niewłaściwa waga przedmiotu, prosze podac wage "
              "w przedziale od 1 kg do 10 kg")
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
            numer_paczki_pustych = paczki_zamkniete
            max_pustych = puste_kilogramy



#   ilosc_pustych_kilogramow =
#   ilość_paczek = paczka1 + paczka2 + paczka3


#    if waga_paczki >= 20:
#       print("nastepna paczka")





if waga_paczki > 0:
    paczki_zamkniete += 1
    puste_kilogramy = 20 - waga_paczki
    if puste_kilogramy > max_pustych:
        numer_paczki_pustych = paczki_zamkniete
        max_pustych = puste_kilogramy
print(f"liczba paczek wysłanych {paczki_zamkniete} szt")
print(f"Suma kilogramów wysłanych {suma_kilogramow} kg")
print (f"liczba pustych kilogramów {puste_kilogramy} kg")
print(f" która paczka miała najwiecej pustych kilogramów {numer_paczki_pustych}!!!")