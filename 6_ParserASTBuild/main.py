# src/main.py
from lfa_parser import Parser

def run(text: str):
    parser = Parser(text)
    return parser.parse()

if __name__ == "__main__":
    # ── STATIC INPUTS ─────────────────────────────────────────────────────────
    tests = [
        "x + 3*(y - 2)",
        "a*(b + c) - 42",
        "-(10 / (2 + z))",
        "sin(x) + 3 * cos(2)"
    ]

    for expr in tests:
        print(f"\nInput:  {expr}")
        try:
            ast = run(expr)
            print(f"AST:    {ast}")
        except SyntaxError as e:
            print(f"Syntax error: {e}")
