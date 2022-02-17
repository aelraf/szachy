# szachy
Prosta aplikacja RESTowa wspomagająca grę w szachy.

# Opis:
1) klasa abstrkacyjna Figure, posiadająca:
  - kontruktor, przyjmujący jako pierwszy parametr pole, na którym znajduje się figura
  - metodę publiczną 'list_available_moves()', wypisującą dozwolone ruchy z zajmowanego miejsca
  - metodę publiczną 'validate_move(dest_field)', informującą, czy możliwy jest ruch na wskazane pole
    

2) 6 klas reprezentujących figury szachowe ( lista figur: https://en.wikipedia.org/wiki/Chess_piece )

3) implementacja algorytmów poruszania się danej figury (możliwe kombinacje ruchów: https://www.ichess.net/blog/chess-pieces-moves/)
Uwaga - uwzględniamy tylko sekwencje poruszania, bez bicia! 

4) Szachownica ma być stworzona zgodnie z zasadami, zachowując wszystkie pola: (https://pl.wikipedia.org/wiki/Szachownica)

5) API, wystawiająca poniżej podane URLe:
- [GET] `/api/v1/{chess-figure}/{current-field}` (wyświetla listę możliwych ruchów)
- [GET] `/api/v1/{chess-figure}/{current-field}/{dest-field}` (waliduje czy ruch na wskazane pole jest poprawny)
  
6) stworzenie prostej instrukcji umożliwiającej uruchomienie aplikacji

7) testy jednostkowe 

8) formatowanie z wykorzystaniem Black + sprawdzenie linterem flake8

# To do
- algorytm poruszania się Skoczka
- API wystawiające URLe
- instrukcja uruchomienia
- formatowanie z wykorzystaniem Black
- sprawdzenie linterem flake8


# Uwaga:
Technologie do wykorzystania:
- Python 3.6 - 3.9
- Black (formatowanie)
- Flake8 (linter)
- Pytest (testy)
- Flask 1.0+
- ewentualne potrzebne zewnętrzne biblioteki

