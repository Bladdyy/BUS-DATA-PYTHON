# My biggest Python project
Pretty open project about tracking and analyzing speed and location of buses in Warsaw.

# Assignment

Korzystając z danych dostępnych na stronie https://api.um.warszawa.pl/# zbierz informacje o pozycjach autobusów w zadanym przedziale czasu. Proponujemy, wybranie dwóch takich przedziałów o długości minimum jedna godzina (ciekawa może być np. jedna z godzin szczytu natężenia ruchu, porównana z wczesnoporanną lub późnowieczorną). 

Następnie przeprowadź analizę zebranych danych. Zachęcamy do inwencji, stawiania własnych hipotez badawczych i ich weryfikację z wykorzystaniem zebranych danych.

## Pytania, na które należy odpowiedzieć niezależnie od własnych analiz, to:
1) Przekraczanie prędkości
1.1) Ile autobusów przekroczyło prędkość 50 km/h?
#### Uwaga:
* Pozycja autobusu jest aktualizowana co minutę. Przyjmując założenie, że autobus porusza się w ciągu minuty po linii prostej, możemy przybliżyć rzeczywistą prędkość.
1.2) Czy były miejsca, w których znaczny procent autobusów przekraczał tę dozwoloną prędkość
#### Uwaga:
* W rozwiązaniu należy zdefiniować pojęcie lokalizacji, np. może to być konkretne miejsce w mieście (np. ulica, most), promień wokół danego punktu geograficznego.
2) Punktualność
Analiza punktualności autobusów w obserwowanym okresie (możemy porównać rzeczywisty czas dojazdu na przystanki z rozkładem jazdy).

Wymagania techniczne, wskazówki co do sposobu oceniania, pomocne uwagi:
A) Rozwiązanie powinno zostać wdrożone w dwóch częściach. Pierwsza niech służy do zbierania danych i zapisu do pliku.
Druga część niech przeprowadza analizę zebranych danych. Daje to elastyczność wymiany jednej z części rozwiązania na zamiennik. (pobieranie danych jest czasochłonne)
B) Zasady oceny:
* Wyjaśnianie decyzji projektowych podczas egzaminu.
* Prawidłowy podział kodu na pakiety i moduły.
* Jakość kodu. Przypominamy o PEP (https://www.python.org/dev/peps/pep-0008/) i zautomatyzowanych narzędziach omawianych na zajęciach 10 jak pylint lub flake, do sprawdzenia kodu.
* Zwrócenie uwagi na nazwy własne funkcji i zmiennych. Funkcje powinny być krótkie. Nie powinno być kopii fragmentów kodu ect.
* Możliwość zainstalowania kodu jako pakietu przy użyciu `pip install ./path/to_package_directory`.
* Pokrycie kodu testami.
* Analiza programu profilerem i omówienie wąskich gardeł w projekcie (oczekujemy analizy i omówienia programu, a nie wielokrotnych iteracji w celu ulepszenia kodu).
* Sposób prezentacji (jeśli skrypt, to np. czy korzysta z argparse-a; jeśli jupyter notebook to jak wizualizowane są dane). Przejrzysty opis projektu.
* Czy jest dodana jakaś autorska analiza poza tymi obowiązkowymi.
* Wizualizacja danych i opcjonalnie wizualizacja wyników na mapie Warszawy.
C) Pomocne uwagi:
* Do analizy danych świetnie nadają się biblioteki numpy i pandas, które odpowiednio będą omówione na pierwszych i drugich zajęciach w 2024.
* Trzecie zajęcia w styczniu będą poświęcone wizualizacji.
D) Termin zaliczenia:
* Do ustalenia z Prowadzącym laboratorium.
* Pierwszy krok to przesłanie dostępu do repozytorium i informacji o ostatnim commit-cie Prowadzącemu.
* Następnie umówienie się na konkretny termin w celu prezentacji programu i wyników analiz Prowadzącemu.
* Jeśli ocena zostanie wystawiona przed końcem sesji, zostanie wpisana do protokołu w pierwszym terminie.
* Osoby, które uzyskają ocenę po końcu sesji, a przed końcem sesji poprawkowej, otrzymają ocenę w drugim terminie.
* Uwaga, ostatniego dnia Prowadzący może mieć zajęte terminy. Proszę też wziąć pod uwagę fakt, że niezbędny jest czas na zapoznanie się z Państwa projektem, przed Państwa prezentacją.
