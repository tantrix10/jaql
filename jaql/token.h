#include <iostream>
#include "./jaql/token_type.h"

namespace Jaql{
    class Token{
        Token(TokenType type, std::string lexeme);
    };
};