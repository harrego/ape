output.asm: example.ape
		python3 main.py example.ape

all: output.asm
		nasm -f elf64 output.asm && ld output.o -o output

run: all
		./output

clean:
		rm *.o *.asm output
