import os
import sys
import random


def randreg():
    R = random.randint(0, 3)
    reg = ""
    if R == 0:
        reg = "eax"
    elif R == 1:
        reg = "ebx"
    elif R == 2:
        reg = "ecx"
    elif R == 3:
        reg = "edx"
    return reg


def randregl():
    R = random.randint(0, 7)
    reg = ""
    if R == 0:
        reg = "al"
    elif R == 1:
        reg = "bl"
    elif R == 2:
        reg = "cl"
    elif R == 3:
        reg = "dl"
    elif R == 4:
        reg = "ah"
    elif R == 5:
        reg = "bh"
    elif R == 6:
        reg = "ch"
    elif R == 7:
        reg = "dh"
    return reg


def randbiop():
    R = random.randint(0, 7)
    biop = ""
    if R == 0:
        biop = "add"
    elif R == 1:
        biop = "sub"
    elif R == 2:
        biop = "and"
    elif R == 3:
        biop = "or"
    elif R == 4:
        biop = "xor"
    elif R == 5:
        biop = "cmp"
    elif R == 6:
        biop = "test"
    elif R == 7:
        biop = "mov"
    return biop


def randomoop():
    R = random.randint(0, 3)
    oop = ""
    if R == 0:
        oop = "inc"
    elif R == 1:
        oop = "dec"
    elif R == 2:
        oop = "not"
    elif R == 3:
        oop = "mul"
    return oop


def rand_insn():
    R = random.randint(0, 9)
    if R == 0:
        op = randomoop()
        r1 = randreg()
        return f"{op} {r1}"
    elif R == 1:
        op = randbiop()
        r1 = randreg()
        r2 = randreg()
        return f"{op} {r1}, {r2}"
    elif R == 2:
        op = randbiop()
        r1 = randreg()
        R = random.randint(0, 0xFFFFFFFF)
        return f"{op} {r1}, {R}"
    elif R == 3:
        r1 = randreg()
        r2 = randreg()
        r3 = randreg()
        return f"lea {r3}, [{r1}+4*{r2}]"
    elif R == 4:
        r1 = randreg()
        r2 = randreg()
        return f"lea {r1}, [{r2}*2]"
    elif R == 5:
        r1 = randreg()
        R = random.randint(0, 6)
        return f"lea {r1}, [ebp+{R}*4]"
    elif R == 6:
        r1 = randreg()
        R = random.randint(0, 32)
        return f"shl {r1}, {R}"
    elif R == 7:
        r1 = randreg()
        R = random.randint(0, 32)
        return f"shr {r1}, {R}"
    elif R == 8:
        r1 = randregl()
        R = random.randint(0, 0xFF)
        return f"mov {r1}, {R}"
    elif R == 9:
        r1 = randreg()
        r2 = randregl()
        return f"movzx {r1}, {r2}"
