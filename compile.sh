g++-11 ./src/codegen/generate_ast.cpp -o codegen
&&
./codegen
&&
g++-11 ./src/main.cpp ./src/scanner.cpp ./src/token.cpp ./src/jaql.cpp   -I./include/jaql -o jaql