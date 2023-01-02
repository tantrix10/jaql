from typing import Any

from src.environment import Environment
from src.exceptions import JaqlRuntimeError, ReturnException
from src.token import Token


class LoxCallable:
    def call(self, interpreter, arguments: list[Any]):
        pass

    def arity(self) -> int:
        return 0


class JaqlFunction(LoxCallable):
    def __init__(self, declaration, closure) -> None:
        self.declaration = declaration
        self.closure = closure

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as e:
            return e.value
        return None

    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"


class JaqlClass(LoxCallable):
    def __init__(self, name) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def call(self, interpreter, arguments):
        instance = JaqlInstance(self)
        return instance

    def arity(self) -> int:
        return 0


class JaqlInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        raise JaqlRuntimeError(name, f"Undefined property {name.lexeme}.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return self.klass.name + " instance"
