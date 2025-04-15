# Chomsky Normal Form Converter

**Course**: Formal Languages & Finite Automata   
**Author**: Blindu Andi   
**Variant**: 2

## 1. Teorie

Forma Normală Chomsky (CNF) este o formă canonică pentru gramatici independente de context.
O gramatică este în CNF dacă fiecare producție respectă una din cele două forme:

* `A → BC`, unde `A`, `B`, `C` sunt variabile (simboluri neterminale), iar `B`, `C` nu sunt simbolul de start.
* `A → a`, unde `a` este un terminal.

Singura excepție permisă este producția `S → ε`, unde `S` este simbolul de start și `ε` apare doar dacă limbajul conține șirul vid.

**De ce CNF?**

* Este punct de plecare pentru algoritmi standard de parsare (de exemplu Cocke–Younger–Kasami).
* Simplifică demonstrațiile teoretice (ex. echivalența cu PDA).
* Permite verificarea proprietăților de decizie (emptiness, membership) cu complexitate polinomială.

## 2. Obiective

Să înțelegem pașii de normalizare a unei gramatici:

1. Eliminarea producțiilor `ε`.
2. Eliminarea unit-producțiilor.
3. Eliminarea simbolurilor neproductive și inaccesibile.
4. Transformarea terminalelor din părți drepte cu lungime ≥ 2 în variabile proxy.
5. Spargerea oricărei producții cu lungime > 2 în lanțuri binare.

Să implementăm în Python un convertor generic care primește orice gramatică independentă de context și o transformă în CNF.
Să testăm funcționalitatea pe varianta 2 a laboratorului și să afișăm fiecare etapă intermediară pentru a valida corectitudinea.

**(BONUS)** Să adaptăm metoda astfel încât să poată primi și alte gramatici, nu doar pe cea din temă.

## 3. Descrierea implementării

Am structurat convertorul în câteva funcții principale. Iată două exemple detaliate și restul sumarizate:

```python
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
```

```python
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
```

Restul funcțiilor implementate (fără afișarea codului):

* `_rm_unit`: elimină unit-producțiile (`A → B`).
* `_rm_useless`: înlătură simbolurile neproductive și inaccesibile.
* `_term_to_var`: înlocuiește terminalele din părți drepte lungi cu variabile proxy.
* `_break_long`: sparge producțiile cu mai mult de două simboluri în lanțuri binare.
* `to_cnf`: orchetrează apelurile în ordine: parsing, \_rm\_eps, \_rm\_unit, \_rm\_useless, \_term\_to\_var, \_break\_long.
* `pretty`: formatează gramatica rezultată într-un șir de caractere pentru afișare.

Fiecare funcție se ocupă de un pas clar în transformarea unei gramatici CFG în formă normală Chomsky.

## 4. Rezultate

Am testat implementarea pe Variant 1:

```python
variant1 = [
    "S->aB", "S->AC",
    "A->a",  "A->ASC", "A->BC", "A->aD",
    "B->b",  "B->bS",
    "C->ε",  "C->bA",
    "E->aB",
    "D->abC"
]
cnf = to_cnf(variant1, start="S")
print(pretty(cnf))
```

**Ieșire intermediară (pe scurt):**

* Gramatică inițială
  `S → aB | AC`
  `A → a | ASC | BC | aD`
  …

* După ε-eliminare
  C nu mai generează ε, dar am adăugat variante fără C în părțile drepte.

* După unit-eliminare
  Toate `A → X` (unde `X` e nonterminal) au dispărut, iar `A` preia direct producțiile lui `X`.

* După eliminarea nefolositorilor
  `S, A, B, C, D` rămân; `E` se exclude dacă nu e accesibil.

* După înlocuirea terminalelor
  Introduc `T1 → a`, `T2 → b` și înlocuiesc, de ex., `abC` → `(T1,T2,C)`.

* **CNF finală**

```text
A  → AS | AX2 | BC | T1D | T2S | a | b
B  → T2S | b
C  → T2A
D  → T1T2 | T1X3
S  → AC | AS | AX1 | BC | T1B | T1D | T2S | a | b
T1 → a
T2 → b
X1 → SC
X2 → SC
X3 → T2C
```

## 5. Concluzii

Am parcurs toţi paşii teoretici de normalizare: ε-eliminare, unit-eliminare, filtre „utile”, transformări de terminale şi „spargeri” binare.

Implementarea generează un convertor generic care poate primi orice gramatică CFG și o transformă în CNF.

Prin afișarea etapelor intermediară, am putut verifica fiecare pas și am eliminat ușor erorile (de exemplu producțiile ε rămase accidental).

Versiunea finală este robustă și poate fi extinsă pentru input din fișiere sau pentru acceptarea de gramatici mai mari.

## 6. Referințe

* Chomsky, N. (1959). *On certain formal properties of grammars*. Information and Control.
* Aho, A. V., & Ullman, J. D. (1972). *The Theory of Parsing, Translation, and Compiling*.
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation*, 3rd ed.
