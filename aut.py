import numpy as np
import PIL
from PIL import Image

'''
    does not work
'''


def repair_angle(image):
    image.show()
    data = np.array(image)
    fft = np.fft.fft2(data)
    max_p = np.max(np.abs(fft))
    fft[fft < (max_p * 0.25)] = 0
    abs_d = 1 + np.abs(fft)
    c = 255.0 / np.log(1 + max_p)
    log_data = c * np.log(abs_d)
    max_scaled_p = np.max(log_data)
    rows, cols = np.where(log_data > (max_scaled_p * 0.9999))
    min_col, max_col = np.min(cols), np.max(cols)
    min_row, max_row = np.min(rows), np.max(rows)
    dy, dx = max_col - min_col, max_row - min_row
    theta = np.arctan(dy / float(dx))
    print(theta)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    width, height = data.shape
    cx, cy = width / 2, height / 2
    new_image = np.zeros(data.shape)
    for x, row in enumerate(data):
        for y, value in enumerate(data):
            xp = cx + (x - cx) * cos_theta - (y - cy) * sin_theta
            yp = cy + (x - cx) * sin_theta + (y - cy) * cos_theta
            if xp < 0 or yp < 0 or xp >= width or yp >= height:
                continue
            new_image[xp, yp] = data[x, y]
    new_image = PIL.Image.fromarray(new_image)
    new_image.show()
    return image
