#include "scanner.h"
#include "token_type.h"
#include "jaql.h"

#include <any>
#include <cctype>

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
                ++line;
                break;
            
            case '"': string(); break;

            default:
                if (std::isdigit(c))
                {
                    number();
                } else if (std::isalpha(c) || c == '_'){
                    identifier();
                }
                else{
                    Jaql::error(line, "Unexpected character.");
                    break;
                }
        }
    }

    void Scanner::identifier()
    {
        while ( std::isdigit(peek()) || std::isalpha(peek()) || peek() == '_' )
        {
            advance();
        }
        std::string ident = source.substr(start, current-start);
        
    }

    void Scanner::number()
    {
        while (std::isdigit(peek())) advance();

        if (peek() == '.' && std::isdigit(peek_next())){
            advance();

            while (std::isdigit(peek())) advance;
        }
        add_token(TokenType::NUMBER, std::stod(source.substr(start, current-start)) );
    }

    char Scanner::peek_next(){
        if (current + 1 >= source.length()) return '\0';
        return source.at(current+1);
    }

    void Scanner::string()
    {
        while (peek() != '"' && !is_at_end()) {
        if (peek() == '\n') ++line;
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