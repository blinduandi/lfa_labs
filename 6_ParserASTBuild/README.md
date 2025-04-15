# Parser & Abstract Syntax Tree Lab Report

**Course**: Formal Languages & Finite Automata   
**Topic**: Parser & Building an Abstract Syntax Tree   
**Author**: Blindu Andi   

## 1. Teorie

**Parsing** este procesul de analiză sintactică a unui șir de tokeni pentru a-i determina structura conform unei gramatici date. Rezultatul tipic este un **parse tree** sau **arbori de sintaxă abstractă** (AST), care reprezintă ierarhic construcțiile din limbaj.

Un **AST** păstrează relațiile semantice dintre noduri (expresii, operatori, variabile) și elimină detaliile de punctuație inutile (de exemplu paranteze explicite), facilitând etapele ulterioare de analiză sau compilare.

## 2. Obiective

1. Definirea unui tip `TokenType` (enum) pentru categorii de tokeni: numere, identificatori, operatori și paranteze.
2. Implementarea unui **lexer** bazat pe expresii regulate, care parcurge textul și emite tokeni tipizați.
3. Crearea structurilor de date pentru nodurile AST: `Number`, `Variable`, `BinaryOp`, `UnaryOp`.
4. Realizarea unui **parser recursive‐descent** pentru gramatica aritmetică:

   ```bnf
   Expr   → Term (('+' | '-') Term)*
   Term   → Factor (('*' | '/') Factor)*
   Factor → ('+' | '-') Factor | Primary
   Primary→ NUMBER | IDENTIFIER | '(' Expr ')'
   ```
5. Dezvoltarea unui driver care execută lexarea și parsing-ul pentru expresii de test și tipărește AST-ul rezultat.

## 3. Descrierea implementării

Am ales două funcții cheie pentru exemplificare și am descris sumar restul:

```python
# În src/lexer.py
class TokenType(Enum):
    NUMBER, IDENTIFIER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto(), auto()

class Lexer:
    def next_token(self) -> Token:
        """
        Folosește un pattern concatenat de regex-uri cu grupuri numite
        pentru fiecare tip de token și returnează următorul Token.
        """
        ...
```

```python
# În src/parser.py
class Parser:
    def expr(self) -> ASTNode:
        node = self.term()
        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current.lexeme
            self.eat(self.current.type)
            node = BinaryOp(op, node, self.term())
        return node
```

Restul componentelor (sumar):

* **AST Nodes** (`src/ast_nodes.py`): clase simple pentru `Number`, `Variable`, `BinaryOp`, `UnaryOp`, fiecare cu constructor și `__repr__`.
* **Parser** (`parser.py`): metode `term()`, `factor()`, `eat()`, `parse()` care aplică regulile gramaticale și verifică `EOF` la final.
* **Driver** (`main.py`): liste statice de expresii de test, instanțiază `Parser`, apelează `parse()` și afișează AST-ul sau erori de sintaxă.

## 4. Rezultate

Am rulat driver-ul pe câteva expresii de test:

```python
tests = [
    "x + 3*(y - 2)",
    "a*(b + c) - 42",
    "-(10 / (2 + z))",
]
for expr in tests:
    print(f"Input: {expr}")
    ast = Parser(expr).parse()
    print(f"AST:   {ast}\n")
```

**Output**:

```
Input: x + 3*(y - 2)
AST:   BinOp(+, Var(x), BinOp(*, Number(3.0), BinOp(-, Var(y), Number(2.0))))

Input: a*(b + c) - 42
AST:   BinOp(-, BinOp(*, Var(a), BinOp(+, Var(b), Var(c))), Number(42.0))

Input: -(10 / (2 + z))
AST:   UnOp(-, BinOp(/, Number(10.0), BinOp(+, Number(2.0), Var(z))))
```

## 5. Concluzii

Am demonstrat un flux complet de la lexare la parsare și construcția AST-ului pentru expresii aritmetice. Codul este modular, iar extensia pentru noi operatori sau reguli se face prin adăugarea de tokeni și metode de parsing corespunzătoare.

Astăzi, AST-urile servesc ca fundament nu doar în compilatoare, ci și în analizatoare statice de cod, interpretoare și generatoare de cod. Structura prezentată poate fi adaptată rapid în astfel de scenarii.

## 6. Referințe

* Aho, A. V., Sethi, R., & Ullman, J. D. (1986). *Compilers: Principles, Techniques, and Tools* (Dragon Book).
* Hopcroft, J. E., & Ullman, J. D. (1979). *Introduction to Automata Theory, Languages, and Computation*.
* Python `re` module documentation: [https://docs.python.org/3/library/re](https://docs.python.org/3/library/re)
