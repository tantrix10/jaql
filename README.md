# jaql
JAQL - Just Another Quantum Language. A Lox implementation attempting to be quantum, eventually. 

## Setup and run

    1. Install: poetry install
    2. Run: poetry run python -m src.main <file_path>
       1. No file_path runs the interpreters

## TODOS:

    1. My error reporting implementation kind of sucks, need to overhaul + fix. Should only be raising errors and catching where appropriate, that prevents this bad passing round of a Jaql obj.
    2. Line counting is wrong
    3. floats are broken if a class or function is defined in file: Expect property name after '.'.
    4. bool == isn't correct, we use python ==, so e.g. True == 1 -> True
    5. Implement [test suite](https://github.com/munificent/craftinginterpreters/tree/master/test)
    6. There's a bunch of my own file path specific stuff scattered around...