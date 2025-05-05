# Chomsky Normal Form Converter

**Disciplina**: Limbaje Formale și Automate Finite
**Autor**: Blindu Andi
**Variantă**: 2

---

## 1. Teorie

Forma Normală Chomsky (Chomsky Normal Form – CNF) este o restricție standard aplicată gramaticilor independente de context (CFG – Context-Free Grammars), cu rol de a simplifica analiza sintactică și demonstrațiile teoretice.

O gramatică este în **CNF** dacă **fiecare regulă de producție** este de una dintre următoarele forme:

* `A → BC` – unde `A`, `B`, `C` sunt **simboluri neterminale** (`B`, `C` ≠ simbol de start);
* `A → a` – unde `a` este un **simbol terminal**;
* Excepțional: `S → ε` este permis **doar dacă** `ε` (șirul vid) face parte din limbajul generat.

### Avantaje ale CNF:

* Este esențială pentru algoritmi de parsare eficienți (ex: **Cocke–Younger–Kasami (CYK)**);
* Permite analiza decizională mai ușoară (ex: verificarea apartenenței unui șir la limbaj);
* Este un punct de plecare pentru demonstrarea echivalenței între CFG și automate cu stivă (PDA);
* Ușurează procesul de optimizare a parserelor pentru compilatoare și interpretoare.

---

## 2. Obiective

Scopul principal este construirea unui convertor automat care transformă o gramatică CFG arbitrară în formă CNF, respectând următoarea secvență de pași:

1. **Eliminarea ε-producțiilor** – reguli care generează șirul vid;
2. **Eliminarea unit-producțiilor** – reguli de forma `A → B`, unde atât A, cât și B sunt neterminale;
3. **Eliminarea simbolurilor neproductive și inaccesibile** – curățare a gramaticii de simboluri inutile;
4. **Transformarea terminalelor din producții complexe în simboluri intermediare**;
5. **Descompunerea producțiilor lungi în lanțuri binare** (`A → BCD` → `A → BX`, `X → CD`).

Vom implementa acești pași într-un program Python modular, ce permite și testarea pe gramatici multiple.

---

## 3. Descrierea implementării

Am organizat codul în mai multe funcții, fiecare ocupându-se de o etapă specifică a transformării. Două exemple importante sunt detaliate mai jos.

### 3.1 Parsare gramatică din input:

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

Această funcție transformă regulile într-o structură de date bazată pe dicționare Python:

* cheia este neterminalul stâng (`LHS`),
* valoarea este o **mulțime de tupluri** reprezentând părțile drepte ale producțiilor.

### 3.2 Eliminarea ε-producțiilor:

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

Această funcție identifică simbolurile nullable (care pot duce la `ε`) și creează toate variantele posibile ale producțiilor eliminând aparițiile acestora.

---

### 3.3 Alte funcții cheie

* **`_rm_unit`** – elimină toate regulile `A → B`, propagând direct regulile lui `B` în `A`.
* **`_rm_useless`** – filtrează simboluri care:

  * nu pot duce la terminale (neproductive);
  * nu pot fi atinse din simbolul de start (inaccesibile).
* **`_term_to_var`** – pentru producții precum `A → aB`, introduce un nou neterminal `T1 → a`, apoi `A → T1B`.
* **`_break_long`** – transformă reguli de lungime > 2, ca `A → BCD`, într-un lanț de reguli binare:

  ```text
  A  → BX1  
  X1 → CX2  
  X2 → D
  ```
* **`to_cnf`** – funcție orchestrator care aplică toți pașii de mai sus în ordine corectă.
* **`pretty`** – formatează gramatica într-un format textual lizibil.

---

## 4. Rezultate obținute

Am testat implementarea pe **varianta 1** din laborator:

```python
variant1 = [
    "S->aB", "S->AC",
    "A->a",  "A->ASC", "A->BC", "A->aD",
    "B->b",  "B->bS",
    "C->ε",  "C->bA",
    "E->aB",
    "D->abC"
]
```

### Ieșiri intermediare:

1. **Inițial**:

   * Reguli complexe, terminale amestecate cu neterminale, `ε` și `unit-productions` prezente.
2. **După eliminare `ε`**:

   * Reguli alternative generate pentru a reflecta prezența sau absența simbolului `C`.
3. **După eliminare unități**:

   * Toate regulile de tip `A → B` dispar. Se înlocuiesc cu regulile `B`.
4. **Simboluri neproductive**:

   * `E` este eliminat (nu e accesibil din `S`).
5. **După transformări terminale și binare**:

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

Am adăugat neterminale noi (`T1`, `T2`, `X1`, etc.) pentru a respecta forma strictă CNF.

---

## 5. Concluzii

Am construit un convertor complet pentru transformarea CFG în Chomsky Normal Form. Am aplicat toți pașii standard din teorie, cu vizibilitate asupra etapelor intermediare pentru depanare și verificare.

### Beneficii ale implementării:

* **Genericitate** – poate procesa orice gramatică CFG dată sub formă de liste de stringuri;
* **Modularitate** – ușor de extins, de exemplu pentru input din fișiere `.txt`;
* **Educațional** – afișarea pașilor intermediari permite întelegerea profundă a procesului de conversie.

### Posibile îmbunătățiri viitoare:

* Interfață grafică pentru vizualizarea arborelui de derivare;
* Suport pentru reguli cu simboluri multiple pe partea stângă (ex: meta-gramatici);
* Optimizări de performanță pentru gramatici mari.

---

## 6. Referințe

* Chomsky, N. (1959). *On certain formal properties of grammars*. *Information and Control*.
* Aho, A. V., & Ullman, J. D. (1972). *The Theory of Parsing, Translation, and Compiling*.
* Hopcroft, J. E., Motwani, R., & Ullman, J. D. (2006). *Introduction to Automata Theory, Languages, and Computation* (3rd ed.).
* Lecture notes – Universitatea Tehnică a Moldovei, curs "Limbaje Formale și Automate Finite".
