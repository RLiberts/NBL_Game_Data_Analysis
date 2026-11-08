# NBL Game Data Analysis

## Par projektu
Projekta mērķis ir iegūt paplašinātu statistisko redzējumu par līgas spēļu datiem. Dati tiek iegūti no Ramirent Nacionālās basketbola līgas mājaslapas. Ar Python skrāperi tiek iegūti spēļu protokoli un spēļu gaita, glabāti MS SQL Server. Rezultātā iegūst specifiska spēlētāja statistiku par ceturtdaļām, spēlētāja izaugsmi, tendencēm un citām metrikām, kuras attēlo Power BI.

Ideja ir radusies ar mērķi detalizētāk analizēt savu basketbola spēļu statistiku. 

## Plāns
|#|Darbība|
|---|---|
|1|Datu avotu izpēte|
|2|Vienas spēles ievākšana|
|3|SQL datubāzes shēma|
|4|Vienas spēles ielāde SQL Server datubāzē|
|5|Visas sezonas automātiska ielāde|
|6|Datu pārbaude SQL|
|7|Skatu izveida priekš metrikām, ceturtdaļām|
|8|Pytests|
|9|Spēlētāju izausgmes un ceturtdaļu analīze|
|10|PowerBI pārskats|
|11|Dokumentācijas, README|

## Dati un noteikumi
-Ievāktie dati netiek publicēti. Spēlētāju vārdi un statistika ir personas dati, un datu īpašnieki ir Latvijas Basketbola savienība un tās statistikas pakalpojuma sniedzējs. Mapes `raw/`, `data/` un `*.csv` faili ir `.gitignore` sarakstā.
-Repozitorijā ir tikai kods, SQL un analīzes rezultāti. Datus var atjaunot, palaižot skrāperi.