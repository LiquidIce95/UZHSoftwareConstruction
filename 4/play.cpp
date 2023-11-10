#include <iostream>

int c = 4;

int foo(){
    int a = c;
    return a;
}

int feee(){
    int (*fa)();

    fa=foo;

    return fa();

}

int main(){

    std::cout<<feee()<<std::endl;
    return 0;
}