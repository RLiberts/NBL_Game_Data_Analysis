## Mērķis
Atrast, kur nbl.basket.lv glabā spēļu datus, un kā tos var iegūt.

## Ko darīju
- nbl.basket.lv/robots.txt izpēte 
- nbl.basket.lv/kalendars, DevTools, Network ar filtru Fetch/XHR un Disable Cache. Meklēju, kur lapa sūta datu pieprasījumu.
- atradu 'fixtures' pieprasījumu un atvēru to atsevišķā cilnē.

## Ko atradu
- nbl.basketb.lv/robots.txt saturēja tikai informāciju par 'content signals' nevis par datu vākšanas aizliegumu.
- Dati tiek ielādēti no ārēja statistikas pakalpojuma Sportradar (https://embed-api.eui.connect.sportradar.com/v1/embed/120/fixtures?)
- API atbild ar JSON
- Dati tiek ielādēti bez jebkādas atslēgas vai pieslēgšanas.

## Lēmumi un kapēc
- Datus ņemšu no API, jo JSON ir stabils un strukturēts.
- Pietiks ar Python requests bibliotēku, jo API strādā bez atslēgas.
