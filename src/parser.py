from src.exceptions import JaqlException, JaqlParseException
from src.token import Token
from src.token_type import TokenType
from src.types.Expr import Binary, Expr, Grouping, Literal, Unary
from src.ast_printer import ASTPrinter

class Parser:
    def __init__(self, tokens: list[Token], jaql, debug=False) -> None:
        self.tokens = tokens
        self.jaql = jaql
        self.debug = debug
        self.size = len(tokens)
        self.current = 0
        self.has_error = False

    def parse(self):
        try:
            exprs = self.expression()
            if self.debug:
                printer = ASTPrinter()
                print(printer.print(expr=exprs))
            return exprs
        except JaqlParseException:
            return None

    def error(self, token: Token, message: str):
        self.jaql.add_error(token.line, message)

    def syncronise(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type is TokenType.SEMICOLON:
                return
            match self.peek().type:
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            self.advance()

    def previous(self):
        return self.tokens[self.current - 1]

    def peek(self):
        return self.tokens[self.current]

    def is_at_end(self):
        return self.peek().type is TokenType.EOJF

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType):
        if self.is_at_end():
            return False
        return self.peek().type is type

    def match(self, types: list[TokenType]):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        self.jaql.add_error("", message)

    def primary(self):
        if self.match(
            [
                TokenType.FALSE,
            ]
        ):
            return Literal(False)
        elif self.match(
            [
                TokenType.TRUE,
            ]
        ):
            return Literal(True)
        elif self.match(
            [
                TokenType.NIL,
            ]
        ):
            return Literal(None)
        elif self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        elif self.match(
            [
                TokenType.LEFT_PAREN,
            ]
        ):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "expected ')' after expression")
            return Grouping(expr)
        return Literal(None)  # not needed, but keeps mypy happy :)

    def unary(self):
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            return Unary(operator, right)
        return self.primary()

    def factor(self):
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator: Token = self.previous()
            right: Expr = self.unary()
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator: Token = self.previous()
            right: Expr = self.factor()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(
            [
                TokenType.GREATER,
                TokenType.GREATER_EQUAL,
                TokenType.LESS,
                TokenType.LESS_EQUAL,
            ]
        ):
            operator: Token = self.previous()
            right: Expr = self.term()
            expr = Binary(expr, operator, right)
        return expr

    def equality(self):
        expr = self.comparison()
        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL]):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def expression(self):
        return self.equality()
