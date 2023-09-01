from typing import Union

from src.token import Token
from src.token_type import TokenType
from src.types.Expr import Binary, Expr, Grouping, Literal, Unary


class ASTPrinter:
    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthesize(
            expr.operator.lexeme,
            [
                expr.left,
                expr.right,
            ],
        )

    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthesize(
            "group",
            [
                expr.expression,
            ],
        )

    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnaryExpr(self, expr: Unary):
        return self.parenthesize(
            expr.operator.lexeme,
            [
                expr.right,
            ],
        )

    def parenthesize(self, name: str, exprs: list[Expr]):
        """
        TODO: implement single and list
        """
        builder = []

        builder.append("(")
        builder.append(name)
        for expr in exprs:
            builder.append(" ")
            builder.append(expr.accept(self))
        builder.append(")")

        return "".join(builder)


def main():
    expression = Binary(
        Unary(Token(TokenType.MINUS, "-", 1, 1), Literal(123)),
        Token(TokenType.STAR, "*", 1, 1),
        Grouping(Literal(45.67)),
    )

    print(ASTPrinter().print(expression))


if __name__ == "__main__":
    main()
