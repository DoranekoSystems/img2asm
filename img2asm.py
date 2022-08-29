import cv2
import os
import sys
import gen
import toml

INSTRUCTIONS = 26
WIDTH = 100
HEIGHT = 100
TIED = False
IMAGE = None

with open("config.toml", "rt") as fp:
    config = toml.load(fp)

PLATFORM = config["Option"]["compiler"]
LARGEADDRESSAWARE_YES = config["Option"]["large_address_aware_yes"]

if PLATFORM == "msvc":
    OUTPUT_FILENAME = "Native.asm"
else:
    OUTPUT_FILENAME = "Native.s"


def image_load(filename):
    global IMAGE
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    img = 255 - img
    img = cv2.resize(img, dsize=(WIDTH, HEIGHT))
    th, img = cv2.threshold(img, 128, 192, cv2.THRESH_OTSU)
    IMAGE = img


def p(code):
    return " " + code + "\n"


def widen():
    if PLATFORM == "msvc":
        return p("vfmaddsub132ps xmm0,xmm1,[rdi+rsi*4+1111111111111111h]")
    else:
        return p("vfmaddsub132ps xmm0,xmm1,[rdi+rsi*4+0x11111111]")


def init_widen():
    code = ""
    code += p("xor rdi, rdi")
    code += p("xor rsi, rsi")
    return code


def s():
    code = "s:\n"
    for i in range(WIDTH + 1):
        if PLATFORM == "msvc":
            code += p(f"dq e_0_{i}")
        else:
            code += p(f".quad e_0_{i}")
    return code


def check(x, y):
    return IMAGE[y, x]


def block_fill(r, c):
    asmcode = ""
    pixel = 0
    if c == 0:
        pixel = 255
    else:
        T = c - 1
        pixel = check(T, r)
    asmcode += widen()

    lines = int(pixel * INSTRUCTIONS / 255)
    for i in range(lines):
        asmcode += p(gen.rand_insn())
    return asmcode


def diag(row, column, width, height, done):
    asmcode = ""
    r = row
    c = column
    for i in range(256):
        nr = r + 1
        if TIED:
            nc = c + 1
        else:
            nc = c
        if TIED:
            if nc >= width:
                asmcode += widen()
                asmcode += p(f"jmp e_{r}_{c}")

        asmcode += f"e_{r}_{c}:\n"
        if nr >= height:
            asmcode += block_fill(r, c)
        elif TIED and (nc >= width):
            asmcode += block_fill(r, c)
            asmcode += p(f"je e_{nr}_{c}")
        else:
            if c == 0:
                asmcode += block_fill(r, c)
                asmcode += p(f"jmp e_{nr}_{nc}")

                if TIED:
                    break
            else:
                asmcode += block_fill(r, c)
                if TIED:
                    asmcode += p(f"je e_{nr}_{nc}")
                else:
                    asmcode += p(f"jmp e_{nr}_{nc}")
        r = r + 1
        if TIED:
            c = c - 1
        if r >= height:
            asmcode += p(f"jmp {done}")
            break
    return asmcode


def main(filename):
    image_load(filename)

    asmcode = ""
    if PLATFORM == "gnu":
        asmcode += ".intel_syntax noprefix\n"

    if PLATFORM == "msvc":
        asmcode += ".code\n"
        asmcode += "asmcode proc EXPORT\n"
    else:
        asmcode += ".global asmcode\n"
        asmcode += "asmcode:\n"
    asmcode += init_widen()
    asmcode += p("nop")
    if LARGEADDRESSAWARE_YES:
        for i in range(int(WIDTH / 2) + 1):
            asmcode += p(f"je e_0_{i}")
            asmcode += p(f"jne e_0_{WIDTH - i}")
    else:
        asmcode += p("mov eax, 0")
        asmcode += p("jmp [s + eax *8]")

    CC = 0
    for i in range(WIDTH + 1):
        asmcode += diag(0, CC, WIDTH + 1, HEIGHT, "done")
        CC += 1
    if TIED:
        RC = 1
        for i in range(HEIGHT - 1):
            asmcode += diag(RC, WIDTH, WIDTH + 1, HEIGHT, "done")
            RC += 1
    asmcode += "done:\n"
    asmcode += p("ret")
    if not LARGEADDRESSAWARE_YES:
        asmcode += s()
    if PLATFORM == "msvc":
        asmcode += "asmcode endp\n"
        asmcode += "end"
    else:
        pass
    with open(OUTPUT_FILENAME, mode="w") as f:
        f.write(asmcode)


if __name__ == "__main__":
    args = sys.argv
    main(args[1])
