import os
from PIL import Image
import numpy as np


def get_int(byte1, byte2):
    """The function for getting an integer value.

    Args:
        byte1 (int): The first value sequence with offset.
        byte2 (int): The second value sequence with offset.

    Returns:
        int: The result value.
    """
    lsb = byte1
    msb = byte2

    if lsb < 0:
        lsb = lsb + 256
    if msb < 0:
        msb = msb + 256

    result = (msb << 8) + lsb
    return result


def get_img_A655SC(filename, frame_nr):
    """The function for getting image from A655SC camera model.

    Args:
        filename (str): The name of the sequence file.
        frame_nr (int): The frame to be captured.

    Returns:
        list: The list of sequences.
    """
    fid = open(filename, "rb")
    seq3 = np.fromfile(fid, dtype=np.ubyte)
    offset = 2781
    if frame_nr > 0:
        offset = (frame_nr - 2) * 617052 + 617180 + 2653 - 1
    matrix_2D = np.zeros((480, 640))
    seq = []
    for nr_y in range(480):
        for nr_x in range(640):
            value = seq3[offset]
            value = get_int(seq3[offset], seq3[offset + 1])
            matrix_2D[nr_y, nr_x] = value
            offset = offset + 2
    seq.append(matrix_2D)
    return seq


def generate_img_from_seq_A655SC(path, frames):
    """The function for generating image from A655SC sequence file.

    Args:
        path (str): The path to the file.
        frames (int): The value specyfing how often a frame should be captured.
    """
    bytes_num = int(os.stat(path).st_size)
    frames_num = int((bytes_num - 617180) / 617052 + 1)
    for i in range(1, frames_num, frames):
        dataset = get_img_A655SC(path, i)
        img = dataset[0]
        im3 = np.interp(img, (img.min(), img.max()), (0, 255))
        img = Image.fromarray(im3.astype(np.uint8))
        img.save(path + "_A655SC" + "_frame_" + str(i) + ".png", "PNG")
