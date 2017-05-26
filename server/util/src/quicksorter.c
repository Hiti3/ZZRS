#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/**
 * quicksort algoritem
 * ./quicksorter <vhodna_datoteka> <izhodna_datoteka>
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

void quicksorter(int *a, int len) {
    if (len < 2) return;
    
    int pivot = a[len / 2];
    
    int i, j;
    for (i = 0, j = len - 1; ; i++, j--) {
        while (a[i] < pivot) i++;
        while (a[j] > pivot) j--;
        
        if (i >= j) break;
        
        int temp = a[i];
        a[i] = a[j];
        a[j] = temp;
    }
    quicksorter(a, i);
    quicksorter(a + i, len - i);
}

int main(int argc, char **argv) {
    
    if(argc == 3) {
        data *d = readFile(argv[1]);
        quicksorter(d->array, d->length);
        writeFile(argv[2], d);
    }
    
    return 0;
}