# jakiej struktury danych użyłbyś do zamodelowania
# szafki która ma trzy szuflady a w kazdej z nich trzy przgródki
# stwórz taki model i umoeść strinkga w srodkowej szufladzie środkowej szafki
# striing długopis

szafka = [[[],[],[]],[[],[],[]],[[],[],[]]]
szafka[1][1] = "długopis"

for szuflada in szafka:
    print(szuflada)


# z poniższej listy wypisz stringa schowany:

lista = [[34, False],[0], [("abc", 123), {"a":1, "x":(True, "schowany", 5)}]]

print(lista[2][1]["x"][1])

K = (('król', {2:'królewna', 1: ['córka', 'wróbel']},'5'),('żółw', 'wiewiórka'))

print(K[0][1][1][1])