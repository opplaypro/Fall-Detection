# Pliki i ich funkcje

Wszystkie pliki znajdują się w folderze `src` (aby było czytelniej)
.
├── `buildozer.spec`
├── `core`
│   ├── `__init__.py`
│   ├── `algorithm.py`
│   ├── `log.py`
│   ├── `notifier.py`
│   └── `sensors.py`
├── `main.py`
└── `ui`
    ├── `__init__.py`
    ├── `screen_manager.py`
    └── `screens`
        ├── `__init__.py`
        ├── `home_screen.kv`
        └── `home_screen.py`

plik `main.py` to punkt startowy
`buildozer.spec` to plik, który jest konfiguracją programu do budowania aplikacji ([`buildozer`](https://buildozer.readthedocs.io/en/latest/))
w folderze `core` znajduje się *backend* aplikacji:
- `algorithm.py` — algorytm wykrywający upadek
- `notifier.py` — będzie kod obsługujący powiadomienia, smsy i co tam się doda
- `sensors.py` — zajmuje się odczytywaniem i obsługiwaniem danych z akcelerometru i żyroskopu (łatwo można żyroskop usunąć, jakby było bez niego)
- `log.py` — logowanie informacji i błędów (do debugowania)
- `__init__.py` — dzięki temu plikowy python traktuje `core` jako moduł (łatwiej się importuje)

w folderze `ui` znajduje się *frontend* — wygląd aplikacji i jej interakcja z użytkownikiem
- `__init__.py` — to samo
- `screen_manager.py` — zarządzenie ekranami (przejścia np, do zrobienia cały)
- w pod folderze `screens` znajdują się pliki ekranów (każdy ekran ma 2 pliki)
	- `home_screen.py` — logika działania ekranu (jak coś się kliknie to co się stanie)
	- `home_screen.kv` — *asset* ekranu (wygląd ekranu, gdzie co jest, czcionki)
	- `__init__.py` — to samo

# Obiekty, klasy i metody
## `sensors.py`
w tym pliku znajdują się 2 klasy:
### `DataBuffer`
jest to bufor na dane (duh). Posiada metody do dodawania danych do niego i odczytywania

### `Sensor`
Główna klasa symbolizująca czujniki. ma metody do włączenia i wyłączenia (na wszelki wypadek) oraz do odczytywania danych z buforu (obiekt `Sensor` zawiera dwa obiekty `DataBuffer` dla danych z akcelerometru i żyroskopu)

## `log.py` 
w skrócie: fancy print do błędów, żeby ładniej wyglądało i czytelniej (pokazuje kiedy był błąd, gdzie był błąd, i wiadomość błędu)

## `algorithm.py`
póki co zawiera funkcję, która oblicza przyspieszenie wypadkowe, zwraca wartość oraz `bool` (True/False) w zależności czy przekroczy 30 m/s2

## `home_screen.py`
czarna magia, pisało mi to AI, razem z `home_screen.kv` zmienia kolorek ekranu w zależności czy był wykryło upadek

## `main.py`
zawiera klasę `MyApp` (nazwa do zmiany), która jest w zasadzie całą aplikacją.
na początku jest włączenie logowania i log informacji o starcie, później dodanie domyślnego `ScreenManager` i ekranu `home_screen.py`

instrukcja
```python
if __name__ == '__main__':
	MyApp.run()
```
uruchamia aplikację, tyle

# Do zmiany

- `main.py` — prawie cały
- `algorithm.py` — sporo, zależy w jaki sposób będziemy obsługiwać upadek
- `notifier.py` — jest pusty
- `screen_manager.py` — póki co to jest proof of concept, nie jest używany, nie działa
- wszystko w folderze `ui/screens/` — czytaj cały wygląd aplikacji
- zrobić  `assets/` na obrazki i `lang/pl-PL.yaml/toml` na tekst, ewentualnie tłumaczenia (naprawdę łatwiej tak jest)
- plik `config.yml`
# Gotowe pliki

- `log.py`
- `sensors.py` — ewentualnie zmiany, jak będzie bez żyroskopy czy jakieś inne drobne poprawki
