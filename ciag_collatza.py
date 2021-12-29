# ciąg collatza
# x = od 1 do 100
# jeżeli x jest parzyste (x % 2 == 0) to x / 2
# jeżeli x jets nieparzyste ( x % 2 == 1) to 3 * x + 1
# wypisz ciąg

over100 = False
print("Ciąg Collatza\npodaj liczbę od 1 do 100")
x = int(input())
if x > 100:
    over100 = True
while x >= 1:

    if x % 2 == 0:
        x /= 2
    elif x % 2 == 1:
        x = 3 * x + 1

    if x == 1:
        break

    elif not over100:
        print(x)
    else:
        print("Miałes podać liczbę od 1 do 100 !!!")

# Nie wiem dlaczego wypisuje to aż tyle razy  ???