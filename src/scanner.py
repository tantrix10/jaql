import logging

from src.exceptions import JaqlException
from src.jaql import Jaql
from src.token import Token
from src.token_type import TokenType


class Scanner:
    def __init__(self, source: str, jaql: Jaql, debug=False) -> None:
        self.source = source
        self.jaql = jaql
        self.debug = debug
        self.size = len(source)
        self.current = 0
        self.start = 0
        self.line = 1
        self.tokens: list[Token] = []
        self.reserved_words = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
        }

    def is_at_end(self):
        return self.current >= self.size

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, token_type: TokenType, literal=None):
        self.tokens.append(
            Token(
                token_type,
                self.source[self.start : self.current],
                self.line,
                literal,
            )
        )

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self):
        if (self.current + 1) >= self.size:
            return "\0"
        return self.source[self.current + 1]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            # TODO: raise exceptions up the stack proper
            # Maybe want the main jaql to inherit everything?
            self.jaql.add_error(self.line, "Unterminated sring")

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, literal=value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
            if self.peek() == "." and self.peek_next().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.advance()
        ident = self.source[self.start : self.current]

        if token_type := self.reserved_words.get(ident):
            self.add_token(token_type)
        else:
            self.add_token(TokenType.IDENTIFIER)

    def scan_token(self):
        c = self.advance()
        match c:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.add_token(TokenType.COMMA)
            case ".":
                self.add_token(TokenType.DOT)
            case "-":
                self.add_token(TokenType.MINUS)
            case "+":
                self.add_token(TokenType.PLUS)
            case ";":
                self.add_token(TokenType.SEMICOLON)
            case "*":
                self.add_token(TokenType.STAR)
            case "!":
                if self.match("="):
                    token_type = TokenType.BANG_EQUAL
                else:
                    token_type = TokenType.BANG
                self.add_token(token_type)

            case "=":
                if self.match("="):
                    token_type = TokenType.EQUAL_EQUAL
                else:
                    token_type = TokenType.EQUAL
                self.add_token(token_type)

            case "<":
                if self.match("="):
                    token_type = TokenType.LESS_EQUAL
                else:
                    token_type = TokenType.LESS
                self.add_token(token_type)

            case ">":
                if self.match("="):
                    token_type = TokenType.GREATER_EQUAL
                else:
                    token_type = TokenType.GREATER
                self.add_token(token_type)

            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)

            case " ":
                pass
            case "\r":
                pass
            case "\t":
                # Ignore whitespace.
                pass

            case "\n":
                self.line += 1

            case '"':
                self.string()

            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha() or c == "_":
                    self.identifier()
                else:
                    self.jaql.add_error(self.line, "Unexpected character.")

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOJF, "", self.line))

        if self.debug:
            for token in self.tokens:
                print(token.to_string())
        return self.tokens
