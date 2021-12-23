# maksymalna waga paczki 20 kg
# każdy element dodawany może ważyć od 1kg do 10kg
# Jeżeli kolejny element przekroczy wagę 20kg paczka powinna zostać wysłana
# - a element dodany do kolejnej paczki
# wszystkie elementy powinny zostać wysłane
# program powinien pobierać ilość elementów do wysłania
# podanie elementu o wadze zero kończy działenie programu tak jakby maksymalna
# liczba paczek została osiągnięta
# na koniec podsumowanie
# program powinien kończyć się błędem gdy element jest większy niż 10kg
# i mniejszy niż 1 kg ale nie jest dokładnie 0
import sys

ilosc_elementow = int(sys.argv[1])
waga_paczki = 0
ilosc_paczek = 0
ilosc_pustych_kilogramow = 0
suma_kilogramow = 0

print("Witamy w uniwersalnym zautomatyzowanym pakowaczu")
for nr in range(ilosc_elementow):

#    print("podaj ile elementów chcesz zapakować: ")
#    ilosc_elementow = int(input())

    print("podaj wagę: ")
    waga_elementu = float(input())
    waga_paczki = waga_paczki + waga_elementu
    suma_kilogramow = waga_paczki
    print("waga :",waga_paczki)

#   ilosc_pustych_kilogramow =
#   ilość_paczek = paczka1 + paczka2 + paczka3
    if waga_elementu == 0:
        print("Koniec wysłania")
        break
    if waga_elementu < 1 or waga_elementow > 10:
        print("Blad !!! niewłaściwa waga przedmiotu, prosze podac wage "
              "w przedziale od 1 kg do 10 kg")
        break

#    if waga_paczki >= 20:
#       print("nastepna paczka")





#print(f"liczba paczek wysłanych {ilosc_paczek} szt")
print(f"Suma kilogramów wysłanych {suma_kilogramow} kg")
#print (f"liczba pustych kilogramów {} kg")
#print(f" która paczka miała najwiecej pustych kilogramów {}?")
