from numbers import Number
from typing import Any
from src.environment import Environment

from src.exceptions import JaqlRuntimeError
from src.token import Token
from src.token_type import TokenType
from src.types import Stmt
from src.types.Expr import Binary, Expr, Grouping, Literal, Unary, Variable
from src.types.Stmt import Expression, Print, Stmt, Var


class Interpreter:
    def __init__(self, jaql):
        self.jaql = jaql
        self.environment = Environment(jaql)

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
            text = str(value)
            if text.endswith(".0"):
                text = text[0:-2]
            return text
        return str(value)

    def evaluate(self, expr: Expr):
        return expr.accept(self)

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

    def visitVariableExpr(self, expr: Variable):
        return self.environment.get(expr.name)

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
