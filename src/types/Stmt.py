# Filegen-ed, do not modify in place
from abc import ABC, abstractmethod
from typing import Any

from src.token import Token
from src.types.Expr import Expr


class Stmt(ABC):
    pass

    @abstractmethod
    def accept(self, visitor):
        pass


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initialiser: Expr):
        self.name = name
        self.initialiser = initialiser

    def accept(self, visitor):
        return visitor.visitVarStmt(self)
