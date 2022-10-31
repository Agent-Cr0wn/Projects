#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    typedef uint8_t BYTE;
    BYTE buffer [512];
    int bytes_read, count = 0;
    char filename[8];

    // Open memory card
    FILE *f = fopen(argv[1], "r");
    FILE *img = NULL;

    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }

    if (f == NULL)
    {
        printf("./recover card.raw");
        return 1;
    }

    // Repeat until the end of the card
    while (true)
    {
        // Read 512 bytes into a buffer
        bytes_read = fread(buffer, sizeof(BYTE), 512, f);
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && ((buffer[3] & 0xf0) == 0xe0))
        {
            // If first JPEG then create file and write
            if (count == 0)
            {
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), bytes_read, img);
                count++;
            }
            // Else close the file and open a new file to write to
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, sizeof(BYTE), bytes_read, img);
                count++;
            }
        }
        //Else if already found JPEG, keep writing to it
        else if (count != 0)
        {
            fwrite(buffer, sizeof(BYTE), bytes_read, img);
            if (bytes_read == 0)
            {
                fclose(img);
                fclose(f);
                return 0;
            }
        }
    }
    fclose(img);
    fclose(f);
}