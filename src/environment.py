from typing import Any

from src.exceptions import JaqlRuntimeError
from src.jaql import Jaql
from src.token import Token


class Environment:
    def __init__(self, jaql: Jaql, enclosing=None) -> None:
        self._final = {}
        self.jaql = jaql
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        # clearly not strictly needed, but making final private
        # gives flexibility on this implementation
        self._final[name] = value

    def get(self, name: Token):
        if name.lexeme in self._final:
            return self._final.get(name.lexeme)
        if self.enclosing is not None:
            return self.enclosing.get(name)
        self.jaql.add_runtime_error(
            JaqlRuntimeError(name, f"Undefined variable {name.lexeme}.")
        )

    def assign(self, name: Token, value: Any):
        if name.lexeme in self._final:
            self._final[name.lexeme] = value
            return None
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None
        self.jaql.add_runtime_error(
            JaqlRuntimeError(name, f"Undefined variable {name.lexeme}.")
        )
