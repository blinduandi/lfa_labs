# Lexer & Scanner – Video Editing DSL

**Course:** Formal Languages & Finite Automata  
**Author:** Cretu Dumitru  
**Acknowledgments:** Kudos to Vasile Drumea and Irina Cojuhari  
**Student:** Blindu Andi, FAF-233

---

## 1. Introduction

In this lab, I implemented a lexer for a small DSL (domain-specific language) used to describe basic video editing operations. Lexical analysis is the process of converting a stream of characters into a stream of tokens. These tokens are then used for parsing or interpreting commands.

Rather than building yet another calculator lexer, I created a language that supports commands like `LOAD`, `CUT`, `FADE`, `OVERLAY`, and `EXPORT`, which resemble scripting commands for a hypothetical video editor.

---

## 2. DSL Input Example

The lexer processes input like the following:
```
LOAD "intro.mp4"
CUT start=10 end=20
FADE type="in" duration=2.5
OVERLAY image="logo.png" position=(100,200)
EXPORT "final_video.mp4"
```
Each line is a command with optional arguments and values. The lexer is responsible for identifying each token: commands, string literals, numbers, symbols, and parameter names.

---

## 3. Design and Token Types

The lexer is built in Python using object-oriented principles. It processes one character at a time and recognizes the following token types:

- Keywords: LOAD, CUT, FADE, etc.
- Identifiers: such as "start", "end", "duration"
- Numbers: both integers (10) and floats (2.5)
- Strings: enclosed in double quotes (e.g. "logo.png")
- Symbols: =, (, ), ,

---

## 4. Components and Functionality

The program is structured around two main classes: `Token` and `Lexer`, and a single `main()` function to execute it.

### Token class
This class stores a `type` and a `value`. For example, a token could be `Token(STRING, "intro.mp4")` or `Token(EQUAL, '=')`. It includes a `__str__()` and `__repr__()` for clean printing.

### Lexer class
The heart of the program, responsible for processing the input string. It maintains the current position and character.

#### Function advance()
Moves the character pointer forward by one and updates the current character.
```python
    def advance(self):
        """Advance the 'pos' pointer and update the current character."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]
```
#### Function peek()
Returns the next character in the input without moving the pointer. Used for lookahead.
```python
    def peek(self):
        """Look at the next character without consuming it."""
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        return self.text[peek_pos]
```
#### Function skip_whitespace()
Skips over spaces and newlines, ensuring we only process relevant characters.

#### Function number()
Builds up a numeric token. If it finds a decimal point, it will return a FLOAT token, otherwise INTEGER.

#### Function string()
Collects characters inside double quotes and returns a STRING token. If the string isn't properly closed, it throws an error.

#### Function identifier()
Parses names like `start`, `end`, `type`. It checks whether the identifier matches a known keyword like `LOAD` or `FADE`, returning the correct token type.

#### Function get_next_token()
The main tokenizer. It checks what kind of character we're dealing with and delegates to the appropriate function (e.g., `number()`, `string()`, `identifier()`). It returns one token at a time until it reaches EOF.
```python
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
```
### Function main()
Defines the DSL input script inside the file, passes it to the Lexer, and prints out all tokens one by one. This acts as the entry point for the lexer.

---

## 5. Output Result

When the lexer is run, the input script is tokenized line by line, and you get output like:

```
Token(LOAD, 'LOAD')
Token(STRING, 'intro.mp4')
Token(CUT, 'CUT')
Token(IDENTIFIER, 'start')
Token(EQUAL, '=')
Token(INTEGER, 10)
Token(IDENTIFIER, 'end')
Token(EQUAL, '=')
Token(INTEGER, 20)
Token(FADE, 'FADE')
Token(IDENTIFIER, 'type')
Token(EQUAL, '=')
Token(STRING, 'in')
Token(IDENTIFIER, 'duration')
Token(EQUAL, '=')
Token(FLOAT, 2.5)
Token(OVERLAY, 'OVERLAY')
Token(IDENTIFIER, 'image')
Token(EQUAL, '=')
Token(STRING, 'logo.png')
Token(IDENTIFIER, 'position')
Token(EQUAL, '=')
Token(LPAREN, '(')
Token(INTEGER, 100)
Token(COMMA, ',')
Token(INTEGER, 200)
Token(RPAREN, ')')
Token(EXPORT, 'EXPORT')
Token(STRING, 'final_video.mp4')
Token(EOF, None)
```

This confirms that each part of the script is correctly classified into tokens that can later be used for syntax analysis or interpretation.

---

## 6. Conclusions

This lab helped me better understand how lexers work internally. I got to explore not only how to break down raw input into tokens, but also how to structure the program cleanly, use object-oriented design, and build something useful for a real-world DSL. The result is a reusable and extendable lexer that could be part of a larger interpreter or compiler.

The lexer is deterministic, clean, and easy to read. It was tested with various commands, string formats, and nested symbols.

