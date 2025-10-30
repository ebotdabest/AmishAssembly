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
        "extern", "section"
    }

class LineByte:
    """
    A helper class to represent a singular line which is the size of a byte
    """
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
    """
    Parses the code for each line and then turns it into whatever it needs to be
    :param content: The RAW content
    :return:
    """
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
    """
    Checks the code if it LOOKS like Assembly, so you know... no cheating?
    :param code: The code duh
    :return:
    """

    # When I found this one, man I came a little
    assembly_like = re.compile(
        r'^\s*'
        r'(?:[A-Za-z_][\w]*:\s*)?'
        r'(?:[A-Za-z]{2,7}\s+'    
        r'(?:[\w\[\]+\-*/$,.\s%]+))?'
        r'(?:\s*;.*)?$'
    )

    in_data_section = False

    for i, line in enumerate(code.split("\n"), 1):
        stripped = line.strip()

        if not stripped or stripped.startswith(";"):
            continue

        if stripped.startswith("section"):
            if any(x in stripped for x in (".data", ".bss", ".rodata")):
                in_data_section = True
            elif ".text" in stripped:
                in_data_section = False
            continue

        if in_data_section:
            continue

        if re.match(r'^[A-Za-z_][\w]*:\s*$', stripped):
            continue

        if not assembly_like.match(stripped):
            print(f"AH AH NOT ASSEMBLY CUNT! AT LINE {i}: {line}")
            return False

    return True

def opcode_check(code: str):
    """
    Checks if the opcodes are valid and stuff
    :param code: The code duh
    :return:
    """
    # stolen pattern
    pattern = re.compile(r'^\s*(?:[A-Za-z_]\w*:\s*)?([A-Za-z]{2,7})\b')
    in_data_section = False

    for i, line in enumerate(code.split("\n"), 1):
        stripped = line.strip()

        if not stripped or stripped.startswith(";"):
            continue

        if stripped.startswith("section"):
            if any(x in stripped for x in (".data", ".bss", ".rodata")):
                in_data_section = True
            elif ".text" in stripped:
                in_data_section = False
            continue

        if in_data_section:
            continue

        if stripped.startswith(("global", "extern")) or re.match(r'^[A-Za-z_][\w]*:\s*$', stripped):
            continue

        match = pattern.match(stripped)
        if not match:
            print(f"THIS AINT A GODDAMN OPCODE SWEETY CAKES {i}: {line}")
            return False

        opcode = match.group(1).lower()
        if opcode not in VALID_OPCODES:
            print(f"THE FUCK KINDA OPCODE IS THIS '{opcode}' BULLSHIT AT LINE {i}")
            return False

    return True



with open(sys.argv[1]) as f:
    content = f.read()

compiled = compile(content)

assembly_structure = check_for_structure(compiled)
if not assembly_structure:
    print("Well fuck you too then! This don't look like assembly to me, nuh uh!")
    exit()

if not opcode_check(compiled):
    print("WELL FUCK YOU TWICE! FAILED AGAIN 2 STRIKES YOU'RE OUT!!!")
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
print("ASSEMBLED, SOMEHOW!")