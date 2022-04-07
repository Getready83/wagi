# niepowtarzalne elementy
#korzystajac z podanej listy A
# stwórz listę B która zawiera tylko unikalne elementy listy A

A = [1, 2, 3, 3, 2, 1, 2, 3]

"""B = []
for element in A:
    if element not in B:
        B.append(element)

B = (list(set(A)))
print(B)"""


"""my_set = {1, 2, 3, 4, 3, 2, 1}
print(my_set)"""

"""my_set = set([1, 2, 3, 2])
print(my_set)

my_set = {1, 2, [3, 4]}
print(my_set)"""

"""a = {}

b = set()

print(type(a))
print(type(b))"""

my_set = {1, 3}
my_set.add(2)
print(my_set)
my_set.update([2,3,4])
print(my_set)
my_set.update([4,5], {1,6,8})
print(my_set)
my_set.discard(2)
print(my_set)
my_set.remove({3, 4})
print(my_set)