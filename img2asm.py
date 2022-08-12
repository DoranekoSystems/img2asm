import cv2
import os
import sys
import gen

INSTRUCTIONS = 26
WIDTH = 100
HEIGHT = 100
TIED = False
IMAGE = None


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
    return p("vfmaddsub132ps xmm0,xmm1,[rdi+rsi*4+1111111111111111h]")


def init_widen():
    code = ""
    code += p("xor rdi, rdi")
    code += p("xor rsi, rsi")
    return code


def s():
    code = "s:\n"
    for i in range(WIDTH + 1):
        code += p(f"dq e_0_{i}")
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
    asmcode += ".code\n"
    asmcode += s()
    asmcode += "asmcode:\n"
    asmcode += init_widen()
    asmcode += p("nop")
    asmcode += p("mov eax, 0")
    asmcode += p("jmp [s+eax*8]")

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
    asmcode += "end"
    with open("Native.asm", mode="w") as f:
        f.write(asmcode)


if __name__ == "__main__":
    args = sys.argv
    main(args[1])
