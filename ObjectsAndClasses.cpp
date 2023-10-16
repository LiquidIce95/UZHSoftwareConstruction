#include <iostream>

template<typename... Args>
void test(Args... args) {
    ((std::cout << args << " some blabla "), ...);
}


int foo(int x, int y) {
    return x + y;
}


int main() {
    test(1, 2, 3, 4);

    int (*fun)(int, int);  // Declare a function pointer
    fun = foo;  // Assign function to pointer
    int result = fun(2, 3);  // Invoke function through pointer
    
    return 0;
}
