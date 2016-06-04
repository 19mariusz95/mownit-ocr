import PIL
from PIL import ImageFont
from PIL import ImageDraw
from PIL import Image
from PIL import ImageOps
import numpy as np

sizes = [72, 48, 36, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 9]

chars = "tabpeocjdfghkmnrsuwyvxzli0123456789?!"

tmpb = 2


def findchar(img, font, char, fft):
    siz = font.getsize(char)
    siz = [siz[0] + tmpb, siz[1] + tmpb]
    # print(char, siz)
    fimage = Image.new("L", siz, 255)
    draw = PIL.ImageDraw.Draw(fimage)
    draw.text((1, 1), char, font=font, fill=0)
    fimage = PIL.ImageOps.invert(fimage)
    # fimage.show()

    fft_e = np.fft.rfft2(np.rot90(fimage, 2), s=img.size[::-1])
    ifft = np.fft.irfft2(fft * fft_e)
    ifftchar = np.fft.irfft2(np.fft.rfft2(fimage) * np.fft.rfft2(np.rot90(fimage, 2), s=fimage.size[::-1]))
    max2 = ifftchar.max()
    count = 0
    list = []
    for i in range(0, ifft.shape[0]):
        for j in range(0, ifft.shape[1]):
            ifft[i][j] /= max2
    ddraw = PIL.ImageDraw.Draw(img)
    for i in range(0, ifft.shape[0]):
        for j in range(0, ifft.shape[1]):
            if ifft[i][j] < 0.9:
                ifft[i][j] = 0
            elif ifft[i][j] <= 1:
                ddraw.rectangle([j - siz[0] + tmpb, i - siz[1] + tmpb, j - tmpb, i - tmpb], fill="black")
                # img.show()
                list.append([i - siz[1], j - siz[0], char, ifft[i][j]])
                count += 1
    return count, list


def execute(img, font, fft):
    list = []
    for i in range(0, len(chars)):
        char = chars[i]
        fft = np.fft.rfft2(img)
        res = findchar(img, font, char, fft)
        list += res[1]
    return list


def checkfont(image, fontfilename):
    print(fontfilename)
    file = "fonts/" + fontfilename
    img = image.copy()
    fft = np.fft.rfft2(img)
    list = []
    for size in sizes:
        font = PIL.ImageFont.truetype(file, size)
        result = execute(img, font, fft)
        result = [x for x in result if len(x) > 1]
        result = sorted(result, key=lambda element: (element[0], element[1]))
        max = -1
        for x in result:
            if x[3] > max:
                max = x[3]
        list.append([result, font, size, max])
        img = image.copy()
    return list