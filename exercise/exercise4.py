#co zostanie wypisane w wywniku poniższego kodu

D = {1:"Ala", 2: "ma", 3: "kota"}

for key in D:
    print(D[key])

# w zależnosci od tego jaka wersja pythona

# pyt dla danego stringa x stwórz słownik przechowujący informacje ile razy dana
# litera występuje w stringu

x = "myszydokazujągdykotanieczują"

D = {}
for litera in x:
    if litera not in D.keys():
        D[litera] = 1
    else:
        D[litera] += 1

S = {x:x+1 for x in range(10000) if x%23 == 0}
E = {a : a+2 for a in range(100) if a%5 == 0}

litera = {'m': 1, 'y': 3, 's': 1, 'z': 3, 'd': 2, 'o': 2, 'k': 2, 'a': 2, 'u': 2, 'j': 2, 'ą': 2, 'g': 1, 't': 1, 'n': 1, 'i': 1, 'e': 1, 'c': 1}

print(list(litera.values()))

print(True if 4 in list(litera.values())else False)

pensje = {'ksiegowa': 5000, 'kierowca': 4500, 'recepcjonistka': 4000}

print(sum(list(pensje.values())))

# stwórz odwróconą listę language

language = ['Python', 'Java', 'C#', 'Ruby']
"""print(language)
language.reverse()
print(language)"""

# wykorzystanie funkcji reversed() - zwraca list_reversiterator object
# zamieniamy na liste
language_reverse = reversed(language)
print(list(language_reverse))

# slicy !!!!
language_reverse = language[::-1]
print(language_reverse)

language_reverse = []
for languag in language:
    language_reverse.insert(0,languag) # insert w tym wypadku zapisuje nowy język na 0 indeksie przy każdym przebiegu petli
print(language_reverse)
#
odwroc_mnie = ['trudne', 'takie', 'bylo', 'nie', 'To']

odwrocona = odwroc_mnie[::-1]
odwrocona =[]
for word in odwroc_mnie:
    odwrocona.insert(0,word)

odwrocona = reversed(odwroc_mnie)
print(list(odwrocona))

odwroc_mnie.reverse()
odwrocona = odwroc_mnie
print(odwrocona)
