from typing import Optional

from src.ast_printer import ASTPrinter
from src.exceptions import JaqlException, JaqlParseException
from src.jaql import Jaql
from src.token import Token
from src.token_type import TokenType
from src.types.Expr import (
    Assign,
    Binary,
    Call,
    Expr,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from src.types.Stmt import Block, Expression, If, Print, Stmt, Var, While


class Parser:
    def __init__(self, tokens: list[Token], jaql: Jaql, debug=False) -> None:
        self.tokens = tokens
        self.jaql = jaql
        self.debug = debug
        self.size = len(tokens)
        self.current = 0
        self.has_error = False

    def statement(self):
        if self.match(
            [
                TokenType.FOR,
            ]
        ):
            return self.for_statement()
        if self.match(
            [
                TokenType.IF,
            ]
        ):
            return self.if_statement()
        if self.match(
            [
                TokenType.PRINT,
            ]
        ):
            return self.print_statement()
        if self.match([TokenType.WHILE]):
            return self.while_statement()
        if self.match(
            [
                TokenType.LEFT_BRACE,
            ]
        ):
            return Block(self.block())
        return self.expression_statement()

    def declaration(self):
        try:
            if self.match(
                [
                    TokenType.VAR,
                ]
            ):
                return self.var_declaration()
            return self.statement()
        except JaqlParseException:
            self.syncronise()
            return None

    def var_declaration(self):
        name: Token = self.consume(TokenType.IDENTIFIER, "Expect variable name.")  # type: ignore
        initialiser: Optional[Expr] = None

        if self.match(
            [
                TokenType.EQUAL,
            ]
        ):
            initialiser = self.expression()
        self.consume(TokenType.SEMICOLON, "Except ';' after variable declaration")
        return Var(name, initialiser)  # type: ignore

    def parse(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

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

    def block(self):
        statements = []

        while (not self.check(TokenType.RIGHT_BRACE)) and (not self.is_at_end()):
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def for_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after for.")

        initialiser: Optional[Stmt]

        if self.match(
            [
                TokenType.SEMICOLON,
            ]
        ):
            initialiser = None
        elif self.match(
            [
                TokenType.VAR,
            ]
        ):
            initialiser = self.var_declaration()
        else:
            initialiser = self.expression_statement()

        condition: Optional[Expr] = None

        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
            self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition")

        increment: Optional[Expr] = None

        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])

        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        if initialiser is not None:
            body = Block([initialiser, body])

        return body

    def while_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")
        body: Stmt = self.statement()

        return While(condition, body)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after if.")
        condition: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch: Stmt = self.statement()
        else_branch: Optional[Stmt] = None

        if self.match(
            [
                TokenType.ELSE,
            ]
        ):
            else_branch = self.statement()

        return If(condition, then_branch, else_branch)

    def print_statement(self):
        value: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self):
        expr: Expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Expression(expr)

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
        self.jaql.add_error(-1, message)

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
                TokenType.IDENTIFIER,
            ]
        ):
            return Variable(self.previous())
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
        return self.call()
    
    def call(self):
        expr: Expr = self.primary()

        while True:
            if self.match([TokenType.LEFT_PAREN,]):
                expr = self.finish_call(expr)
            else:
                break
        
        return expr
    
    def finish_call(self, callee: Expr):
        arguments: list[Expr] = []

        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= self.jaql.max_arugments:
                    self.jaql.add_error(self.peek().line, f"Can't have more than {self.jaql.max_arugments} arguments")
                arguments.append(self.expression())
                if not self.match([TokenType.COMMA]):
                    break
        
        paren: Token = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments") # type: ignore

        return Call(callee, paren, arguments)

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
        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator: Token = self.previous()
            right: Expr = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def and_(self):
        expr: Expr = self.equality()

        while self.match(
            [
                TokenType.AND,
            ]
        ):
            operator: Token = self.previous()
            right: Expr = self.equality()
            expr = Logical(expr, operator, right)
        return expr

    def or_(self):
        expr: Expr = self.and_()

        while self.match(
            [
                TokenType.OR,
            ]
        ):
            operator: Token = self.previous()
            right: Expr = self.and_()
            expr = Logical(expr, operator, right)
        return expr

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr: Expr = self.or_()

        if self.match(
            [
                TokenType.EQUAL,
            ]
        ):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, Variable):
                name: Token = expr.name
                return Assign(name, value)

            self.jaql.add_error(equals.line, "Invalid assignment")

        return expr
