import logging

from src.exceptions import JaqlException
from src.scanner import Scanner


class Jaql:
    def __init__(self, code: str) -> None:
        self.code: str = code
        self.error: bool = False
        self.runtime_error: bool = False

    def report(self, line: int, where: str, message: str):
        print(f"[[ {line}, char: {where} ]] Error: {message}")
        raise JaqlException

    def add_error(self, line: int, message: str):
        self.error = True
        self.report(line, "", message)
