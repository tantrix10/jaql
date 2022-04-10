#include <iostream>
#include <any>
#include "token_type.h"

namespace Jaql{
    class Token{
        public:
            Token(TokenType type, std::string lexeme, int line);

            Token(TokenType type, std::string lexeme, std::any literal, int line);

            std::string to_string() const;
            TokenType type;
            std::string lexeme;
            std::string literal_to_string() const;
            std::any literal;
            int line;
        
    };
};