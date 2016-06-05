import os
import sys

from PIL import Image

from aut import repair_angle
from ut import checkfont, tmpb
from PIL import ImageOps

alf = ".,!?0123456789abcdefghijklmnoprstuwyvxz"


def print_result(result):
    font = result[1]
    print("result for ", font.getname(), "size", result[2], "avg correlation", result[3])
    prev = -1
    spw = font.getsize(" ")[0]
    prevw = -tmpb
    for x in result[0]:
        n = (x[1] - prevw) / spw
        prevw = x[1] + font.getsize(x[2])[0]
        for i in range(0, int(n)):
            print(" ", end="")
        if prev == x[0]:
            print(x[2], end="")
        else:
            print()
            print(x[2], end="")
            prev = x[0]
    print()
    for i in range(0, len(alf)):
        char = alf[i]
        cnt = len([x for x in result[0] if x[2] == char])
        print(char, " : ", cnt)
    print()


if len(sys.argv) < 2:
    exit(1)

file_name = sys.argv[1]
image = Image.open(file_name)
image = image.convert('L')

image = ImageOps.invert(image)

font_folder = 'fonts'
results = []

for fontfilename in os.listdir(font_folder):
    results += checkfont(image, fontfilename)

results = sorted(results, key=lambda element: (element[3], element[2]), reverse=True)

for i in range(0, 3):
    print_result(results[i])
