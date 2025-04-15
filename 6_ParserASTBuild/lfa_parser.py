# src/lfa_parser.py
from lexer import Lexer, TokenType
from ast_nodes import Number, Variable, BinaryOp, UnaryOp

class Parser:
    def __init__(self, text: str):
        self.lexer = Lexer(text)
        self.current = self.lexer.next_token()

    def eat(self, token_type: TokenType):
        if self.current.type == token_type:
            self.current = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current.type}")

    def parse(self):
        node = self.expr()
        if self.current.type != TokenType.EOF:
            raise SyntaxError("Extra input after end of expression")
        return node

    def expr(self):
        node = self.term()
        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current.lexeme
            self.eat(self.current.type)
            node = BinaryOp(op, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current.type in (TokenType.MUL, TokenType.DIV):
            op = self.current.lexeme
            self.eat(self.current.type)
            node = BinaryOp(op, node, self.factor())
        return node

    def factor(self):
        tok = self.current
        # unary + or -
        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            self.eat(tok.type)
            return UnaryOp(tok.lexeme, self.factor())
        # number literal
        elif tok.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(float(tok.lexeme))
        # identifier
        elif tok.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(tok.lexeme)
        # parenthesized expression
        elif tok.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        else:
            raise SyntaxError(f"Unexpected token {tok}")
