#include <iostream>
#include <fstream>


void run(const std::string code)
{
    // scan
    // parse
    // run
}

void run_file(const std::string file_name)
{
    std::cout << "Readig file" << std::endl;
    std::ifstream file{file_name};
    if (!file.good())
    {
        throw std::exception();
    };

    std::string line;
    std::string code;

    while (std::getline(file, line))
    {
        std::cout << line + '\n';
        code += line + '\n';
    }

    run(code);
    // JAQL error
}

void run_interpreter()
{
    std::cout << "ENTERING JAQL INTERPRETER" << std::endl;
    std::string code;
    bool running = true;
    while (running)
    {
        std::cout << ">> ";

        if (std::getline(std::cin, code)){
            std::cout << code << std::endl;
            run(code);
            // JAQL error
        }
        else {
            std::cout << "exiting jaql";
            running = false;
        }
    }
}

int main(int argc, char **argv)
{
    if (argc > 2)
    {
        std::cout << "Too many input args. ./lox <script location> ";
        std::cout << "or ./lox for interpreter mode" << std::endl;
    }
    else if (argc == 2)
    {
        std::cout << "Running file " << argv[1] << std::endl;
        run_file(argv[1]);
    }
    else
    {
        std::cout << "Entering interpreter." << std::endl;
        run_interpreter();
    };

    return 0;
}
