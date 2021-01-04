# ape

## IMPORTANT

There is no integer support and if statements can only compare integers, this is only temporary. To fix this, after transpiling an Ape file you must replace the characters prefixing the string from "db" to "dd", remove the string length and remove the single quotes from after the number. After these changes if statements will work.

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
