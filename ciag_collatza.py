# ciąg collatza
# x = od 1 do 100
# jeżeli x jest parzyste (x % 2 == 0) to x / 2
# jeżeli x jets nieparzyste ( x % 2 == 1) to 3 * x + 1
# wypisz ciąg

over100 = False
print("Ciąg Collatza\npodaj liczbę od 1 do 100")
n = int(input())
if n > 100:
    over100 = True
while n >= 1:

    if n % 2 == 0:
        n = n / 2
    elif n % 2 == 1:
        n = 3 * n + 1

    if n == 1:
        break

    if not over100:
        print(n)
    else:
        print("Miałes podać liczbę od 1 do 100 !!!")
