# ape

Generic C style language -> elf64 NASM transpiler

## Usage

There is a `Makefile` included with the repo, running `make run` will compile and run `example.ape` included.

These are the manual steps to build and run:

1) `python3 main.py <file>.ape`
2) `nasm -f elf64 output.asm`
3) `ld output.o`
4) `./a.out`

## Supports

- [x] Variables
- [x] Print
- [x] Strings

## Generic Language?

The syntax of an `ape` file is not yet decided but looks like a generic C style language.