from typing import Union
from src.token import Token
from src.types.Expr import Expr, Variable
from src.types.Stmt import Block, Stmt, Var


class Resolver:
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter
        self.scopes = []
    
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

        scope[name.lexeme] = False
    
    def define(self, name: Token):
        if self.scopes_empty():
            return None
        self.scopes[-1][name.lexeme] = True
    
    def resolve_local(self, expr: Expr, name: Token):
        for i in range(len(self.scopes)-1, 0, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes)-1-i)
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
        if not self.scopes_empty() and not self.scopes[-1].get(expr.name.lexeme):
            self.interpreter.jaql.add_error(expr.name, "Can't read local variable in its own intialiser")
        self.resolve_local(expr, expr.name)
        return None
    
        