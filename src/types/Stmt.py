# Filegen-ed, do not modify in place
from abc import ABC, abstractmethod
from typing import Any, Optional

from src.token import Token
from src.types.Expr import Expr


class Stmt(ABC):
    pass

    @abstractmethod
    def accept(self, visitor):
        pass


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)


class Expression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)


class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)


class Class(Stmt):
    def __init__(self, name: Token, methods: list[Function]):
        self.name = name
        self.methods = methods

    def accept(self, visitor):
        return visitor.visitClassStmt(self)


class If(Stmt):
    def __init__(self, condition: Expr, then_branch: Stmt, else_branch: Optional[Stmt]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)


class Return(Stmt):
    def __init__(self, keyword: Token, value: Optional[Expr]):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)


class Var(Stmt):
    def __init__(self, name: Token, initialiser: Expr):
        self.name = name
        self.initialiser = initialiser

    def accept(self, visitor):
        return visitor.visitVarStmt(self)


class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
