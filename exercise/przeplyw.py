
version = 3.7

print(version < 3)

"""if [warunek]:
    [instrukcja]"""

if 8 < 10:
    print("tak")

a = 8
if a > 10:
    print(" jest większe")
else:
    print("jest mniejsze")


age = 27
if age < 18:
    print("Nie masz uprawnien")
else:
    print("dostęp przyznany")

age = int(input("Podaj wiek :"))
if age == 18:
    print("masz 18 lat")
elif age < 18:
    print("Nie masz uprawnien")
else:
    print("dostęp przyznany")


A = ["apple", "bannan", "orange"]
B = ["red", "Yellow", "orange"]
count = 0
for fruits in A:
    print(fruits, B[count])
    count += 1

