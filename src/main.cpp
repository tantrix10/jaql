#include <iostream>

int main(int argc, char** argv){
    if (argc > 2){
        std::cout << "Too many input args. ./lox <script location> ";
        std::cout << "or ./lox for interpreter mode"<<std::endl;
    }
    else if(argc == 2){
        std::cout << "Running file " << argv[1] <<std::endl;
    }
    else {
        std::cout << "Entering interpreter."<<std::endl;
    };

    return 0;

}
