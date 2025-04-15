from typing import Dict, Set, Tuple, List

EPS = "ε"  # Marker pentru epsilon

# ────────────────────────── parsare ──────────────────────────
def _parse(lines: List[str]) -> Dict[str, Set[Tuple[str, ...]]]:
    g: Dict[str, Set[Tuple[str, ...]]] = {}
    for l in lines:
        L, R = l.split("->")
        L = L.strip()
        for alt in R.split("|"):
            alt = alt.strip()
            g.setdefault(L, set()).add(
                tuple(alt) if alt and alt != EPS else tuple()
            )
    return g

# ───────────────── ε-eliminare ─────────────────
def _rm_eps(g: Dict[str, Set[Tuple[str, ...]]], start="S"):
    nullable, changed = set(), True
    while changed:
        changed = False
        for A, prods in g.items():
            if (
                A not in nullable
                and any((not p) or all(s in nullable for s in p) for p in prods)
            ):
                nullable.add(A)
                changed = True

    ng = {A: set() for A in g}
    for A, prods in g.items():
        for p in prods:
            # toate submulțimile pozițiilor nullable
            idx = [i for i, s in enumerate(p) if s in nullable]
            subsets = [[]]
            for i in idx:
                subsets += [old + [i] for old in subsets]
            for sub in subsets:
                alt = tuple(sym for i, sym in enumerate(p) if i not in sub)
                if alt or A == start:
                    ng[A].add(alt)
    return ng

# ───────────── unit-removal ─────────────
def _rm_unit(g: Dict[str, Set[Tuple[str, ...]]]):
    ng = {A: set() for A in g}
    for A in g:
        stack, seen = [A], set()
        while stack:
            X = stack.pop()
            for p in g[X]:
                if len(p) == 1 and p[0].isupper():
                    B = p[0]
                    if B not in seen:
                        seen.add(B)
                        stack.append(B)
                else:
                    ng[A].add(p)
    return ng

# ─────── neproductive & inaccesibile ───────
def _rm_useless(g: Dict[str, Set[Tuple[str, ...]]], start="S"):
    # productive
    prod, changed = set(), True
    while changed:
        changed = False
        for A, prods in g.items():
            if A not in prod and any(
                all((not s.isupper()) or s in prod for s in p) for p in prods
            ):
                prod.add(A)
                changed = True
    g = {
        A: {p for p in prods if all((not s.isupper()) or s in prod for s in p)}
        for A, prods in g.items() if A in prod
    }
    # accessible
    acc, changed = {start}, True
    while changed:
        changed = False
        for A in list(acc):
            for p in g.get(A, []):
                for s in p:
                    if s.isupper() and s in g and s not in acc:
                        acc.add(s)
                        changed = True
    return {A: prods for A, prods in g.items() if A in acc}

# ───────── terminals → variabile ─────────
def _term_to_var(g: Dict[str, Set[Tuple[str, ...]]]):
    mp, cnt, extra = {}, 1, {}
    for A, prods in g.items():
        newset = set()
        for p in prods:
            if len(p) >= 2:
                rep = []
                for s in p:
                    if s.isupper():
                        rep.append(s)
                    else:
                        if s not in mp:
                            v = f"T{cnt}"
                            cnt += 1
                            mp[s] = v
                            extra[v] = {(s,)}
                        rep.append(mp[s])
                newset.add(tuple(rep))
            else:
                newset.add(p)
        g[A] = newset
    g.update(extra)
    return g

# ───────────── spargere RHS lungi ─────────────
def break_long(
    g: Dict[str, Set[Tuple[str, ...]]], prefix="X"
) -> Dict[str, Set[Tuple[str, ...]]]:
    """
    Fiecare A → X1 X2 … Xk (k ≥ 3) devine un lanț binar:
      A → X1 aux1
      aux1 → X2 aux2
      …
      auxN → Xk-1 Xk
    """
    newg: Dict[str, Set[Tuple[str, ...]]] = {A: set() for A in g}
    fresh_id = 1

    def fresh() -> str:
        nonlocal fresh_id
        v = f"{prefix}{fresh_id}"
        fresh_id += 1
        newg.setdefault(v, set())
        return v

    for A, prods in g.items():
        for rhs in prods:
            if len(rhs) <= 2:
                newg[A].add(rhs)
            else:
                first, *rest = rhs
                aux = fresh()
                newg[A].add((first, aux))

                prev = aux
                while len(rest) > 2:
                    sym, *rest = rest
                    nxt = fresh()
                    newg[prev].add((sym, nxt))
                    prev = nxt

                newg[prev].add(tuple(rest))
    return newg

# ─────────────────── public ────────────────────
def to_cnf(lines: List[str], start="S"):
    g = _parse(lines)
    print("► Gramatica inițială:")
    print(pretty(g), "\n")

    g = _rm_eps(g, start)
    print("► După eliminarea ε-productions:")
    print(pretty(g), "\n")

    g = _rm_unit(g)
    print("► După eliminarea unit-productions:")
    print(pretty(g), "\n")

    g = _rm_useless(g, start)
    print("► După eliminarea simbolurilor neproductive/inaccesibile:")
    print(pretty(g), "\n")

    g = _term_to_var(g)
    print("► După înlocuirea terminalelor din RHS-uri lungi cu variabile:")
    print(pretty(g), "\n")

    g = break_long(g)
    print("► Forma Normală Chomsky (final):")
    print(pretty(g), "\n")

    return g

def pretty(g: Dict[str, Set[Tuple[str, ...]]]) -> str:
    return "\n".join(
        f"{A} → {' | '.join(''.join(p) if p else EPS for p in sorted(g[A]))}"
        for A in sorted(g)
    )

# — exemple de rulare —
variant1 = [
    "S->aB", "S->AC",
    "A->a",  "A->ASC", "A->BC", "A->aD",
    "B->b",  "B->bS",
    "C->ε",  "C->bA",
    "E->aB",
    "D->abC",
]

cnf = to_cnf(variant1, start="S")
