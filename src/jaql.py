import sys

from src.exceptions import JaqlException, JaqlRuntimeError


class Jaql:
    def __init__(self, code: str) -> None:
        self.code: str = code
        self.error: bool = False
        self.runtime_error: bool = False
        self.max_arugments = 256

    def report(self, line: int, where: str, message: str):
        print(f"[[ {line}, char: {where} ]] Error: {message}")
        # raise JaqlException

    def add_error(self, line: int, message: str):
        self.error = True
        print("ERROR:")
        self.report(line, "", message)
        # raise JaqlException()

    def add_runtime_error(self, error):
        self.runtime_error = True
        print("ERROR:")
        print(error.get_message())
        # raise JaqlException(error.get_message())

    def check_errors(self):
        if self.error:
            sys.exit(65)
        if self.runtime_error:
            sys.exit(70)
