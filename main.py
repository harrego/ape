import sys
import random
import string

print("ape [alpha 1]\n")


inputFile = open(sys.argv[1])
inputFileCode = inputFile.read().split("\n")

def processString(str):
    if str[0] == "\"" and str[-1] == "\"":
        return {"type": "string", "value": str[1:-1]}
    else:
        return {"type": "var", "value": str}

sectionStart = []
variables = {}
sections = []

inlineParentInstruction = None

for line in inputFileCode:
    lineSplit = line.split(" ")

    if lineSplit[0] == "}":
        if inlineParentInstruction is None:
            print("YOU'RE ENDING AN INLINE YOU NEVER STARTED DUMBASS!")
            sys.exit()
        sectionStart.append(inlineParentInstruction)
        inlineParentInstruction = None

    if lineSplit[0] == "var":
        if lineSplit[2] == "=":
            processedString = processString(" ".join(lineSplit[3:]))
            if processedString.get("type") == "string":
                variables[lineSplit[1]] = processedString["value"]
    if lineSplit[0] == "if":
        if inlineParentInstruction is not None:
            print("YOU CAN'T USE INLINE CODE INSIDE OF INLINE CODE!")
            sys.exit()
        comparisonX = lineSplit[1]
        comparisonY = lineSplit[3]
        if lineSplit[2] == "==" and lineSplit[4] == "{":
            if comparisonX in variables and comparisonY in variables:
                inlineParentInstruction = ["if", [comparisonX, comparisonY], []]
            else:
              print("Invalid variables used in statement") 
    else:
        # check if function
        functionSplit = line.split("(")
        if len(functionSplit) > 1:
            arguments = functionSplit[1].split(")")[0]
            arguments = arguments.split(",")
            if functionSplit[0] == "print":
                processedString = processString(arguments[0])
                if processedString.get("type") == "string":
                    randomStr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                    newVar = "unnamed_var_" + randomStr
                    variables[newVar] = processedString["value"]

                    instruction = ["print", newVar]
                    if inlineParentInstruction is None:
                        sectionStart.append(instruction)
                    else:
                        inlineParentInstruction[2].append(instruction)
                elif processedString.get("type") == "var":
                    if processedString.get("value") in variables:
                        instrucion = ["print", processedString.get("value")]
                        if inlineParentInstruction is None:
                            sectionStart.append(instruction)
                        else:
                            inlineParentInstruction[2].append(instruction)
                    else:
                        print("error: " + processedString.get("value") + " is not a variable!!!")

print(variables)
print(sectionStart)

def parseInstructions(instructions):
    parsedLines = []
    for instruction in instructions:
        print("3")
        if instruction[0] == "print":
            parsedLines.append("\tmov rax,1")
            parsedLines.append("\tmov rdi,1")
            parsedLines.append("\tmov rsi," + instruction[1])
            parsedLines.append("\tmov rdx," + instruction[1] + "_SYSTEM_LEN")
            parsedLines.append("\tsyscall")
        elif instruction[0] == "if":
            parsedLines.append("\tmov eax,[" + instruction[1][0] + "]")
            parsedLines.append("\tmov ebx,[" + instruction[1][1] + "]")
            parsedLines.append("\tcmp eax,ebx")
            randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
            successJump = ".SUCCESS_" + randomName
            parsedLines.append("\tje " + successJump)
            
            sections.append([successJump, instruction[2]])
    return parsedLines

finalFileLines = []
finalFileLines.append("global _start")
finalFileLines.append("section .data")
for var in variables:
    finalFileLines.append("\t" + var + ": db '" + variables[var] + "'," + str(len(variables[var])))
    finalFileLines.append("\t" + var + "_SYSTEM_LEN: equ $-" + var)

finalFileLines.append("section .text")

finalFileLines.append("_start:")
for line in parseInstructions(sectionStart):
    finalFileLines.append(line)
finalFileLines.append("\tjmp .end")

for section in sections:
    finalFileLines.append(section[0] + ":")
    for instructions in parseInstructions(section[1]):
      finalFileLines.append(instructions)
    finalFileLines.append("\tjmp .end")

finalFileLines.append(".end:")
finalFileLines.append("\tmov rax,60")
finalFileLines.append("\txor rdi,rdi")
finalFileLines.append("\tsyscall")

finalFile = "\n".join(finalFileLines)

outputFile = open("output.asm", "w")
outputFile.write(finalFile)
