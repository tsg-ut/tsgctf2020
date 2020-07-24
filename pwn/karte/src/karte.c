#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define N_ENT 32
#define MIN_SIZE 0x50
#define MAX_SIZE 0xa0

//#define DEBUG

#ifdef DEBUG
#define dbg(...) fprintf(stderr, __VA_ARGS__)
#else
#define dbg(...)
#endif

typedef struct {
    unsigned long long size;
    unsigned long long id;
    unsigned long long data[];
}__attribute__((__packed__)) Vec;

Vec *vecs[N_ENT] = {0};

typedef unsigned long long idt;

idt get_num()
{
    idt c;
    if (scanf("%llu", &c) != 1)
        exit(-1);
    return c;
}

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

unsigned search_index(idt id) {
    for (unsigned i = 0; i < N_ENT; i++) {
        if (vecs[i] != NULL && vecs[i]->id == id) {
            return i;
        }
    }
    puts("no such ent");
    exit(-1);
}

idt get_empty() {
    for (unsigned i = 0; i < N_ENT; i++) {
        if (vecs[i] == NULL) {
            return i;
        }
    }
    puts("no such ent");
    exit(-1);
}

unsigned long long  get_id() {
    unsigned long long id = get_num();
    return id;
}

unsigned get_index() {
    idt id = get_num();
    return search_index(id);
}

unsigned get_size() {
    unsigned size = get_num();
    if (size < MIN_SIZE || size > MAX_SIZE) {
        puts("invalid size\n");
        exit(-1);
    }
    return size;
}


void allocate() {
    printf("id > ");
    idt id = get_id();
    printf("size > ");
    unsigned size = get_size();
    unsigned num = get_empty();
    vecs[num] = realloc(vecs[num], size);
    vecs[num]->size = size;
    vecs[num]->id = id;
}

void extend() {
    printf("id > ");
    unsigned num = get_index();
    printf("size > ");
    unsigned size = get_size();
    if (vecs[num]->size > size) {
        puts("You cannot shrink any buffer\n");
        return;
    }
    vecs[num] = realloc(vecs[num], size);
    vecs[num]->size = size;
}

void change_id() {
    printf("id > ");
    unsigned num = get_index();
    if (vecs[num]->size == 0) {
        puts("no such ent");
        return;
    }

    printf("new id > ");
    idt new_id = get_id();
    vecs[num]->id = new_id;
}


void show() {
    printf("id > ");
    unsigned num = get_index();
    printf("id: %llx size: %llx\n", vecs[num]->id, vecs[num]->size);
}

void deallocate() {
    printf("id > ");
    unsigned num = get_index();
    realloc(vecs[num], 0);
}

void menu() {
    puts("---------------");
    puts("0: alloc");
    puts("1: extend");
    puts("2: change id");
    puts("3: show");
    puts("4: dealloc");
    puts("---------------");
    printf("> ");
}

void setup() { // TODO:setvbuf
   alarm(60);
   setvbuf(stdout, NULL, _IONBF, 0);
   setvbuf(stdin, NULL, _IONBF, 0);
   setvbuf(stderr, NULL, _IONBF, 0);
}

char name[0x20] = {0};
int authorized = 0;

int main(void) {
    setup();
    printf("What's your name > ");
    readn(name, 0x1f);
    printf("Hello: %s\n", name);
    while (1) {
        menu();
        switch (get_num()) {
            case 0:
                allocate();
                break;
            case 1:
                extend();
                break;
            case 2:
                change_id();
                break;
            case 3:
                show();
                break;
            case 4:
                deallocate();
                break;
            case 5:
                if(authorized) system("/bin/sh");
            default:
                printf("no such command");
                exit(-1);
        }
    }
    return 0;
}

