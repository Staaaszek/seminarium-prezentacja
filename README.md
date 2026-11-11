# Prezentacja: rozdział 2 (Alman, Vassilevska Williams 2026)

Slajdy Beamer (motyw `Madrid`, 16:9) o rozdziale 2 pracy *Truly Subquadratic 3SUM and
Truly Subcubic APSP via Triangles in Sparse Lopsided Graphs*: Twierdzenie 5, Lematy 6–11
i Uwaga 12, z dowodami w kolejności z pracy.

## Budowanie (Ubuntu i macOS)

    ./build.sh            # obie wersje: prezentacja.pdf (z animacjami) i prezentacja_handout.pdf
    ./build.sh prezentacja
    ./build.sh handout
    ./build.sh sprawdz    # python3: weryfikuje liczby ze slajdów
    ./build.sh clean

Skrypt sprawdza, czy są potrzebne pakiety LaTeX-a, i jeśli czegoś brakuje, wypisuje
polecenie instalacji (`apt-get` na Ubuntu, MacTeX/BasicTeX + `tlmgr` na macOS).
Wystarczy `pdflatex`. Python jest potrzebny tylko do `./build.sh sprawdz`.

## Struktura

- `prezentacja.tex`: preambuła, makra i kolejność sekcji.
- `sekcje/01_twierdzenie5.tex` … `07_podsumowanie.tex`: slajdy w kolejności z `Plan_prezentacji.md`.
- `skrypty/sprawdz.py`: implementacja `Full` i `Pruned`. Sprawdza na małych parametrach
  Lematy 6–11, wszystkie przykłady liczbowe ze slajdów i stałe z dowodu Twierdzenia 5.

## Orientacyjny podział czasu (90 min)

| Część | Slajdy | Czas |
|---|---|---|
| Twierdzenie 5 i mapa rozdziału | 4 | 7 min |
| 2.1 Strassen, trzy fazy, zapis trójliniowy | 5 | 9 min |
| 2.2 Schönhage, Lemat 6, obserwacje | 8 | 13 min |
| 2.3 `Full`, Lematy 7–9, kafelkowanie | 22 | 27 min |
| 2.4 kodowanie raz, `Pruned`, Lematy 10–11 | 18 | 25 min |
| 2.4.4 dowód Twierdzenia 5, Uwaga 12 | 7 | 8 min |
| Podsumowanie: kluczowe idee | 1 | 1 min |
