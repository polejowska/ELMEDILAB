"""A320G.py file consists of functions processing the data from the A320G thermal camera sequence files."""

import math
import os
from PIL import Image
import numpy as np


HEADER_1ST_FRAME_LEN = 1372
HEADER_FRAME_LEN = 1372
FOOTER_LEN = 3860 + 32
IMAGE_DATA_LEN = 320 * 240 * 2
FIRST_FRAME_LEN = 1372 + (320 * 240 * 2) + 3860
FRAME_LEN = 1372 + (320 * 240 * 2) + 3860 + 32
IMAGE_SIZE = 320 * 240

# calibration constants
C1 = 21764040
C2 = 3033.3
C3 = 134.06


def convert_to_numpy(file, every=1, temp=False):
    """The function for reading data from a file and converting to numpy array.

    Args:
        file (str): The file.
        every (int, optional): The number specifying how many frames should be processed. Defaults to 1.
        temp (bool, optional): The temporary flag. Defaults to False.

    Returns:
        list: The list of sequences.
    """

    no_of_frames = int(os.stat(file).st_size / FRAME_LEN)

    index = 0
    seq = []
    with open(file, "rb") as fi:
        for _ in range(0, no_of_frames, every):
            if index == 0:
                fi.read(HEADER_1ST_FRAME_LEN)
                image_data = fi.read(IMAGE_DATA_LEN)
                fi.read(FOOTER_LEN)
            else:
                if every > 1:
                    for _ in range(1, every):
                        fi.read(FRAME_LEN)
                index = index + (every - 1)
                fi.read(HEADER_FRAME_LEN)
                image_data = fi.read(IMAGE_DATA_LEN)
                fi.read(FOOTER_LEN)

            res = np.empty([IMAGE_SIZE], dtype=int)

            for p in range(0, IMAGE_DATA_LEN, 2):
                result = int.from_bytes(
                    image_data[p : p + 2], byteorder="little", signed=False
                )
                if temp:
                    result_temp = (C2 / math.log(C3 + C1 / result) - 273.15) * 10
                else:
                    result_temp = result
                res[int(p / 2)] = result_temp
            seq.append(res)
            index = index + 1
    return seq


def save_image(filename, image, depth16=False):
    """The function for saving image data to graphical format PNG (data are automatically scaled to 0..255 or 0..65535).

    Args:
        filename (str): The filename.
        image (list): The image data.
        depth16 (bool, optional): The image depth specification. Defaults to False.
    """

    image = image.reshape([240, 320])

    if depth16:
        image = np.interp(image, (image.min(), image.max()), (0, 65535))
        image = np.uint16(image)
        array_buffer = image.tobytes()
        im = Image.frombytes("I", image.T.shape, array_buffer, "raw", "I;16")
    else:
        image = np.interp(image, (image.min(), image.max()), (0, 255))
        image = np.uint8(image)
        im = Image.frombytes("L", image.T.shape, image, "raw", "L")

    im.save(filename)


def generate_img_from_seq_A320G(path, frames):
    """The function for generating an image from A320 SEQ.

    Args:
        path (str): The path to the sequence file.
        frames (int): The number of frames.
    """
    frames_num = int(os.stat(path).st_size / FRAME_LEN)
    for i in range(1, frames_num, frames):
        dataset = convert_to_numpy(path, every=i)
        if len(dataset) == 5:
            break
        img = dataset[5].reshape((240, 320))
        save_image(path + "_" + "A320G" + "_frame_" + str(i) + ".png", img)