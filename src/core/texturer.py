import av
import numpy as np
from PIL import Image

from loguru import logger
import dearpygui.dearpygui as imgui

def resize_image(img: Image, max_length: int = 500):

    width, height = img.size
    aspect_ratio = width / height

    if width > height:
        new_width = max_length
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = max_length
        new_width = int(new_height * aspect_ratio)

    resized_img = img.resize((new_width, new_height))

    return resized_img

def append_size_image(img: Image, size: tuple[int, int] | list[int, int]):
    if size is None or len(size) != 2:
        raise Exception

    img = img.convert('RGBA')
    new_img = Image.new("RGBA", size, 0)
    new_img.paste(img)
    return new_img


def img2array(img: Image):
    width, height = img.size
    arr = np.asfarray(img.getdata(), dtype='f')

    result = 1
    for size in arr.shape: result *=size

    if result != width * height * 4:
        raise Exception()

    arr = arr.reshape((width, height, 4))
    arr = np.true_divide(arr, 255.0)
    return arr

def get_first_frame(video_path: str):
    v = av.open(video_path)
    for f in v.decode(video=0):
        im = Image.fromarray(f.to_ndarray(format='rgb24')).convert('RGBA')
        # im.show()
        return im


def replenish_array_to(arr: np.ndarray, size: int):
    if len(arr.shape) != 3 or arr.shape[2] != 4:
        raise Exception()

    width = arr.shape[0]
    heigth = arr.shape[1]

    if width == size and heigth == size:
        return arr
    elif width == size:
        d = size - heigth
        if d > 0:
            zero = np.zeros((size, d, 4), dtype='f')
            arr = np.insert(arr, 1, zero, 1)
        else:
            raise Exception()
    elif heigth == size:
        d = size - width
        if d > 0:
            zero = np.zeros((d, size, 4), dtype='f')
            arr = np.insert(arr, 1, zero, 0)
        else:
            raise Exception()
    else:
        raise Exception()

    return arr
