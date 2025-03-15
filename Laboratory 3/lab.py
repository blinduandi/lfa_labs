#!/usr/bin/env python3
"""
Lexer for a Video Editing DSL.
This lexer is designed for the course Formal Languages & Finite Automata.
Author: Cretu Dumitru (with kudos to Vasile Drumea & Irina Cojuhari)

Supported DSL commands:
  LOAD, CUT, TRIM, FADE, OVERLAY, TRANSITION, EXPORT

The DSL supports:
  - Keywords (e.g., LOAD, CUT, EXPORT)
  - Identifiers (for argument names, e.g., start, end, type)
  - Numbers (integer and float values)
  - String literals (enclosed in double quotes)
  - Symbols: equal sign (=), comma (,), parentheses ( and )
"""

# Token type constants
INTEGER, FLOAT = 'INTEGER', 'FLOAT'
STRING = 'STRING'
IDENTIFIER = 'IDENTIFIER'
LOAD, CUT, TRIM, FADE, OVERLAY, TRANSITION, EXPORT = 'LOAD', 'CUT', 'TRIM', 'FADE', 'OVERLAY', 'TRANSITION', 'EXPORT'
EQUAL, COMMA, LPAREN, RPAREN = 'EQUAL', 'COMMA', 'LPAREN', 'RPAREN'
EOF = 'EOF'

# Reserved keywords dictionary: maps lower-case command to token type.
reserved_keywords = {
    'load': LOAD,
    'cut': CUT,
    'trim': TRIM,
    'fade': FADE,
    'overlay': OVERLAY,
    'transition': TRANSITION,
    'export': EXPORT
}

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {repr(self.value)})"

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0  # current position in input string
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception(f"Invalid character '{self.current_char}' at position {self.pos}")

    def advance(self):
        """Advance the 'pos' pointer and update the current character."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        """Skip over any whitespace characters."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        """
        Return an INTEGER or FLOAT token from the input.
        It handles numbers with or without a decimal point.
        """
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
            result += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(INTEGER, int(result))
        elif dot_count == 1:
            return Token(FLOAT, float(result))
        else:
            self.error()

    def string(self):
        """
        Handle string literals.
        Strings are expected to be enclosed in double quotes.
        """
        self.advance()  # Skip the opening quote
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            self.error()  # Unterminated string literal
        self.advance()  # Skip the closing quote
        return Token(STRING, result)

    def identifier(self):
        """
        Handle identifiers and reserved keywords.
        Identifiers consist of alphanumeric characters and underscores.
        """
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        # Check if the identifier is a reserved keyword.
        token_type = reserved_keywords.get(result.lower(), IDENTIFIER)
        return Token(token_type, result)

    def get_next_token(self):
        """
        Lexical analyzer (tokenizer).
        Breaks the input into tokens one at a time.
        """
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '=':
                self.advance()
                return Token(EQUAL, '=')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

def main():
    # Static DSL script as a multi-line string.
    dsl_script = '''\
LOAD "intro.mp4"
CUT start=10 end=20
FADE type="in" duration=2.5
OVERLAY image="logo.png" position=(100,200)
EXPORT "final_video.mp4"'''

    lexer = Lexer(dsl_script)

    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()
    print(token)  # Print the EOF token

if __name__ == '__main__':
    main()
