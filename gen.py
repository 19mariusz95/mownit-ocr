import os

import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

font_folder = "fonts"
fonts = []
for fontfilename in os.listdir(font_folder):
    file = font_folder + "/" + fontfilename
    fonts.append(file)

for i in range(0, len(fonts)):
    print(i, fonts[i])

print("width")
width = int(input())
print("height")
height = int(input())

print("which font?")

fi = int(input())
print("size")
size = int(input())
print("rotation")
rot = int(input())

font = PIL.ImageFont.truetype(fonts[fi], size)

fimage = Image.new("L", [width, height], 0)
draw = PIL.ImageDraw.Draw(fimage)
print("x y text")
flaga = True
while flaga:
    try:
        line = input()
        toks = line.split(" ", 2)
        x = int(toks[0])
        y = int(toks[1])
        text = toks[2]
        draw.text((x, y), text, font=font, fill=255)
    except Exception:
        flaga = False

if rot != 0:
    fimage = fimage.rotate(rot, expand=1)
fimage = PIL.ImageOps.invert(fimage)
fimage.save("test.png")
