from __future__ import division, print_function

import numpy
from PIL import Image
from matplotlib.mlab import rms_flat
from numpy import mean, array
from skimage.transform import radon

try:
    from parabolic import parabolic


    def argmax(x):
        return parabolic(x, numpy.argmax(x))[0]
except ImportError:
    from numpy import argmax


def repair_angle(image):
    old_image = image
    image = image - mean(image)
    sinogram = radon(image)
    r = array([rms_flat(line) for line in sinogram.transpose()])
    rotation = argmax(r)
    rotation = 90 - rotation
    image = Image.fromarray(image)
    image = image.rotate(rotation, expand=1, resample=Image.BICUBIC)
    if rotation != 0:
        print("Rotation: ", rotation)
        old_image.show()
        image.show()
        return image
    return old_image
