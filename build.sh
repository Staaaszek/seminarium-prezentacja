#!/usr/bin/env bash
# Buduje prezentację na Ubuntu/Debianie i macOS.
#
# Użycie:  ./build.sh [all|prezentacja|handout|sprawdz|clean]
#   all          (domyślnie) obie wersje PDF
#   prezentacja  wersja z animacjami (overlayami) -> prezentacja.pdf
#   handout      wersja do druku, jedna strona na slajd -> prezentacja_handout.pdf
#   sprawdz      uruchamia skrypty/sprawdz.py (weryfikuje liczby ze slajdów)
#   clean        usuwa katalog build/ i zbudowane PDF-y
set -euo pipefail
cd "$(dirname "$0")"

SYSTEM="$(uname -s)"
GLOWNY=prezentacja
BUILD=build

# MacTeX/BasicTeX instaluje programy w /Library/TeX/texbin, którego nie zawsze ma PATH.
if [ "$SYSTEM" = "Darwin" ] && [ -d /Library/TeX/texbin ]; then
  PATH="/Library/TeX/texbin:$PATH"
fi

jak_zainstalowac() {
  case "$SYSTEM" in
    Linux)
      cat <<'TXT'
Ubuntu/Debian:
  sudo apt-get update
  sudo apt-get install texlive-latex-base texlive-latex-recommended texlive-latex-extra \
       texlive-pictures texlive-fonts-recommended texlive-lang-polish lmodern
TXT
      ;;
    Darwin)
      cat <<'TXT'
macOS (Homebrew):
  pełny TeX Live:  brew install --cask mactex-no-gui
  albo mniejszy:   brew install --cask basictex
                   eval "$(/usr/libexec/path_helper)"
                   sudo tlmgr update --self
                   sudo tlmgr install beamer translator pgf babel-polish \
                        hyphen-polish lm mathtools booktabs etoolbox xcolor
TXT
      ;;
    *)
      echo "Zainstaluj dystrybucję TeX Live z pakietami: beamer, pgf/tikz, babel-polish, lm, mathtools, booktabs."
      ;;
  esac
}

sprawdz_zaleznosci() {
  if ! command -v pdflatex >/dev/null 2>&1 || ! command -v kpsewhich >/dev/null 2>&1; then
    echo "Brak pdflatex/kpsewhich (TeX Live)." >&2
    jak_zainstalowac >&2
    exit 1
  fi
  brakuje=""
  for plik in beamer.cls tikz.sty polish.ldf lmodern.sty t1lmr.fd \
              amsmath.sty amssymb.sty mathtools.sty booktabs.sty array.sty; do
    if [ -z "$(kpsewhich "$plik" 2>/dev/null)" ]; then
      brakuje="$brakuje $plik"
    fi
  done
  if [ -n "$brakuje" ]; then
    echo "Brakuje plików LaTeX-a:$brakuje" >&2
    jak_zainstalowac >&2
    exit 1
  fi
}

# kompiluj <nazwa_zadania> <kod przed \input>
kompiluj() {
  zadanie="$1"
  przed="$2"
  mkdir -p "$BUILD"
  # Dwa przebiegi: beamer potrzebuje drugiego do spisu treści i nawigacji.
  for przebieg in 1 2; do
    if ! pdflatex -interaction=nonstopmode -halt-on-error -file-line-error \
          -output-directory="$BUILD" -jobname="$zadanie" \
          "${przed}\\input{${GLOWNY}.tex}" >"$BUILD/$zadanie.stdout" 2>&1; then
      echo "Błąd kompilacji $zadanie (przebieg $przebieg). Fragment logu:" >&2
      grep -n -A4 -E '^(!|.*:[0-9]+:)' "$BUILD/$zadanie.log" | head -40 >&2 || tail -40 "$BUILD/$zadanie.log" >&2
      exit 1
    fi
  done
  cp "$BUILD/$zadanie.pdf" "./$zadanie.pdf"
  echo "Gotowe: $(pwd)/$zadanie.pdf"
}

cel="${1:-all}"
case "$cel" in
  all)
    sprawdz_zaleznosci
    kompiluj "$GLOWNY" ""
    kompiluj "${GLOWNY}_handout" '\PassOptionsToClass{handout}{beamer}'
    ;;
  prezentacja)
    sprawdz_zaleznosci
    kompiluj "$GLOWNY" ""
    ;;
  handout)
    sprawdz_zaleznosci
    kompiluj "${GLOWNY}_handout" '\PassOptionsToClass{handout}{beamer}'
    ;;
  sprawdz)
    command -v python3 >/dev/null 2>&1 || { echo "Potrzebny python3." >&2; exit 1; }
    python3 skrypty/sprawdz.py
    ;;
  clean)
    rm -rf "$BUILD" "$GLOWNY.pdf" "${GLOWNY}_handout.pdf"
    ;;
  *)
    echo "Użycie: $0 [all|prezentacja|handout|sprawdz|clean]" >&2
    exit 2
    ;;
esac
