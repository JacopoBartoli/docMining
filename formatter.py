import xml.etree.ElementTree as et
import os
from rectangle import Rectangle
from filesplitter import FileSplitter
from PIL import Image


def create_rectangle(points, img_width=1, img_height=1):
    # Points[0][0] refer to the x coord of the upper left angle.
    # Points[1][0] refer to the x coord of the upper right angle.
    # Points[2][0] refer to the x coord of the bottom left angle.
    # Points[3][0] refer to the x coord of the bottom right angle.
    width = points[1][0] - points[0][0]
    height = points[2][1] - points[0][1]

    x_center = (points[1][0] - points[0][0]) / 2.0
    y_center = (points[2][1] - points[0][1]) / 2.0

    return Rectangle(width/img_width, height/img_height, x_center/img_width, y_center/img_height)


# Parse the string received from the xml file, and create a rectangle.
# Use parameters img_width and img_height for normalized the dimension of the rectangle (xywh in (0,1)).
def calc_box(coord, img_width=1, img_height=1):
    # The key for this dictionary is 'points'.
    key = 'points'
    coord_dict=coord.attrib

    # Iterate over the string to collect the data.
    points = []
    current_number = ''
    prev_number = ''
    for char in coord_dict[key]:
        if char == ' ':
            points.append((int(prev_number), int(current_number)))
            prev_number = ''
            current_number = ''
        elif char == ',':
            prev_number = current_number
            current_number = ''
        else:
            current_number = current_number + char
    points.append((int(prev_number), int(current_number)))
    return create_rectangle(points, img_width, img_height)


def get_classes(dir_path):
    class_dict = {}
    index = 0
    for filename in os.listdir(dir_path):
        tree = et.parse(dir_path + '/' + filename)
        root = tree.getroot()
        for child in root:
            class_dict[child.tag] = index
    return class_dict


def save_classes(classes, path):
    file = open(path, 'w+')
    for key in classes.keys():
        file.write(str(key) + '\n')
    file.close()


def icdar_to_darknet():
    # Path of input annotations.
    in_annotations_dir = "./Dataset/icdar_2017/Annotations"
    # Output path for the new annotations.
    out_annotations_dir = "./Dataset/icdar/labels"
    # Path of input images.
    in_image_dir = "./Dataset/icdar_2017/Images"
    # Output path for the new images.
    out_image_dir = "./Dataset/icdar/images"

    # Get the dictionary with all the classes
    classes_dir = "./Dataset/icdar.names"
    class_dict = get_classes(in_annotations_dir)
    save_classes(class_dict, classes_dir)

    for filename in os.listdir(in_annotations_dir):
        tree = et.parse(in_annotations_dir + '/' + filename)
        root = tree.getroot()
        # Storing the corresponding image to the file.
        img_filename = in_image_dir+'/' + filename.replace('.xml', '.bmp')
        img = Image.open(img_filename)
        if len(root.items()) != 0:
            out_annotation = open(out_annotations_dir + '/' + filename.replace('.xml', '.txt'), "w+")
        for child in root:
            for item in child:
                if item.tag == 'Coords':
                    img_width,  img_height = img.size
                    normalized_box = calc_box(item, img_width, img_height)
                    # Create new annotation files and save them in the right directory, and in the right format(.txt).
                    out_annotation.write(str(class_dict[child.tag]) + ' ')
                    out_annotation.write(str(normalized_box.x_center) + ' ')
                    out_annotation.write(str(normalized_box.y_center) + ' ')
                    out_annotation.write(str(normalized_box.width) + ' ')
                    out_annotation.write(str(normalized_box.height) + '\n')

                    # Create new image files and save them in the right directory, and in the right format(.jpg)
        img.save(out_image_dir + '/' + filename.replace('.xml', '.jpg'))
        out_annotation.close()


if __name__ == '__main__':
    icdar_to_darknet()
    fs = FileSplitter(1600)
    fs.split(20)
