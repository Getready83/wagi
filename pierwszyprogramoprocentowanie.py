kredyt = float(input("Kwota kredytu wynosi: "))
oprocentowanie = float(input ("Oprocentowanie kredytu wynosi: "))
ratakredytu = float(input("rata kredytu spłacana co miesiąc to: "))





styczen19 = ((1)+(float(1.5928245)+(oprocentowanie))/(1200))*((kredyt)-(ratakredytu))
print("W styczniu 2019 twoja pozostała kwota kredytu to",(round(styczen19,2)),
      " i jest to ",round((kredyt - styczen19),2)," mniej niż w poprzednim miesiącu")
luty19 = ((1)+(float(-0.4535091012)+(oprocentowanie))/(1200))*((styczen19)-(ratakredytu))
print("W lutym 2019 twoja pozostała kwota kredytu to",(round(luty19,2)),
      "i jest to",round((styczen19 - luty19),2),"mniej niż w poprzednim miesiącu")
marzec19 = ((1)+(float(2.3246717171)+(oprocentowanie))/(1200))*((luty19)-(ratakredytu))
print("W marcu 2019 twoja pozostała kwota kredytu to",(round(marzec19,2)),
      "i jest to",round((luty19 - marzec19),2),"mniej niż w poprzednim miesiącu")
kwiecien19 = ((1)+(float(1.2612544072)+(oprocentowanie))/(1200))*((marzec19)-(ratakredytu))
print("W kwietniu 2019 twoja pozostała kwota kredytu to",(round(kwiecien19,2)),
      "i jest to",round((marzec19 - kwiecien19),2),"mniej niż w poprzednim miesiącu")
maj19 = ((1)+(float(1.78252628571251)+(oprocentowanie))/(1200))*((kwiecien19)-(ratakredytu))
print("W maju 2019 twoja pozostała kwota kredytu to",(round(maj19,2)), "i jest to",
round((kwiecien19 - maj19),2),"mniej niż w poprzednim miesiącu")
czerwiec19 = ((1)+(float(2.3293845415)+(oprocentowanie))/(1200))*((maj19)-(ratakredytu))
print("W czerwcu 2019 twoja pozostała kwota kredytu to",(round(czerwiec19,2)),
      "i jest to",round((maj19 - czerwiec19),2),"mniej niż w poprzednim miesiącu")
lipiec19 = ((1)+(float(1.5022298422)+(oprocentowanie))/(1200))*((czerwiec19)-(ratakredytu))
print("W lipcu 2019 twoja pozostała kwota kredytu to",(round(lipiec19,2)),
      "i jest to",round((czerwiec19 - lipiec19),2),"mniej niż w poprzednim miesiącu")
sierpien19 = ((1)+(float(1.7825262857)+(oprocentowanie))/(1200))*((lipiec19)-(ratakredytu))
print("W sierpniu 2019 twoja pozostała kwota kredytu to",(round(sierpien19,2)),
      "i jest to",round((lipiec19 - sierpien19),2),"mniej niż w poprzednim miesiącu")
wrzesien19 = ((1)+(float(2.3288489941)+(oprocentowanie))/(1200))*((sierpien19)-(ratakredytu))
print("We wrześniu 2019 twoja pozostała kwota kredytu to",(round(wrzesien19,2)),
      "i jest to",round((sierpien19 - wrzesien19),2),"mniej niż w poprzednim miesiącu")
pazdziernik19 = ((1)+(float(0.6169213482)+(oprocentowanie))/(1200))*((wrzesien19)-(ratakredytu))
print("W październiku 2019 twoja pozostała kwota kredytu to",(round(pazdziernik19,2)),
      "i jest to",round((wrzesien19 - pazdziernik19),2),"mniej niż w poprzednim miesiącu")
listopad19 = ((1)+(float(2.3522958864)+(oprocentowanie))/(1200))*((pazdziernik19)-(ratakredytu))
print("W listopadzie 2019 twoja pozostała kwota kredytu to",(round(listopad19,2)),
      "i jest to",round((pazdziernik19 - listopad19),2),"mniej niż w poprzednim miesiącu")
grudzien19 = ((1)+(float(0.3377795452)+(oprocentowanie))/(1200))*(listopad19)-(ratakredytu)
print("W grudniu 2019 twoja pozostała kwota kredytu to",(round(grudzien19,2)),
      "i jest to",round((listopad19 - grudzien19),2), "mniej niż w poprzednim miesiącu")
szer = 110
print("*" * szer)
styczen20 = ((1)+(float(1.5770352473)+(oprocentowanie))/(1200))*((grudzien19)-(ratakredytu))
print("W styczniu 2020 twoja pozostała kwota kredytu to",(round(styczen20,2)),
      "i jest to",round((grudzien19 - styczen20),2),"mniej niż w poprzednim miesiącu")
luty20 = ((1)+(float(-0.2927814426)+(oprocentowanie))/(1200))*((styczen20)-(ratakredytu))
print("W lutym 2020 twoja pozostała kwota kredytu to",(round(luty20,2)),
      "i jest to",round((styczen20 - luty20),2),"mniej niż w poprzednim miesiącu")
marzec20 = ((1)+(float(2.4861965902)+(oprocentowanie))/(1200))*((luty20)-(ratakredytu))
print("W marcu 2020 twoja pozostała kwota kredytu to",(round(marzec20,2)),
      "i jest to",round((luty20 - marzec20),2), "mniej niż w poprzednim miesiącu")
kwiecien20 = ((1)+(float(0.2671103178)+(oprocentowanie))/(1200))*((marzec20)-(ratakredytu))
print("W kwietniu 2020 twoja pozostała kwota kredytu to",(round(kwiecien20,2)),
      "i jest to",round((marzec20 - kwiecien20),2),"mniej niż w poprzednim miesiącu")
maj20 = ((1)+(float(1.4179526723)+int(oprocentowanie))/(1200))*((kwiecien20)-(ratakredytu))
print("W maju 2020 twoja pozostała kwota kredytu to",(round(maj20,2)),
      "i jest to",round((kwiecien20 - maj20),2),"mniej niż w poprzednim miesiącu")
czerwiec20 = ((1)+(float(1.0542432673)+(oprocentowanie))/(1200))*((maj20)-(ratakredytu))
print("W czerwcu 2020 twoja pozostała kwota kredytu to",(round(czerwiec20,2)),
      "i jest to",round((maj20 - czerwiec20),2),"mniej niż w poprzednim miesiącu")
lipiec20 = ((1)+(float(1.4805201045)+(oprocentowanie))/(1200))*((czerwiec20)-(ratakredytu))
print("W lipcu 2020 twoja pozostała kwota kredytu to",(round(lipiec20,2)),
      "i jest to",round((czerwiec20 - lipiec20),2),"mniej niż w poprzednim miesiącu")
sierpien20 = ((1)+(float(1.5770352473)+(oprocentowanie))/(1200))*((lipiec20)-(ratakredytu))
print("W sierpniu 2020 twoja pozostała kwota kredytu to",(round(sierpien20,2)),
      "i jest to",round((lipiec20 - sierpien20),2),"mniej niż w poprzednim miesiącu")
wrzesien20 = ((1)+(float(-0.0774206903)+(oprocentowanie))/(1200))*((sierpien20)-(ratakredytu))
print("We wrześniu 2020 twoja pozostała kwota kredytu to",(round(wrzesien20,2)),
      "i jest to",round((sierpien20 - wrzesien20),2),"mniej niż w poprzednim miesiącu")
pazdziernik20 = ((1)+(float(1.165733987)+(oprocentowanie))/(1200))*((wrzesien20)-(ratakredytu))
print("W październiku 2020 twoja pozostała kwota kredytu to",(round(pazdziernik20,2)),
      "i jest to",round((wrzesien20 - pazdziernik20),2),"mniej niż w poprzednim miesiącu")
listopad20 = ((1)+(float(-0.4041867176)+(oprocentowanie))/(1200))*((pazdziernik20)-(ratakredytu))
print("W listopadzie 2020 twoja pozostała kwota kredytu to",(round(listopad20,2)),
      "i jest to",round((pazdziernik20 - listopad20),2),"mniej niż w poprzednim miesiącu")
grudzien20 = ((1)+(float(1.4997085208)+(oprocentowanie))/(1200))*((listopad20)-(ratakredytu))
print("W grudniu 2020 twoja pozostała kwota kredytu to",(round(grudzien20,2)),
      "i jest to",round((listopad20 - grudzien20),2),"mniej niż w poprzednim miesiącu")