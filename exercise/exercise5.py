# palindrom jak sprawdzic czy wyraz jest palindromem

def sprawdz_palindrom(slowo):
    slowo_odwrocony = slowo[::-1]
    if slowo == slowo_odwrocony:
        return True
    else:
        return False

print(sprawdz_palindrom("droga"))


def check_palindrom(word):
    return True if word == word[::-1] else False

print(check_palindrom("kajak"))
print(check_palindrom("anakonda"))

def check_letters_palindrom(word):
    start = 0
    end = len(word) -1
    while start <= end:
        print(word[start], word[end])
        if word[start] != word[end]:
            return False
        else:
            start += 1
            end -= 1
            print(word[start] , word[end])
    return True

print(check_letters_palindrom("andomodna"))


# range -  stwórz listę A- zawierającą liczby od 1-10 i B zawierającą co 3 liczbe
# z zakresu od 1 do 10

#  print(list(range(10+1))) # range(start, stop, krok(skok))

A = list(range(1,10+1))
print(A)
B = list(range(100,0,-3))
print(B)

# wypisz pierwsze 5 elementów listy L
# wypisz co drugą literę stringa s zaczynając od ostatniej  cofając sie do
# poczatku

L = [11, 22, 33, 44, 55, 66, 77, 88, 99, 1010]
s = 'a nMozh^tKysPW 9ęxi b$uML'

print(L[len(L)::-1])
print(L[:5])

print(s[len(s)::-2])
print(s[-1::-2])

a = '!ooe&sj7?czaa()lmxuo,t2fa^4rtngk'
print(a[-2::-3])

# funkcja sprawdzająca string

a = "python_moj_kod.py"

b = "python_notatki.txt"

def check_string(file_name):
    if file_name[0:6] == "python" and file_name[-3::1] == ".py":
        return True
    else:
        return False

print(check_string(a))


# wypisz podaną listę imion dodając prze każdym kolejny numer zacz od 1

names = ['Adam', 'Stanisław', 'Maria', 'Zofia', "Mikołaj"]

count = 1
for name in names:
    print(count, name)
    count +=1

# enumerate !!!

for count, name in enumerate(names,20):
    print(count, name)