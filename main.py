import os
import sys

import PIL.ImageDraw
from PIL import Image
from ut import checkfont, tmpb
from PIL import ImageOps

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

for x in results:
    print(x[1].getname(), x[2], len(x[0]), x[3])

result = results[0][0]
font = results[0][1]
prev = -1
spw = font.getsize(" ")[0]
prevw = -tmpb
for x in result:
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
