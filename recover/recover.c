#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    typedef uint8_t BYTE;
    BYTE buffer [512];
    int bytes_read, counter = 0;
    char filename[8];
    // Open memory card
    FILE *f = fopen(argv[1], "r");
    // Repeat until the end of the card
    while(true)
    {
    // Read 512 bytes into a buffer
        bytes_read = fread(buffer, sizeof(BYTE), 512, f);
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
    // If first JPEG then create file and write
            if(counter == 0)
            {

                sprintf(filename, "%03i.jpg", 2, count);
            }
        }
    }








}