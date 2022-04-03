#include <string>
#include <vector>
#include <any>

#include "token.h"
#include "token_type.h"

namespace Jaql
{
    class Scanner
    {
        public:
            Scanner(std::string source);
            std::vector<Token> scan_tokens();
        
        private:
        void scan_token();

        std::string source;
        std::vector<Token> tokens;
        bool is_at_end();
        char advance();
        void add_token(TokenType type, std::any literal );
        void add_token(TokenType type);
        bool match(char expected);
        char peek();
        void string();

        int start = 0;
        int current = 0;
        int line = 1;
    };
};