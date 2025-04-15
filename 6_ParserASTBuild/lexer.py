# src/lexer.py
import re
from enum import Enum, auto

class TokenType(Enum):
    NUMBER     = auto()
    IDENTIFIER = auto()
    PLUS       = auto()
    MINUS      = auto()
    MUL        = auto()
    DIV        = auto()
    LPAREN     = auto()
    RPAREN     = auto()
    EOF        = auto()

# list of (TokenType, regex) pairs
TOKEN_REGEX = [
    (TokenType.NUMBER,     r"\d+(?:\.\d+)?"),
    (TokenType.IDENTIFIER, r"[A-Za-z_]\w*"),
    (TokenType.PLUS,       r"\+"),
    (TokenType.MINUS,      r"-"),
    (TokenType.MUL,        r"\*"),
    (TokenType.DIV,        r"/"),
    (TokenType.LPAREN,     r"\("),
    (TokenType.RPAREN,     r"\)"),
]

class Token:
    def __init__(self, type: TokenType, lexeme: str):
        self.type = type
        self.lexeme = lexeme
    def __repr__(self):
        return f"{self.type.name}({self.lexeme})"

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        # compile one pattern with named groups
        self.pattern = re.compile(
            "|".join(f"(?P<{t.name}>{p})" for t,p in TOKEN_REGEX)
        )

    def next_token(self) -> Token:
        while self.pos < len(self.text):
            match = self.pattern.match(self.text, self.pos)
            if match:
                for t in TokenType:
                    lex = match.group(t.name)
                    if lex:
                        tok = Token(t, lex)
                        self.pos = match.end()
                        return tok
            if self.text[self.pos].isspace():
                self.pos += 1
                continue
            raise SyntaxError(f"Unexpected character: '{self.text[self.pos]}'")
        return Token(TokenType.EOF, "")
