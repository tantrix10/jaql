#include <iostream>

namespace Jaql{

    class Jaql{
        public:
            static void report(int line, std::string where, std::string message);
            static void error(int line, std::string message);
            static bool Error;
            static bool RuntimeError;
    };
};