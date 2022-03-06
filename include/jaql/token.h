#include <iostream>
#include "token_type.h"

namespace Jaql{
    class Token{
        public:
            Token(TokenType type, std::string lexeme, std::string literal, int line);
            std::string to_string() const;
            TokenType type;
            std::string lexeme;
            std::string literal;
            int line;
    };
};