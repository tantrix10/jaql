#include "scanner.h"
#include "token_type.h"
#include "jaql.h"

#include <any>

namespace Jaql
{
    Scanner::Scanner(std::string source)
    {
        
    }


    std::vector<Token> Scanner::scan_tokens()
    {
        while (!is_at_end()){
            start = current;
            scan_token();
        }
        tokens.emplace_back(TokenType::EOJF, "", line);
    }

    bool Scanner::is_at_end()
    {
        return current >= static_cast<int>(source.size());
    }
    
    void Scanner::scan_token()
    {
        char c = advance();
        switch (c){
            case '(': add_token(TokenType::LEFT_PAREN);
            case ')': add_token(TokenType::RIGHT_PAREN); break;
            case '{': add_token(TokenType::LEFT_BRACE); break;
            case '}': add_token(TokenType::RIGHT_BRACE); break;
            case ',': add_token(TokenType::COMMA); break;
            case '.': add_token(TokenType::DOT); break;
            case '-': add_token(TokenType::MINUS); break;
            case '+': add_token(TokenType::PLUS); break;
            case ';': add_token(TokenType::SEMICOLON); break;
            case '*': add_token(TokenType::STAR); break; 
            case '!':
                add_token(match('=') ? TokenType::BANG_EQUAL : TokenType::BANG);
                break;
            case '=':
                add_token(match('=') ? TokenType::EQUAL_EQUAL : TokenType::EQUAL);
                break;
            case '<':
                add_token(match('=') ? TokenType::LESS_EQUAL : TokenType::LESS);
                break;
            case '>':
                add_token(match('=') ? TokenType::GREATER_EQUAL : TokenType::GREATER);
                break;
            case '/':
                if (match('/')){
                    while (peek() != '\n' && !is_at_end()) advance();
                } else{
                    add_token(TokenType::SLASH);
                }

            case ' ':
            case '\r':
            case '\t':
                // Ignore whitespace.
                break;

            case '\n':
                line++;
                break;
            
            case '"': string(); break;

            default:
                Jaql::error(line, "Unexpected character.");
                break;
        }
    }

    void Scanner::string()
    {
        while (peek() != '"' && !is_at_end()) {
        if (peek() == '\n') line++;
        advance();
    }

    if (is_at_end()) {
      Jaql::error(line, "Unterminated string.");
      return;
    }

    // The closing ".
    advance();

    // Trim the surrounding quotes.
    std::string value = source.substr(start + 1, current - 1);
    add_token(TokenType::STRING, value);
    }

    char Scanner::peek()
    {
        if (is_at_end()) return '\0';
        return source.at(current);
    }

    bool Scanner::match(char expected)
    {
        if (is_at_end()) return false;
        if (source.at(current) != expected ) return false;
        ++current;
        return true;
    }

    char Scanner::advance()
    {
        ++current;
        return source.at(current-1);
    }

    void Scanner::add_token(TokenType type)
    {
        add_token(type, NULL);
    }

    void Scanner::add_token(TokenType type, std::any literal)
    {
        tokens.emplace_back(type, source.substr(start, current-start), literal, line);
    }
};