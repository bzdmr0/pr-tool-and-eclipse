#include <stdio.h>

int main() {
    printf("Hello World!\n");

#ifdef COMPILED_BY_PYTHON
    printf("This was compiled by Python script!\n");
#else
    printf("This was compiled by Eclipse or manual gcc\n");
#endif

    return 0;
}

//asd123
