"""Functions processing the data from the Flir SC3000 thermal camera sequence files."""

import numpy as np
import math
import os
from PIL import Image

HEADER_1ST_FRAME_LEN = 696
HEADER_FRAME_LEN = 568
FOOTER_LEN = 3840
IMAGE_DATA_LEN = 320 * 240 * 2
FIRST_FRAME_LEN = 696 + (320 * 240 * 2) + 3840
FRAME_LEN = 568 + (320 * 240 * 2) + 3840
IMAGE_SIZE = 320 * 240

# calibration constants
C1 = 21764040
C2 = 3033.3
C3 = 134.06


def read_image_data_from_file(file, index, temp=False):
    """Read data2 from a file."""

    with open(file, "rb") as fi:
        if index == 0:
            fi.read(HEADER_1ST_FRAME_LEN)
            image_data = fi.read(IMAGE_DATA_LEN)
        else:
            fi.read(FIRST_FRAME_LEN)
            for _ in range(1, index - 1):
                fi.read(FRAME_LEN)
            fi.read(HEADER_FRAME_LEN)
            image_data = fi.read(IMAGE_DATA_LEN)

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

        return res


def convert_to_numpy(file, every=1, temp=False):
    """Read data2 from a file and convert to numpy array."""

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


def gen_images_from_seq(src_filename, subject, dest_path, every=1, depth16=False):
    """The function for generating PNG files from the sequence of thermal images (data2 are automatically scaled to 0..255 or 0..65535)

    Args:
        src_filename ([type]): The full path to the source file with a sequence of thermal images.
        subject ([type]): [description]
        dest_path ([type]): The destination folder.
        every (int, optional): Index hoe often images will be generated: 1-all frames, 2- every second frame, etc.. Defaults to 1.
        depth16 (bool, optional): If True then PNG files with depth of 16 bits will be generated. Defaults to False.
    """
    no_of_frames = int(os.stat(src_filename).st_size / FRAME_LEN)
    if depth16:
        img_depth = "16bits"
    else:
        img_depth = "8bits"

    for i in range(0, no_of_frames, every):
        data = read_image_data_from_file(src_filename, i, False)
        dest_filename = (
            dest_path + "/" + subject + "_frame_" + str(i) + "_" + img_depth + ".png"
        )
        save_image(dest_filename, data, depth16)
