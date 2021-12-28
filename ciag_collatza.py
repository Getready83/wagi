# ciąg collatza
# x = od 1 do 100
# jeżeli x jest parzyste (x % 2 == 0) to x / 2
# jeżeli x jets nieparzyste ( x % 2 == 1) to 3 * x + 1
# wypisz ciąg

print("Ciąg Collatza\npodaj liczbę od 1 do 100")
n = int(input())
while n > 1:
    if n % 2 == 0:
        n = n / 2
    elif n % 2 == 1:
        n = 3 * n + 1
    if n == 1:
        break
    print(n)



