# MIT License

# Copyright (c) 2018 Andrew Carter

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""PASCAL VOC XML annotation writer template."""

import os
from jinja2 import Environment, PackageLoader


class Writer:
    """PASCAL VOC XML annotation format writer.

    This is a class for generating PASCAL VOC XML annotation format according to
    the specified template.
    """

    def __init__(self, path, width, height, depth=3, database="Unknown", segmented=0):
        """Initializes the annotation.

        Args:
            path (str): The path to the annotated file.
            width (str): The width of the annotated image.
            height (str): The height of the annotated image.
            depth (int, optional): The depth of the annotated image. Defaults to 3.
            database (str, optional): The image source database. Defaults to "Unknown".
            segmented (int, optional): The value indicating segmentation. Defaults to 0.
        """
        environment = Environment(
            loader=PackageLoader("website", "templates"), keep_trailing_newline=True
        )
        self.annotation_template = environment.get_template("annotation.xml")

        abspath = os.path.abspath(path)

        self.template_parameters = {
            "path": abspath,
            "filename": os.path.basename(abspath),
            "folder": os.path.basename(os.path.dirname(abspath)),
            "width": width,
            "height": height,
            "depth": depth,
            "database": database,
            "segmented": segmented,
            "objects": []
        }

    def add_object(
        self,
        name,
        xmin,
        ymin,
        xmax,
        ymax,
        pose="Unspecified",
        truncated="0",
        difficult="0",
        occluded="0"
    ):
        """Appends an object to the annotation.

        Args:
            name (str): The name of the object annotated.
            xmin (str): The lowest x coordinate of the bounding box.
            ymin (str): The lowest y coordinate of the bounding box.
            xmax (str): The highest x coordinate of the bounding box.
            ymax (str): The highest y coordinate of the bounding box.
            pose (str, optional): The pose of the object. Defaults to "Unspecified".
            truncated (str, optional): The value indicating whether the object is truncated.
                                       If truncated: "1", if not "0". Defaults to "0".
            difficult (str, optional): The value indicating whether the object is difficult.
                                       If difficult: "1", if not "0". Defaults to "0".
            occluded (str, optional): The value indicating whether the object is occluded.
                                      If occluded: "1", if not: "0". Defaults to "0".
        """
        self.template_parameters["objects"].append(
            {
                "name": name,
                "xmin": xmin,
                "ymin": ymin,
                "xmax": xmax,
                "ymax": ymax,
                "pose": pose,
                "truncated": truncated,
                "difficult": difficult,
                "occluded": occluded,
            }
        )

    def save(self, annotation_path):
        """Saves the created annotation in a specified directory.

        Args:
            annotation_path (str): The path to the location for saving the annotation.
        """
        with open(annotation_path, "w", encoding="utf-8") as file:
            content = self.annotation_template.render(**self.template_parameters)
            file.write(content)
