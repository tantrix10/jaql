from typing import Any, Optional

from src.exceptions import JaqlRuntimeError
from src.jaql import Jaql
from src.token import Token


class Environment:
    def __init__(self, enclosing=None) -> None:
        self._final = {}
        self.enclosing = enclosing

    def define(self, name: str, value: Any):
        self._final[name] = value

    def get(self, name: Token):
        if name.lexeme in self._final:
            return self._final.get(name.lexeme)
        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise JaqlRuntimeError(name, f"Undefined variable {name.lexeme}.")

    def get_at(self, distance: int, name: str):
        return self.ancestor(distance)._final.get(name)

    def ancestor(self, distance: int):
        environment = self
        for _ in range(distance):
            environment = environment.enclosing
        return environment

    def assign(self, name: Token, value: Any):
        if name.lexeme in self._final:
            self._final[name.lexeme] = value
            return None
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return None
        raise JaqlRuntimeError(name, f"Undefined variable {name.lexeme}.")
    
    def assign_at(self, distance: int, name: Token, value):
        self.ancestor(distance)._final[name.lexeme] = value
