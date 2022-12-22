import sys
from io import TextIOWrapper
from pathlib import Path

from src.exceptions import JaqlException


def define_type(
    writer: TextIOWrapper, base_name: str, class_name: str, field_list: str
):
    writer.write(f"class {class_name}({base_name}):\n")
    writer.write(f"    def __init__(self, {field_list}):\n")
    for field in field_list.split(","):
        print(field, field_list)
        name = field.split(":")[0]
        writer.write(f"        self.{name} = {name}\n")
    writer.write("\n")
    writer.write(f"    def accept(self, visitor):\n")
    writer.write(f"        return visitor.visit{class_name}{base_name}(self)\n")
    writer.write("\n \n")


def define_ast(output_dir: str, base_name: str, types: list[str]):
    file_path = Path(output_dir) / f"{base_name}.py"

    with open(file_path, "w") as file:
        file.write("# Filegen-ed, do not modify in place\n")
        file.write("from abc import ABC, abstractmethod\n")
        file.write("from typing import Any\n")
        file.write("from src.token import Token\n")
        file.write("\n \n")
        file.write(f"class {base_name}(ABC):\n")
        file.write("    pass\n")
        file.write("    @abstractmethod\n")
        file.write("    def accept(self, visitor):\n")
        file.write("        pass\n")
        file.write("\n \n")
        for type in types:
            class_name = type.split("::")[0].strip()
            fields = type.split("::")[1].strip()
            define_type(file, base_name, class_name, fields)


def main():
    if len(sys.argv) != 2:
        raise JaqlException("Usage: generate_ast <output_dir>")

    output_dir = sys.argv[1]

    define_ast(
        output_dir,
        "Expr",
        [
            "Binary   :: left: Expr, operator: Token, right: Expr",
            "Grouping :: expression: Expr",
            "Literal  :: value: Any",
            "Unary    :: operator: Token, right: Expr",
        ],
    )


if __name__ == "__main__":
    main()
