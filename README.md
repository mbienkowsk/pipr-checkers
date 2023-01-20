# readme

## Instrukcja włączenia programu

- Do obsługi programu potrzebna jest biblioteka pygame. Pisząc go, używałem ostatniej dostępnej dla mnie wersji - pygame'a 2.1.2 na pythonie 3.8.10, nie jestem niestety pewien, jaka najniższa wersja zadziała poprawnie.
- Z poziomu głównego katalogu projektu należy uruchomić program przez terminal
(python3 -m checkers.main), ze względu na segmentację paczek na testy i pliki z kodem
przycisk run w vsc nie rozwiązuje poprawnie importów.

## Instrukcja korzystania z programu

- Aby wyjść z partii w trakcie gry do głównego menu, należy nacisnąć "q" na klawiaturze. Jeśli przycisk zostanie kliknięty w trakcie kalkulacji ruchu przez bota, wyjście do menu nastąpi po jego decyzji.
- Jeżeli partia skończy się w, jak się wydaje, losowym momencie, oznacza to, że limit możliwych ruchów bez bicia został przekroczony zgodnie z zasadami gry. Domyślnie jest to 50 ruchów, aby zmienić tę wartość, należy ustawić zmienną MAX_MOVES_WITHOUT_ATTACKS w pliku constants na wybraną wartość.
- Jeżeli w wybranej rozgrywce bierze udział bot, to po kliknięciu przycisku w głównym menu, na terminalu należy wpisać, który z botów ma wziąć udział i, jeżeli jest to bot minimax, ustawić jego głębię. Na poziomach 1-5 jest on mało zaawansowanym przeciwnikiem oraz czas ruchu jest bardzo niewielki. Głębia 6-7 to moim zdaniem złoty środek pomiędzy poziomem bota, a jego czasem ruchu (średnia około 4-8 sekund, zależnie od pozycji w rozgrywanej partii.) Powyżej głębii 7 bot jest zaawansowanym przeciwnikiem, czas ruchu zwiększa się jednak wykładniczo z każdym dodanym poziomem.
