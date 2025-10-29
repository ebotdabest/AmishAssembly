import os
import re, sys
import subprocess as sp

BSCHAR = list("01011100")
NCHAR = list("01101110")
VALID_OPCODES = {
        "mov", "add", "sub", "mul", "div", "inc", "dec",
        "push", "pop", "jmp", "je", "jne", "jg", "jl", "jge", "jle",
        "cmp", "test", "and", "or", "xor", "not", "call", "ret",
        "nop", "lea", "int", "shr", "shl", "sar", "sal",
        "stos", "lods", "xchg", "seta", "setb", "setc", "setg",
        "sete", "setne", "setl", "setle", "cmovz", "cmovnz",
    }

class LineByte:
    def __init__(self):
        self.byte = list("0"*8)
        self.index = 0

    def change(self):
        self.byte[self.index] = "1"

    def move(self):
        self.index += 1
        if self.index > 7:
            print("error")

    def output_char(self) -> str:
        num = int("".join(self.byte), 2)
        if num == 0: return None
        char = chr(num)
        return char

def compile(content: str) -> str:
    lines = content.split("\n")

    characters = []
    for line in lines:
        lineb = LineByte()
        for i, c in enumerate(line):
            if c == "]":
                lineb.move()
            elif c == "1":
                lineb.change()
            elif i == 0 and line[0] == "0" and line[2] == "0":
                if line[1] == "<":
                    characters.append("\n")
                elif line[1] ==">":
                    characters.append(" ")
                break

        char = lineb.output_char()
        if char: characters.append(char)

    return "".join(characters)

def check_for_structure(code: str):
    assembly_like = re.compile(
        r'^\s*'
        r'(?:[A-Za-z_][\w]*:\s*)?' 
        r'(?:[A-Za-z]{2,7}\s+' 
        r'(?:[\w\[\]+\-*/$,.\s%]+))'
        r'(?:\s*;.*)?$'
    )

    for i, line in enumerate(code.split("\n")):
        if not assembly_like.match(line):
            print(f"AH AH NOT ASSEMBLY CUNT! AT LINE {i+1}:{line}")
            return False

        return True

def opcode_check(code: str):
    pattern = re.compile(r'^\s*(?:[A-Za-z_]\w*:\s*)?([A-Za-z]{2,7})\b')
    for line in code.split("\n"):
        match = pattern.match(line)
        return match


with open(sys.argv[1]) as f:
    content = f.read()

compiled = compile(content)

assembly_structure = check_for_structure(compiled)
if not assembly_structure:
    print("Well fuck you too then!")
    exit()

if not opcode_check(compiled):
    print("WELL FUCK YOU TWICE!")
    exit()

with open("output.asm", "w") as f:
    f.write(compiled)

if os.name == "nt":
    tpe = "win64"
else:
    tpe = "elf64"

result = sp.run(["nasm", f"-f{tpe}", "output.asm", "-o", "output.o"],
                            capture_output=True, text=True)
if result.returncode != 0:
    print("ERROR!!!")
    print(result.stderr)

linker = sp.run(["clang", "-o", sys.argv[1].replace(".aasm", ".exe"), "output.o"])

os.remove("output.asm")
print("ASSEMBLED!")