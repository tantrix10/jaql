from src.token import Token


class JaqlException(Exception):
    pass


class JaqlParseException(Exception):
    pass


class JaqlRuntimeError(Exception):
    def __init__(self, operator: Token, message: str):
        self.operator = operator
        self.message = message

    def get_message(self):
        return f"{self.message} on line: [{self.operator.line}]"

    pass


class ReturnException(JaqlException):
    def __init__(self, value) -> None:
        self.value = value
