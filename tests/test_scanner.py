import pytest

from src.scanner import Scanner
from src.token_type import TokenType


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
    ),
)
def test_reserved_words_token_parsing(input, token_type):
    scanner = Scanner(input)
    scanner.scan_tokens()
    assert scanner.tokens[0].type == token_type
