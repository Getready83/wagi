import sys

# pyt - jakiej struktury użyjesz do zapisania numerów telefonów
# wszystkich klientów firmy i odpwiadajacym im nazwiska. wybierz strukture tak
#aby sprawdzic wlasciciela numeru tel

# Stwórz strukture przechowujaca ponizsze dane
# 123456789 - jan Kot
# 999888777 - Anna Lis
# 111222333 - Jan Kot
# odczytaj nazwisko własciciela 123456789

lista_tele_adresowa = {123456789: "Jan Kot",999888777: "Anna Lis", 111222333: "Jan Kot"}

print(lista_tele_adresowa[int(sys.argv[1])])

