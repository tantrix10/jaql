from time import time

from src.interpreter import LoxCallable


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        return time()

    def __str__(self) -> str:
        return "<native fn [[clock]]>"
