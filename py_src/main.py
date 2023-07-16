import sys
from os.path import isfile

from src.interpreter import Interpreter
from src.jaql import Jaql
from src.parser import Parser
from src.resolver import Resolver
from src.scanner import Scanner


def run(code: str):
    jaql = Jaql(code)

    scanner = Scanner(source=code, jaql=jaql, debug=False)
    tokens = scanner.scan_tokens()
    jaql.check_errors()

    parser = Parser(tokens, jaql=jaql, debug=True)
    statements = parser.parse()
    jaql.check_errors()

    interpreter = Interpreter(jaql=jaql)
    resolver = Resolver(interpreter=interpreter, jaql=jaql)

    resolver.resolve(statements=statements)
    jaql.check_errors()

    interpreter.interpret(statements)  # type: ignore
    jaql.check_errors()


def run_file(file_name: str):
    print(f"Reading file: [[{file_name}]]")
    if isfile(file_name):
        code = ""
        with open(file=file_name) as file:
            for line in file:
                # print(line)
                code += line + "\n"
            run(code)
    else:
        raise FileNotFoundError(f"Cannot find file: {file_name}")


def run_interpreter():
    print("ENTERING JAQL INTERPRETER")
    code = ""
    running = True

    while running:
        print(">> ")
        if code := input():
            run(code)
        else:
            print("Exiting jaql")
            running = False


def main():
    if (args_count := len(sys.argv)) > 2:
        print(
            "Too many input args. ./lox <script location> or ./lox for interpreter mode"
        )
        raise SystemExit(2)
    elif args_count == 2:
        run_file(sys.argv[1])
    else:
        run_interpreter()

    return 0


if __name__ == "__main__":
    main()
