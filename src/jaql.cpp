#include "../jaql/jaql.h"

namespace Jaql
{
    bool Jaql::Error = false;
    bool Jaql::RuntimeError = false;

    void Jaql::report(int line, std::string where, std::string message)
    {
        // [[line: 254, char: 3454]] Error: message
        std::cout << "[[ " << line << ", char: " << where << " ]] Error: " << message << std::endl;
        throw std::exception();
    }

    void Jaql::error(int line, std::string message)
    {
        Error = true;
        report(line, "", message);
    }
};