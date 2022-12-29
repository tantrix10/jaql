from typing import Any
from src.exceptions import JaqlRuntimeError
from src.jaql import Jaql
from src.token import Token

class Environment:
    def __init__(self, jaql: Jaql) -> None:
        self._final = {}
        self.jaql = jaql
    
    def define(self, name: str, value: Any):
        # clearly not strictly needed, but making final private
        # gives flexibility on this implementation
        self._final[name] = value
    
    def get(self, name: Token):
        if value := self._final.get(name.lexeme):
            return value
        self.jaql.add_runtime_error(JaqlRuntimeError(name, f"Undefined variable {name.lexeme}."))
        