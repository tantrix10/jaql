from typing import Union

from src.token import Token
from src.token_type import FunctionType
from src.types.Expr import (
    Assign,
    Binary,
    Call,
    Expr,
    Grouping,
    Literal,
    Logical,
    Unary,
    Variable,
)
from src.types.Stmt import (
    Block,
    Class,
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    Var,
    While,
)


class Resolver:
    def __init__(self, interpreter, jaql) -> None:
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.jaql = jaql

    def scopes_empty(self):
        return len(self.scopes) == 0

    def resolve(self, statements: list[Stmt]):
        # maybe should be *statements, maybe this is cleaner
        for statement in statements:
            self.resolve_single(statement)

    def resolve_single(self, statement: Union[Stmt, Expr]):
        statement.accept(self)

    def start_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if self.scopes_empty():
            return None
        scope = self.scopes[-1]

        if name.lexeme in scope:
            self.jaql.add_error(name.line, "Already a variable with this")
            return None

        scope[name.lexeme] = False

    def define(self, name: Token):
        if self.scopes_empty():
            return None
        self.scopes[-1][name.lexeme] = True

    def resolve_local(self, expr: Expr, name: Token):
        i = 0
        for scope in reversed(self.scopes):
            if name.lexeme in scope:
                self.interpreter.resolve(expr, i)
                return None
            i += 1

    def resolve_function(self, function: Function, function_type: FunctionType):
        enclosing_function = self.current_function
        self.current_function = function_type
        self.start_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()
        self.current_function = enclosing_function

    def visitFunctionStmt(self, stmt: Function):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolve_function(stmt, FunctionType.FUNCTION)
        return None

    def visitExpressionStmt(self, stmt: Expression):
        self.resolve_single(stmt.expression)
        return None

    def visitIfStmt(self, stmt: If):
        self.resolve_single(stmt.condition)
        self.resolve_single(stmt.then_branch)

        if stmt.else_branch is not None:
            self.resolve_single(stmt.else_branch)
        return None

    def visitPrintStmt(self, stmt: Print):
        self.resolve_single(stmt.expression)
        return None

    def visitReturnStmt(self, stmt: Return):
        if self.current_function == FunctionType.NONE:
            self.jaql.add_error(stmt.keyword.line, "Can't return from top-level code.")
        if stmt.value is not None:
            self.resolve_single(stmt.value)
        return None
    
    def visitClassStmt(self, stmt: Class):
        self.declare(stmt.name)
        self.define(stmt.name)
        return None

    def visitWhileStmt(self, stmt: While):
        self.resolve_single(stmt.condition)
        self.resolve_single(stmt.body)
        return None

    def visitBinaryExpr(self, expr: Binary):
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)
        return None

    def visitCallExpr(self, expr: Call):
        self.resolve_single(expr.callee)
        for argument in expr.arguments:
            self.resolve_single(argument)
        return None

    def visitGroupingExpr(self, expr: Grouping):
        self.resolve_single(expr.expression)

    def visitLiteralExpr(self, expr: Literal):
        return None

    def visitLogicalExpr(self, expr: Logical):
        self.resolve_single(expr.left)
        self.resolve_single(expr.right)
        return None

    def visitUnaryExpr(self, expr: Unary):
        self.resolve_single(expr.right)
        return None

    def visitAssignExpr(self, expr: Assign):
        self.resolve_single(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visitBlockStmt(self, stmt: Block):
        self.start_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def visitVarStmt(self, stmt: Var):
        self.declare(stmt.name)
        if stmt.initialiser is not None:
            self.resolve_single(stmt.initialiser)
        self.define(stmt.name)
        return None

    def visitVariableExpr(self, expr: Variable):
        if (not self.scopes_empty()) and (
            self.scopes[-1].get(expr.name.lexeme) == False
        ):
            self.interpreter.jaql.add_error(
                expr.name, "Can't read local variable in its own initialiser"
            )
        self.resolve_local(expr, expr.name)
        return None
