#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>


//#define DEBUG

#ifdef DEBUG
#define dbg(...) fprintf(stderr, __VA_ARGS__)
#else
#define dbg(...)
#endif

#define FLAG_LEN 40
#define N_PTR 2

char *ptrs[N_PTR];
char flag = 0;

void readn(char *buf, unsigned size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned x = read(0, buf + i, 1);
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n') buf[cnt - 1] = '\x00';
}

unsigned get_num()
{
    char buf[0x20] = {0};
    readn(buf, 0x19);
    unsigned c = atoi(buf);
    return c;
}

unsigned get_index() {
    unsigned idx = get_num();
    if (idx >= N_PTR) {
        puts("invalid index");
        exit(-1);
    }
    return idx;
}

void menu() {
    puts("---------------");
    puts("0: alloc");
    puts("1: dealloc");
    puts("2: read");
    puts("---------------");
    printf("> ");
}


void allocate() {
    printf("index > ");
    unsigned idx = get_index();
    printf("size > ");
    unsigned n = get_num();
    if (n >= 0x100) {
        puts("too big");
        return;
    }
    ptrs[idx] = calloc(1, n);
    printf("data > ");
    readn(ptrs[idx], n);
}

void deallocate() {
    printf("index > ");
    unsigned idx = get_index();
    if (ptrs[idx] == NULL) {
        return;
    }
    free(ptrs[idx]);
    ptrs[idx] = NULL;
}

void read_flag() {
    printf("index > ");
    unsigned idx = get_index();
    if (ptrs[idx] == NULL) {
        puts("create a buffer");
        return;
    }
    if (flag == 0) {
        puts("you have already read it");
        return;
    }
    printf("at > ");
    unsigned index = get_num();
    ptrs[idx][index] = flag;
    flag = 0;
}

void sanity_check(char *buf) {
    if (strlen(buf) != FLAG_LEN) {
        exit(-1);
    }
    if (strncmp(buf, "TSGCTF{", 7) != 0) {
        exit(-1);
    }
    if (buf[FLAG_LEN - 1] != '}') {
        exit(-1);
    }
    for (int i = 7; i < FLAG_LEN - 1; i++) {
        if (('a' <= buf[i] && buf[i] <= 'f') ||
                ('0' <= buf[i] && buf[i] <= '9')) {
            continue;
        }
        exit(-1);
    }
}

void setup() {
    alarm(5);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    printf("index > ");
    unsigned num = get_num();
    if (num >= FLAG_LEN) {
        puts("invalid");
        exit(-1);
    }

    char buf[FLAG_LEN + 1] = {0};
    int fd = open("flag", O_RDONLY);
    if (fd == -1) exit(-1);
    read(fd, buf, FLAG_LEN);
    close(fd);

    sanity_check(buf);
    flag = buf[num];
}

int main(void) {
    setup();
    while(1) {
        menu();
        int n = get_num();
        switch (n) {
            case 0:
                allocate();
                break;
            case 1:
                deallocate();
                break;
            case 2:
                read_flag();
                break;
            default:
                return 0;
        }
    }
    return 0;
}
