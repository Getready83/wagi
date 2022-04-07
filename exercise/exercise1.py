# wykonanie poniższego kodu

a = "abcdefg"
print(a[1])
#a[1] = "x"

a_list = list(a)
print(a_list)
print(a_list[1])
a_list[1] = "x"
print(a_list)
a = "".join(a_list)
print(a)