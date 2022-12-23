class JaqlException(Exception):
    pass


class JaqlParseException(Exception):
    pass


class JaqlRuntimeError(Exception):
    def __init__(self, operator, message):
        self.operator = operator
        self.message = message
    
    def get_message(self):
        return f"{self.message} on line: [{self.operator.line}]"
    pass
