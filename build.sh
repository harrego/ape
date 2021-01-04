#!/bin/bash
python3 main.py example.ape 
nasm -f elf64 output.asm
ld -s -o test output.o
./test
