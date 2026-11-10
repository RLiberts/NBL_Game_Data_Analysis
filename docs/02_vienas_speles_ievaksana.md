## Mērķis
Ievākt vienas spēles protokolu un spēles gaitu, pārvērst datus CSV un saprast, kā ievākt un apstrādāt visas sezonas spēles datus.

## Ko darīju
- Izveidots state.py, kur funkcija encode_state no atslēgām izveido API parametru state. Ar to var izveidot pieprasījumu jebkurai spēlei.
- Izveidots fetch_game.py, kur funkcija fetch_json lejupielādē spēles protokolu un spēles gaitu JSON formātā un saglabā tos mapē raw/.
- Izveidots parse_game.py, kas pārvērš JSON failus divās CSV tabulās. Pirmā players.csv, kur viena rinda ir viens spēlētājs spēlē. Otra tabula events.csv, kur viena rinda ir viens spēles notikums.

## Ko atradu
- Gan spēlētāju minūtes protokolā, gan pulkstenis spēles gaitā laiks tiek glabāts PT_M_S formātā. (PT33M33S)
- Spēles gaitas laiks iet dilstoša secībā. Rāda atlikušo laiku ceturtdaļā.
- Paraugspēlē ir 532 spēles gaitas notikumi

## Lēmumi un kapēc
- Kešs mapē raw/ pirms pieprasījuma pārbauda, vai fails jau ir. Katra spēle tiek lejupielādēta tikai vienreiz, tādejādi serveris netiek lieki noslogots, un datus var apstrādāt atkārtoti bez interneta.
- Laiks pārvērsts sekundēs, jo sekundes ir precīzas. Minūtes ar komatu būtu jānoapaļo, un summās kļūda uzkrātos. 
- CSV ar utf-8-sig, lai Excel pareizi rādītu latviešu burtus.
