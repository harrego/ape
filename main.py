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

for line in inputFileCode:
    lineSplit = line.split(" ")
    if lineSplit[0] == "var":
        if lineSplit[2] == "=":
            processedString = processString(" ".join(lineSplit[3:]))
            if processedString.get("type") == "string":
                variables[lineSplit[1]] = processedString["value"]
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
                    sectionStart.append(["print", newVar])
                elif processedString.get("type") == "var":
                    if processedString.get("value") in variables:
                        sectionStart.append(["print", processedString.get("value")])
                    else:
                        print("error: " + processedString.get("value") + " is not a variable!!!")

print(variables)
print(sectionStart)

finalFileLines = []
finalFileLines.append("SECTION .DATA")
for var in variables:
    finalFileLines.append("\t" + var + ": db '" + variables[var] + "'," + str(len(variables[var])))
    finalFileLines.append("\t" + var + "_SYSTEM_LEN: equ $-" + var)

finalFileLines.append("SECTION .TEXT")
finalFileLines.append("\tGLOBAL _start")

finalFileLines.append("_start:")
for instruction in sectionStart:
    if instruction[0] == "print":
        finalFileLines.append("\tmov eax,1")
        finalFileLines.append("\tmov ebx,1")
        finalFileLines.append("\tmov ecx," + instruction[1])
        finalFileLines.append("\tmov edx," + instruction[1] + "_SYSTEM_LEN")
        finalFileLines.append("\tint 80h")

finalFileLines.append("\tmov eax,1")
finalFileLines.append("\tmov ebx,0")
finalFileLines.append("\tint 80h")

finalFileLines.append("")

finalFile = "\n".join(finalFileLines)

outputFile = open("output.asm", "w")
outputFile.write(finalFile)
