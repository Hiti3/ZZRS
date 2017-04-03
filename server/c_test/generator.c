#include <stdio.h>

/**
 * generira datoteko z nakljucnimi stevili
 * ./generator <ime_datoteke> <stevilo_int_stevil>
*/

int main(int argc, char **argv) {
    
    if(argc == 3) {
        FILE *f = fopen(argv[1], "w");
        int i, iMax = atoi(argv[2]);
        fprintf(f, "%d\n", iMax);
        for(i = 0; i < iMax; i++) {
            fprintf(f, "%d\n", rand());
        }
    }
    
    return 0;
}