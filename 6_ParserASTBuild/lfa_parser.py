from lexer import Lexer, TokenType
from ast_nodes import Number, Variable, BinaryOp, UnaryOp, FuncCall

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

        # function call: sin(x), cos(45), etc.
        elif tok.type == TokenType.FUNC:
            func_name = tok.lexeme
            self.eat(TokenType.FUNC)
            self.eat(TokenType.LPAREN)
            arg = self.expr()
            self.eat(TokenType.RPAREN)
            return FuncCall(func_name, arg)

        # number literal
        elif tok.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(float(tok.lexeme))

        # variable
        elif tok.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(tok.lexeme)

        # parentheses
        elif tok.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node

        else:
            raise SyntaxError(f"Unexpected token {tok}")
