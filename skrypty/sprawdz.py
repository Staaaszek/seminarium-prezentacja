"""Sprawdza wszystkie liczby i przykłady pokazywane na slajdach.

Uruchomienie: python3 skrypty/sprawdz.py  (z katalogu prezentacja/).
Implementuje Full i Pruned z rozdziału 2 i weryfikuje Lematy 6-11 na małych
parametrach, a także stałe z dowodu Twierdzenia 5.
"""

import itertools as it
import math
import random
from fractions import Fraction

random.seed(2026)

LEWE = ["x1", "x2", "x3", "p11", "p12", "p21", "p22"]
PRAWE = ["y1", "y2", "y3", "q11", "q12", "q21", "q22"]
SKL = [f"P{i}{j}" for i in (1, 2, 3) for j in (1, 2, 3)] + ["P0"]
WYJ = [f"z{i}{j}" for i in (1, 2, 3) for j in (1, 2, 3)] + ["z0"]


def phat(i, j):
    if j == 3:
        return {}
    if i < 3:
        return {f"p{i}{j}": 1}
    return {f"p1{j}": -1, f"p2{j}": -1}


def qhat(i, j):
    if i == 3:
        return {}
    if j < 3:
        return {f"q{i}{j}": 1}
    return {f"q{i}1": -1, f"q{i}2": -1}


PHI, PSI = {}, {}
for i, j in it.product((1, 2, 3), repeat=2):
    PHI[f"P{i}{j}"] = {f"x{i}": 1, **phat(i, j)}
    PSI[f"P{i}{j}"] = {f"y{j}": 1, **qhat(i, j)}
PHI["P0"] = {"x1": -1, "x2": -1, "x3": -1}
PSI["P0"] = {"y1": 1, "y2": 1, "y3": 1}


def wnosi(lam, z):
    return z == "z0" or lam == "P" + z[1:]


def ev(forma, w):
    return sum(c * w[s] for s, c in forma.items())


# ---------------------------------------------------------------- Strassen
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
(a11, a12), (a21, a22) = A
(b11, b12), (b21, b22) = B
S = [None,
     (a11 + a22) * (b11 + b22), (a21 + a22) * b11, a11 * (b12 - b22),
     a22 * (b21 - b11), (a11 + a12) * b22, (a21 - a11) * (b11 + b12),
     (a12 - a22) * (b21 + b22)]
AB = [[S[1] + S[4] - S[5] + S[7], S[3] + S[5]], [S[2] + S[4], S[1] - S[2] + S[3] + S[6]]]
assert AB == [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
print("Strassen S1..S7 =", S[1:], " AB =", AB)
# zapis trójliniowy: współczynnik c_ik po lewej
chi = {1: {"11": 1, "22": 1}, 2: {"21": 1, "22": -1}, 3: {"12": 1, "22": 1},
       4: {"11": 1, "21": 1}, 5: {"12": 1, "11": -1}, 6: {"22": 1}, 7: {"11": 1}}
for i, k in it.product((1, 2), repeat=2):
    assert sum(S[r] * chi[r].get(f"{i}{k}", 0) for r in range(1, 8)) == AB[i - 1][k - 1]
L = 10
dodawania = sum(7 ** k * 4 ** (L - k) for k in range(L))
assert dodawania <= Fraction(4, 3) * 7 ** L
print(f"Strassen N=1024: 7^10={7**10}, 8^10={8**10}, sum 7^k 4^(L-k)={dodawania}")

# ---------------------------------------------------------------- Lemat 6
for _ in range(200):
    w = {s: random.randint(-9, 9) for s in LEWE + PRAWE}
    ph = {(i, j): ev(phat(i, j), w) for i, j in it.product((1, 2, 3), repeat=2)}
    qh = {(i, j): ev(qhat(i, j), w) for i, j in it.product((1, 2, 3), repeat=2)}
    for j in (1, 2, 3):
        assert sum(ph[i, j] for i in (1, 2, 3)) == 0
    for i in (1, 2, 3):
        assert sum(qh[i, j] for j in (1, 2, 3)) == 0
    C = {l: ev(PHI[l], w) * ev(PSI[l], w) for l in SKL}
    for i, j in it.product((1, 2, 3), repeat=2):
        lewa = sum(C[l] for l in SKL if wnosi(l, f"z{i}{j}"))
        x, y = w[f"x{i}"], w[f"y{j}"]
        assert lewa == x * y + x * qh[i, j] + ph[i, j] * y + ph[i, j] * qh[i, j]
    lewa0 = sum(C.values())
    assert lewa0 == sum(w[f"p{i}{j}"] * w[f"q{i}{j}"] for i in (1, 2) for j in (1, 2))
print("Lemat 6: OK (200 losowych podstawień)")

# przykład liczbowy ze slajdu
w = dict(x1=1, x2=2, x3=-1, y1=2, y2=0, y3=1,
         p11=1, p12=2, p21=3, p22=4, q11=1, q12=-1, q21=2, q22=1)
ph = [[ev(phat(i, j), w) for j in (1, 2, 3)] for i in (1, 2, 3)]
qh = [[ev(qhat(i, j), w) for j in (1, 2, 3)] for i in (1, 2, 3)]
print("przyklad: p^ =", ph, " q^ =", qh)
C = {l: ev(PHI[l], w) * ev(PSI[l], w) for l in SKL}
print("przyklad: phi =", {l: ev(PHI[l], w) for l in SKL})
print("przyklad: psi =", {l: ev(PSI[l], w) for l in SKL})
print("przyklad: iloczyny =", C)
print("przyklad: z0 =", sum(C.values()), " <p,q> =",
      sum(w[f"p{i}{j}"] * w[f"q{i}{j}"] for i in (1, 2) for j in (1, 2)))
for i, j in it.product((1, 2, 3), repeat=2):
    print(f"   z{i}{j}: C={C[f'P{i}{j}']}, x_i y_j={w[f'x{i}'] * w[f'y{j}']},"
          f" blad={C[f'P{i}{j}'] - w[f'x{i}'] * w[f'y{j}']}")

# tabela gamma
GAMMA = {}
for s, t, z in it.product(LEWE, PRAWE, WYJ):
    GAMMA[s, t, z] = sum(PHI[l].get(s, 0) * PSI[l].get(t, 0) for l in SKL if wnosi(l, z))
    assert GAMMA[s, t, z] in (-1, 0, 1)
for s, t, z, oczek in (("x1", "y1", "z11", 1), ("p11", "q11", "z0", 1), ("x1", "q11", "z11", 1),
                       ("x1", "q11", "z13", -1), ("p11", "y1", "z31", -1), ("x1", "y1", "z0", 0),
                       ("x1", "y2", "z11", 0), ("p22", "q22", "z0", 1), ("p11", "q12", "z0", 0), ("x2", "q21", "z21", 1)):
    assert GAMMA[s, t, z] == oczek, (s, t, z)
print("gamma: przyklady OK; niezerowych:", sum(1 for v in GAMMA.values() if v))


# ---------------------------------------------------------------- Full
def full(a, b, L):
    """a, b: słowniki krotka-zmiennych -> liczba; zwraca (wynik, liczba mnożeń)."""
    if L == 0:
        return {(): a[()] * b[()]}, 1
    Cl, mn = {}, 0
    for lam in SKL:
        Al = {u[1:]: 0 for u in a}
        Bl = {v[1:]: 0 for v in b}
        for u, val in a.items():
            Al[u[1:]] += PHI[lam].get(u[0], 0) * val
        for v, val in b.items():
            Bl[v[1:]] += PSI[lam].get(v[0], 0) * val
        Cl[lam], k = full(Al, Bl, L - 1)
        mn += k
    c = {}
    for z in WYJ:
        for w2 in Cl["P0"]:
            c[(z,) + w2] = sum(Cl[l][w2] for l in SKL if wnosi(l, z))
    return c, mn


def zbior_wew(slowo):
    return frozenset(i + 1 for i, s in enumerate(slowo) if s[0] in "pq" or s == "z0")


for L, m in ((2, 1), (3, 1), (3, 2)):
    N0, D = 3 ** (L - m), 4 ** m
    Qs = [frozenset(c) for c in it.combinations(range(1, L + 1), m)]
    X = {Q: [[random.randint(-5, 5) for _ in range(D)] for _ in range(N0)] for Q in Qs}
    Y = {Q: [[random.randint(-5, 5) for _ in range(N0)] for _ in range(D)] for Q in Qs}
    wiersze = list(it.product(["x1", "x2", "x3"], repeat=L - m))
    kolumny = list(it.product(["y1", "y2", "y3"], repeat=L - m))
    wew = list(it.product([(1, 1), (1, 2), (2, 1), (2, 2)], repeat=m))

    def sklej(Q, zew, wewn):
        zew, wewn, out = list(zew), list(wewn), []
        for l in range(1, L + 1):
            out.append(wewn.pop(0) if l in Q else zew.pop(0))
        return tuple(out)

    a = {u: 0 for u in it.product(LEWE, repeat=L)}
    b = {v: 0 for v in it.product(PRAWE, repeat=L)}
    for Q in Qs:
        for r, row in enumerate(wiersze):
            for c, pi in enumerate(wew):
                a[sklej(Q, row, [f"p{i}{j}" for i, j in pi])] = X[Q][r][c]
        for r, pi in enumerate(wew):
            for c, col in enumerate(kolumny):
                b[sklej(Q, col, [f"q{i}{j}" for i, j in pi])] = Y[Q][r][c]
    wynik, mn = full(a, b, L)
    assert mn == 10 ** L
    for Q in Qs:
        for r, row in enumerate(wiersze):
            for c, col in enumerate(kolumny):
                zs = [f"z{x[1]}{y[1]}" for x, y in zip(row, col)]
                w_ = sklej(Q, zs, ["z0"] * m)
                assert zbior_wew(w_) == Q
                assert wynik[w_] == sum(X[Q][r][k] * Y[Q][k][c] for k in range(D))
    # Lemat 8 na losowych wejściach (L=2)
    if L == 2:
        ar = {u: random.randint(-3, 3) for u in a}
        br = {v: random.randint(-3, 3) for v in b}
        wr, _ = full(ar, br, L)
        for w_ in wr:
            ex = sum(math.prod(GAMMA[u[l], v[l], w_[l]] for l in range(L)) * ar[u] * br[v]
                     for u in ar for v in br)
            assert ex == wr[w_]
        print("Lemat 7/8 (L=2): OK")
    print(f"Lemat 9 L={L} m={m}: OK  (K={len(Qs)} iloczynów {N0}x{D}x{N0}, {mn} mnożeń)")


# ---------------------------------------------------------------- Pruned
def liscie_wnoszace(w_):
    opcje = [SKL if z == "z0" else ["P" + z[1:]] for z in w_]
    return set(it.product(*opcje))


def pruned(S, k, L, licznik, sciezka=()):
    licznik["rozmiar"] += len(S)
    if k == L:
        licznik["liscie"].add(sciezka)
        return
    for lam in SKL:
        Sl = {w_[1:] for w_ in S if wnosi(lam, w_[0])}
        if Sl:
            pruned(Sl, k + 1, L, licznik, sciezka + (lam,))


U = {("z13", "z0"), ("z0", "z21")}
lic = {"rozmiar": 0, "liscie": set()}
pruned(U, 0, 2, lic)
assert lic["liscie"] == set().union(*(liscie_wnoszace(w_) for w_ in U))
print("Pruned przyklad L=2:", len(lic["liscie"]), "liści, suma rozmiarów", lic["rozmiar"])

for L, m in ((4, 1), (4, 2), (5, 2)):
    wszystkie = [w_ for w_ in it.product(WYJ, repeat=L) if len(zbior_wew(w_)) == m]
    for _ in range(20):
        U = set(random.sample(wszystkie, random.randint(1, 30)))
        lic = {"rozmiar": 0, "liscie": set()}
        pruned(U, 0, L, lic)
        lv = set().union(*(liscie_wnoszace(w_) for w_ in U))
        assert lic["liscie"] == lv
        assert lic["rozmiar"] <= (L + 1) * len(lv)
        bound = sum(min(len(U) * math.comb(m, d) * 9 ** d,
                        math.comb(L, m - d) * 9 ** (L - m + d)) for d in range(m + 1))
        assert len(lv) <= bound
print("Lemat 10 i pierwsza nierówność Lematu 11: OK")

# ---------------------------------------------------------------- rzędy: L=6, m=2
L, m = 6, 2
M = math.comb(L, m) * 9 ** (L - m)
w_ = ("z13", "z0", "z21", "z33", "z0", "z12")
lv = liscie_wnoszace(w_)
rzad = lambda t: m - sum(1 for s in t if s == "P0")
for d in range(m + 1):
    ad = math.comb(m, d) * 9 ** d
    bd = math.comb(L, m - d) * 9 ** (L - m + d)
    assert sum(1 for t in lv if rzad(t) == d) == ad
    assert M * ad == bd * math.comb(L - m + d, d)
    print(f"L=6 m=2 d={d}: alpha={ad}, beta={bd}, udzial={math.comb(L - m + d, d)}")
print("M =", M)

# ---------------------------------------------------------------- L = 19m
for m in range(1, 60):
    L = 19 * m
    M = math.comb(L, m) * 9 ** (L - m)
    beta = [math.comb(L, m - d) * 9 ** (L - m + d) for d in range(m + 1)]
    assert beta[0] == M
    for d in range(1, m + 1):
        assert Fraction(beta[d], beta[d - 1]) == Fraction(9 * (m - d + 1), L - m + d)
        assert 2 ** d * beta[d] <= M
    mala = sum(math.comb(m, d) * 9 ** d for d in range(m + 1) if 9 * d <= m)
    assert mala ** 9 < 2 ** (8 * m)  # < 2^m 2^{-m/9}
    duza = sum(beta[d] for d in range(m + 1) if 9 * d > m)
    assert duza ** 9 * 2 ** m < (2 * M) ** 9  # < 2 * 2^{-m/9} M
print("(5) i druga nierówność Lematu 11 dla m=1..59: OK")

for m in (10, 50, 200):
    for c in (10, 19):
        L = c * m
        r = (10 ** L / (math.comb(L, m) * 9 ** (L - m)))
        print(f"10^L/M dla L={c}m, m={m}: {r:.4g} = D^{math.log(r) / math.log(4 ** m):.4f}")
assert 72 * Fraction(9, 8) ** 9 < 208
assert 19 * math.e * 3 ** 18 < 4 ** 18
assert 10 ** 19 * 2 ** (1 / 9) / 3 ** 18 < 4 ** 18
print(f"72(9/8)^9 = {72 * (9 / 8) ** 9:.3f};  19e 3^18 = {19 * math.e * 3 ** 18:.4e};"
      f"  10^19 2^(1/9)/3^18 = {10 ** 19 * 2 ** (1 / 9) / 3 ** 18:.4e};  4^18 = {4 ** 18:.4e}")

print("WSZYSTKO OK")
