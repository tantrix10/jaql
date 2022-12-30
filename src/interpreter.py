from numbers import Number
from typing import Any, Optional

from src.callable import JaqlFunction, LoxCallable
from src.environment import Environment
from src.exceptions import JaqlRuntimeError, ReturnException
from src.natives import Clock
from src.token import Token
from src.token_type import TokenType
from src.types import Stmt
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
    Expression,
    Function,
    If,
    Print,
    Return,
    Stmt,
    Var,
    While,
)


class Interpreter:

    globals = Environment()
    globals.define("clock", Clock())
    locals: dict[Expr, int] = {}

    def __init__(self, jaql):
        self.jaql = jaql

        self.environment = self.globals

    def interpret(self, statements: list[Stmt]):
        try:
            for statement in statements:
                self.execute(statement)
        except JaqlRuntimeError as e:
            self.jaql.add_runtime_error(e)

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def stringify(self, value):
        if value is None:
            return "nill"
        if isinstance(value, Number):
            text = str(value)  # type: ignore
            if text.endswith(".0"):
                text = text[0:-2]
            return text
        return str(value)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def resolve(self, expr: Expr, depth: int):
        self.locals[expr] = depth

    def is_truthy(self, obj: Any):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, left, right):
        # TODO: the idea of equality should be tightened here
        if (left is None) and (right is None):
            return True
        if left is None:
            return False
        if right is None:
            return False
        return left == right or left is right

    def check_number_operands(self, operator: Token, left: Any, right: Any):
        if isinstance(left, Number) and isinstance(right, Number):
            return True
        raise JaqlRuntimeError(
            operator,
            f"Operand {left} and {right} for operator {operator} must be a number.",
        )

    def check_number_operand(self, operator: Token, operand: Any):
        if isinstance(operand, Number):
            return True
        raise JaqlRuntimeError(
            operator, f"Operand {operand} for operator {operator} must be a number."
        )

    def execute_block(self, statements: list[Stmt], environment: Environment):
        previous = self.environment
        self.environment = environment

        try:
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def look_up_variable(self, name: Token, expr: Expr):
        distance = self.locals.get(expr)

        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        else:
            return self.globals.get(name)

    def visitFunctionStmt(self, stmt: Function):
        function = JaqlFunction(declaration=stmt, closure=self.environment)
        self.environment.define(stmt.name.lexeme, function)
        return None

    def visitIfStmt(self, stmt: If):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visitExpressionStmt(self, stmt: Expression):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt: Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt: Var):
        value = None
        if stmt.initialiser is not None:
            value = self.evaluate(stmt.initialiser)
        self.environment.define(name=stmt.name.lexeme, value=value)
        return None

    def visitReturnStmt(self, stmt: Return):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)

    def visitBlockStmt(self, stmt: Block):
        self.execute_block(stmt.statements, Environment(enclosing=self.environment))
        return None

    def visitWhileStmt(self, stmt: While):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None

    def visitAssignExpr(self, expr: Assign):
        value = self.evaluate(expr.value)

        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value

    def visitVariableExpr(self, expr: Variable):
        return self.look_up_variable(expr.name, expr)

    def visitLiteralExpr(self, expr: Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Grouping):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Unary):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right  # type: ignore
            case TokenType.BANG:
                return not self.is_truthy(right)

        return None

    def visitLogicalExpr(self, expr: Logical):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        elif not self.is_truthy(left):
            return left

        return self.evaluate(expr.right)

    def visitBinaryExpr(self, expr: Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right  # type: ignore
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return left / right  # type: ignore
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return left * right  # type: ignore
            case TokenType.PLUS:
                if isinstance(left, Number) and isinstance(right, Number):
                    return left + right

                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                self.jaql.add_runtime_error(
                    JaqlRuntimeError(
                        expr.operator,
                        f"{left} and {right} must be two number or two strings.",
                    )
                )
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left, right)
                return left > right  # type: ignore
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left >= right  # type: ignore
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return left < right  # type: ignore
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return left <= right  # type: ignore
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)

        return None

    def visitCallExpr(self, expr: Call):
        callee: LoxCallable = self.evaluate(expr.callee)  # type: ignore

        arguments = []

        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))

        if not isinstance(callee, LoxCallable):
            raise JaqlRuntimeError(expr.paren, f"Cannot call {callee}")

        if len(arguments) != callee.arity():
            raise JaqlRuntimeError(
                expr.paren, f"Expected {callee.arity()} arguments, got {len(arguments)}"
            )

        return callee.call(self, arguments)
