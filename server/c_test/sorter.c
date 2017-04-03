#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/**
 * preprost sort algoritem
 * ./sorter <vhodna_datoteka> <izhodna_datoteka>
*/

typedef struct data {
    int length, *array;
} data;

data* readFile(char *path) {
    FILE *f = fopen(path, "r");
    data *d = malloc(sizeof(data));
    fscanf(f, "%d", &(d->length));
    d->array = malloc(sizeof(int)*(d->length));
    int tmp, i = 0;
    while(fscanf(f, "%d", &(d->array[i])) != EOF && i < d->length) {
        i++;
    }
    fclose(f);
    return d;
}

void print(data *d) {
    int i;
    for(i = 0; i < d->length; i++) {
        printf("%d\n", d->array[i]);
    }
}

void writeFile(char *path, data *d) {
    FILE *f = fopen(path, "w");
    fprintf(f, "%d\n", d->length);
    int i;
    for(i = 0; i < d->length; i++) {
        fprintf(f, "%d\n", d->array[i]);
    }
    fclose(f);
}

void sorter(data *d) {
    int i, j, tmp;
    for(i = 0; i < d->length; i++) {
        for(j = 0; j < d->length; j++) {
            if(d->array[i] < d->array[j]) {
                tmp = d->array[i];
                d->array[i] = d->array[j];
                d->array[j] = tmp;
            }
        }
    }
}

int main(int argc, char **argv) {
    
    if(argc == 3) {
        data *d = readFile(argv[1]);
        sorter(d);
        writeFile(argv[2], d);
    }
    
    return 0;
}