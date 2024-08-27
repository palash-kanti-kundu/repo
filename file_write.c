#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *file = fopen("largefile.bin", "wb");
    if (!file) {
        perror("Failed to open file");
        return 1;
    }

    // Allocate 10 GB of memory
    size_t size = 10L * 1024 * 1024 * 1024;
    char *buffer = (char *)malloc(size);
    if (!buffer) {
        perror("Failed to allocate memory");
        fclose(file);
        return 1;
    }

    // Write the buffer to the file
    size_t written = fwrite(buffer, 1, size, file);
    if (written != size) {
        perror("Failed to write data");
    }

    // Clean up
    free(buffer);
    fclose(file);

    return 0;
}
