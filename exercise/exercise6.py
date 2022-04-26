# znajdź róznice miedzy najwyższą a najmniw=ejsza wartością w poniższej liscie
# rozw ma być  efektywne

A = [4, 5, 7, -3, 2, 8, -10, 15, 1, 0]

"""#1
A = sorted(A)  # wydajność 0(N*log_N)
print(A[-1] - A[0])"""

#2  wydajność  O(N)

"""max = A[0]
min = A[0]
count = 0
for number in A:
    if number > max:
        max = number
    elif number < min:
        min = number
    count += 1
    print(count, min, max)
print(count, max, min)
print(max - min)"""

#3  wydajność O(N)

print(max(A)- min(A))
print(min(A))

B = [x**2 + 3 for x in range(10)]
print(B)