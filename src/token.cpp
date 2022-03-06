#include "token.h"

namespace Jaql
{
    Token::Token(TokenType type, std::string lexeme, std::string literal, int line) : Token(type, lexeme, literal, line){};

    std::string Token::to_string() const
    {
        return "Type: " + std::to_string(static_cast<int>(type)) + ", Lexeme: " + lexeme + ", Literal: " + literal;
    };
};