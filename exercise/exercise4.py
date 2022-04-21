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
