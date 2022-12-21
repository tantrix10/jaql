from typing import Any

from src_py.token_type import TokenType


class Token:
    def __init__(self, type: TokenType, lexeme: str, line: int, literal: Any = None):
        self.type: TokenType = type
        self.lexeme: str = lexeme
        self.line: int = line
        self.literal: Any = literal

    def to_string(self):
        output = f"Type: {self.type}, Lexeme: {self.lexeme}"

        if self.type in (TokenType.STRING, TokenType.NUMBER):
            output += f", Literal: {self.literal_to_string()}"

        return output

    def literal_to_string(self):
        """
        Right now clearly not needed because of python casting, but will become
        needed for numerical printing
        """
        match self.type:
            case TokenType.STRING:
                return self.literal
            case TokenType.NUMBER:
                return self.literal
            case _:
                return ""
