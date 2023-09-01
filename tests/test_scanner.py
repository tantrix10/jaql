import pytest

from src.scanner import Scanner
from src.token_type import TokenType
from src.jaql import Jaql


@pytest.mark.parametrize(
    "input,token_type",
    (
        ("and", TokenType.AND),
        ("class", TokenType.CLASS),
        ("else", TokenType.ELSE),
        ("false", TokenType.FALSE),
        ("for", TokenType.FOR),
        ("fun", TokenType.FUN),
        ("if", TokenType.IF),
        ("nil", TokenType.NIL),
        ("or", TokenType.OR),
        ("print", TokenType.PRINT),
        ("return", TokenType.RETURN),
        ("super", TokenType.SUPER),
        ("this", TokenType.THIS),
        ("true", TokenType.TRUE),
        ("var", TokenType.VAR),
        ("while", TokenType.WHILE),
        ("(", TokenType.LEFT_PAREN),
        (")", TokenType.RIGHT_PAREN),
        ("{", TokenType.LEFT_BRACE),
        ("}", TokenType.RIGHT_BRACE),
        (",", TokenType.COMMA),
        (".", TokenType.DOT),
        ("-", TokenType.MINUS),
        ("+", TokenType.PLUS),
        (";", TokenType.SEMICOLON),
        ("*", TokenType.STAR),
        ("!=", TokenType.BANG_EQUAL),
        ("!", TokenType.BANG),
        ("==", TokenType.EQUAL_EQUAL),
        ("=", TokenType.EQUAL),
        ("<=", TokenType.LESS_EQUAL),
        ("<", TokenType.LESS),
        (">=", TokenType.GREATER_EQUAL),
        (">", TokenType.GREATER),
        ("/", TokenType.SLASH),
    ),
)
def test_reserved_words_and_tokens_parsing(input, token_type):
    jaql = Jaql('')
    scanner = Scanner(input, jaql)
    scanner.scan_tokens()
    assert scanner.tokens[0].type == token_type


@pytest.mark.parametrize(
    "input",
    (
        ("\r",),
        ("\t",),
        ("\n",),
        (" ",),
    ),
)
def test_none_tokens(input):
    """
    Note: You cannot have a file of just //, '', or whitespace
    greater than 1-space. Something to fix
    """
    jaql = Jaql('')
    scanner = Scanner(input, jaql)
    scanner.scan_tokens()
    assert scanner.tokens[0].type == TokenType.EOJF
