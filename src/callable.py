from typing import Any, Optional

from src.environment import Environment
from src.exceptions import JaqlRuntimeError, ReturnException
from src.token import Token


class LoxCallable:
    def call(self, interpreter, arguments: list[Any]):
        pass

    def arity(self) -> int:
        return 0


class JaqlInstance:
    def __init__(self, klass) -> None:
        self.klass = klass
        self.fields = {}

    def get(self, name: Token):
        if name.lexeme in self.fields:
            return self.fields.get(name.lexeme)

        method: JaqlFunction = self.klass.find_method(name.lexeme)

        if method is not None:
            return method.bind(self)

        raise JaqlRuntimeError(name, f"Undefined property {name.lexeme}.")

    def set(self, name: Token, value: Any):
        self.fields[name.lexeme] = value

    def __str__(self) -> str:
        return self.klass.name + " instance"


class JaqlFunction(LoxCallable):
    def __init__(self, declaration, closure, is_initialiser) -> None:
        self.declaration = declaration
        self.closure = closure
        self.is_initialiser: bool = is_initialiser

    def arity(self) -> int:
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnException as e:
            if self.is_initialiser:
                return self.closure.get_at(0, "this")
            return e.value
        
        if self.is_initialiser:
            return self.closure.get_at(0, "this")
        return None
    
    def bind(self, instance: JaqlInstance):
        environment: Environment = Environment(self.closure)
        environment.define("this", instance)
        return JaqlFunction(self.declaration, environment, self.is_initialiser)


    def __str__(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"


class JaqlClass(LoxCallable):
    def __init__(self, name, methods) -> None:
        self.name = name
        self.methods = methods

    def __str__(self) -> str:
        return self.name

    def call(self, interpreter, arguments):
        instance = JaqlInstance(self)
        initialiser: Optional[JaqlFunction] = self.find_method("init")
        if initialiser is not None:
            initialiser.bind(instance).call(interpreter, arguments)
        return instance

    def arity(self) -> int:
        initialiser = self.find_method("init")
        if initialiser is None:
            return 0
        return initialiser.arity()

    def find_method(self, name: str):
        if name in self.methods:
            return self.methods.get(name)
        return None



