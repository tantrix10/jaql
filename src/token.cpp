#include "token.h"
#include <any>
#include <iostream>

namespace Jaql
{
    Token::Token(TokenType type, std::string lexeme, int line): 
        Token(type, lexeme, std::any{}, line)
    {};

    Token::Token(TokenType type, std::string lexeme, std::any literal, int line):
        type(type),
        lexeme(std::move(lexeme)),
        literal(literal),
        line(line)
    {};

    std::string Token::to_string() const
    {
        std::string output = "Type: " + std::to_string(static_cast<int>(type)) + ", Lexeme: " + lexeme ;
        if (type == TokenType::STRING or type == TokenType::NUMBER){
             output+= ", Literal: "; 
             output  += literal_to_string() ;
        }
        return output;
    };
    std::string Token::literal_to_string() const
    {
        switch (type) {
        case TokenType::STRING:
            return std::any_cast<std::string>(literal);
        case TokenType::NUMBER:
            return std::to_string(std::any_cast<double>(literal));
        default:
            return "";
        }
    }
};