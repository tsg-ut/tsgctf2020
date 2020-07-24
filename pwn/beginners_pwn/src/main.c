#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>


#define SIZE 24

/*
__attribute__((constructor))
void initialize() {
    //setvbuf(stdin, NULL, _IONBF, 0);
	//setvbuf(stdout, NULL, _IONBF, 0);
    alarm(60);
}
*/

void readn(char *buf, int size) {
    unsigned cnt = 0;
    for (unsigned i = 0; i < size; i++) {
        unsigned long long x = 1;
         asm(
        "movq $1, %%rdx\n"
        "movq %1, %%rsi\n"
        "movq $0, %%rdi\n"
        "movq $0, %%rax\n"
        "syscall\n"
        "movq %%rax, %0\n"
        : "=r"(x)
        : "r"(buf+i)
        : "memory");
        cnt += x;
        if (x != 1 || buf[cnt - 1] == '\n') break;
    }
    if (cnt == 0) exit(-1);
    if (buf[cnt - 1] == '\n') buf[cnt - 1] = '\x00';

}

int main(void) {
    char buf[SIZE];
    readn(buf, SIZE);
    scanf(buf);
    return 0;
}
