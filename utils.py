import xml.etree.ElementTree as Et
import os
from rectangle import Rectangle
from filesplitter import FileSplitter
from PIL import Image
import cv2
import image_transformer
import numpy as np
import struct


def create_rectangle(points, img_width=1, img_height=1):
    # Create a bounding box in darknet format.

    # Points[0][0] refer to the x coord of the upper left angle.
    # Points[1][0] refer to the x coord of the upper right angle.
    # Points[2][0] refer to the x coord of the bottom left angle.
    # Points[3][0] refer to the x coord of the bottom right angle.
    width = points[1][0] - points[0][0]
    height = points[2][1] - points[0][1]

    x_center = points[0][0] + width / 2.0
    y_center = points[0][1] + height / 2.0

    return Rectangle(width / img_width, height / img_height, x_center / img_width, y_center / img_height)


def create_rectangle_marmot(points, img_width=1, img_height=1):
    # Alternative version of the create_rectangle.
    # Create a bounding box in darknet format.

    # Points[0][0] refer to the x coord of the upper left angle.
    # Points[1][0] refer to the x coord of the upper right angle.
    # Points[2][0] refer to the x coord of the bottom left angle.
    # Points[3][0] refer to the x coord of the bottom right angle.
    width = points[1, 0] - points[0, 0]
    height = points[2, 1] - points[0, 1]
    x_center = (points[1, 0] - points[0, 0]) / 2.0
    y_center = (points[2, 1] - points[0, 1]) / 2.0
    return Rectangle(width / img_width, height / img_height, x_center / img_width, y_center / img_height)


# convert hexadecimal to decimal
def convert_to_decimal(coord, img_height):
    # Takes the whole string relative to the BBox

    # Each coord of the box is represented by an hexadecimal number.
    # The characters from 10 to 25 contains the information of the x coord of the top left corner.
    # The characters from 27 to 42 contains the information of the y coord of the top left corner.
    # The characters from 44 to 59 contains the information of the x coord of the top left corner.
    # The characters from 61 to 76 contains the information of the y coord of the top left corner.
    i = 0
    x1 = ''
    y1 = ''
    x2 = ''
    y2 = ''
    for char in coord:
        if 10 <= i <= 25:
            x1 = x1 + char
        if 27 <= i <= 42:
            y1 = y1 + char
        if 44 <= i <= 59:
            x2 = x2 + char
        if 61 <= i <= 76:
            y2 = y2 + char
        i = i + 1

    # The couple of strings (x1,y1) represent the top left corner coord.
    # The couple of strings (x2,y2) represent the bottom left corner coord.
    bbox = [x1, y1, x2, y2]

    # Convert hex strings to decimal numbers.
    conv_pound = [struct.unpack('!d', bytes.fromhex(t))[0] for t in bbox]
    i = 0
    for c in conv_pound:
        if i % 2 == 0:
            c = (c * 96 / 72)
        else:
            c = img_height - (c * 96 / 72)
        conv_pound[i] = c
        i = i + 1
    return conv_pound


# Parse the string received from the xml file, and create a rectangle.
# Use parameters img_width and img_height for normalized the dimension of the rectangle (xywh in (0,1)).
def calc_box(coord, img_width=1, img_height=1):
    # The key for this dictionary is 'points'.
    key = 'points'
    coord_dict = coord.attrib

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


def calc_box_marmot(box_converted, img_width=1, img_height=1):
    # Assign value to each point, box_converted contains in order [x_up_left, y_up_left, x_bottom_right, y_bottom_right]
    # Points[0,0] refer to the x coord of the upper left angle.
    # Points[1,0] refer to the x coord of the upper right angle.
    # Points[2,0] refer to the x coord of the bottom left angle.
    # Points[3,0] refer to the x coord of the bottom right angle.

    # Initialize the dot matrix
    points = np.zeros((4, 2))
    # Assign the x in the upper left
    points[0, 0] = box_converted[0]
    # Assign the y in the upper left
    points[0, 1] = box_converted[1]
    # Assign the x at the bottom right
    points[3, 0] = box_converted[2]
    # Assign the y at the bottom right
    points[3, 1] = box_converted[3]

    # Calculate the remaining rectangle points.
    # Assign x top right = x bottom right
    points[1, 0] = points[3, 0]
    # Assign y top right = y top left
    points[1, 1] = points[0, 1]
    # Assign x bottom left = x top left
    points[2, 0] = points[0, 0]
    # Assign y bottom left = y bottom right
    points[2, 1] = points[3, 1]
    return create_rectangle_marmot(points, img_width, img_height)


# OBSOLETE, there is only a binary representation.
def get_classes(dir_path):
    # Get the list of all the classes of the ICDAR dataset.
    class_dict = {}
    index = 0
    for filename in os.listdir(dir_path):
        tree = Et.parse(dir_path + '/' + filename)
        root = tree.getroot()
        for child in root:
            if child.tag not in class_dict:
                class_dict[child.tag] = index
                index = index + 1
    return class_dict


# OBSOLETE, now there is only a binary representation
def save_classes(classes, path):
    # Store all the classes in a file
    file = open(path, 'w+')
    for key in classes.keys():
        file.write(str(key) + '\n')
    file.close()


# # Convert the ICDAR 2017 POD dataset into the darknet format.
# OBSOLETE representation, the not binary one.
# def icdar_to_darknet():
#     # Pass the path as parameter here too?
#
#     # Path of input annotations.
#     in_annotations_dir = "./Dataset/icdar_2017/Annotations"
#     # Output path for the new annotations.
#     out_annotations_dir = "./Dataset/icdar/labels"
#     # Path of input images.
#     in_image_dir = "./Dataset/icdar_2017/Images"
#     # Output path for the new images.
#     out_image_dir = "./Dataset/icdar/images"
#
#     # Get the dictionary with all the classes
#     classes_dir = "./Dataset/icdar.names"
#     class_dict = get_classes(in_annotations_dir)
#     print(class_dict)
#     save_classes(class_dict, classes_dir)
#
#     for filename in os.listdir(in_annotations_dir):
#         tree = et.parse(in_annotations_dir + '/' + filename)
#         root = tree.getroot()
#         # Storing the corresponding image to the file.
#         img_filename = in_image_dir + '/' + filename.replace('.xml', '.bmp')
#         img = Image.open(img_filename)
#         if len(root.items()) != 0:
#             out_annotation = open(out_annotations_dir + '/' + filename.replace('.xml', '.txt'), "w+")
#         for child in root:
#             for item in child:
#                 if item.tag == 'Coords':
#                     img_width, img_height = img.size
#                     normalized_box = calc_box(item, img_width, img_height)
#                     # Create new annotation files and save them in the right directory, and in the right format(.txt).
#                     out_annotation.write(str(class_dict[child.tag]) + ' ')
#                     out_annotation.write(str(normalized_box.x_center) + ' ')
#                     out_annotation.write(str(normalized_box.y_center) + ' ')
#                     out_annotation.write(str(normalized_box.width) + ' ')
#                     out_annotation.write(str(normalized_box.height) + '\n')
#
#                     # Create new image files and save them in the right directory, and in the right format(.jpg)
#         img.save(out_image_dir + '/' + filename.replace('.xml', '.jpg'))
#         out_annotation.close()


def convert_marmot(in_annotations_dir, in_image_dir, out_annotations_dir, out_image_dir, classes_dir):
    # Create the.names file
    file = open(classes_dir, 'w+')
    file.write('tableRegion')
    file.close()

    for filename in os.listdir(in_annotations_dir):
        tree = Et.parse(in_annotations_dir + '/' + filename)
        root = tree.getroot()
        # Storing the corresponding image to the file.
        img_filename = in_image_dir+'/' + filename.replace('.xml', '.bmp')
        img = Image.open(img_filename)
        for child in root:
            for item in child:
                st = str(item.attrib)
                if st == "{'Label': 'Table'}":
                    out_annotation = open(out_annotations_dir + '/' + filename.replace('.xml', '.txt'), "w+")
                    for last in item:
                        img_width,  img_height = img.size
                        coord = str(last.attrib)
                        box_converted = convert_to_decimal(coord, img_height)
                        normalized_box = calc_box_marmot(box_converted, img_width, img_height)
                        # Insert the item in the annotation files and save them in the right directory,
                        # and in the right format(.txt).
                        out_annotation.write('1 ')
                        out_annotation.write(str(normalized_box.x_center) + ' ')
                        out_annotation.write(str(normalized_box.y_center) + ' ')
                        out_annotation.write(str(normalized_box.width) + ' ')
                        out_annotation.write(str(normalized_box.height) + '\n')
                    out_annotation.close()
        # Create new image files and save them in the right directory, and in the right format(.jpg)
        img.save(out_image_dir + '/' + filename.replace('.xml', '.jpg'))


# Convert the ICDAR 2017 POD dataset into the darknet format.
def convert_icdar(in_annotations_dir, in_image_dir, out_annotations_dir, out_image_dir, classes_dir):
    # Binary class representation.
    # Create the.names file
    file = open(classes_dir, 'w+')
    file.write('tableRegion')
    file.close()
    # Explore the directory.
    for filename in os.listdir(in_annotations_dir):
        tree = Et.parse(in_annotations_dir + '/' + filename)
        root = tree.getroot()
        # Storing the corresponding image to the file.
        img_filename = in_image_dir + '/' + filename.replace('.xml', '.bmp')
        img = Image.open(img_filename)
        out_annotation = open(out_annotations_dir + '/' + filename.replace('.xml', '.txt'), "w+")
        for child in root:
            if child.tag == 'tableRegion':
                # Create the file only if there is a tableRegion object.
                for item in child:
                    if item.tag == 'Coords':
                        img_width, img_height = img.size
                        normalized_box = calc_box(item, img_width, img_height)
                        # Insert the item in the annotation files and save them in the right directory,
                        # and in the right format(.txt).
                        out_annotation.write(str(1) + ' ')
                        out_annotation.write(str(normalized_box.x_center) + ' ')
                        out_annotation.write(str(normalized_box.y_center) + ' ')
                        out_annotation.write(str(normalized_box.width) + ' ')
                        out_annotation.write(str(normalized_box.height) + '\n')
        out_annotation.close()
        # Create new image files and save them in the right directory, and in the right format(.jpg)
        img.save(out_image_dir + '/' + filename.replace('.xml', '.jpg'))



# !!!Probably this will not be used.
def convert_test(input_dir, output_dir):
    # Convert unlabeled images in Darknet format.
    for filename in os.listdir(input_dir):
        img_filename = input_dir + '/' + filename
        img = Image.open(img_filename)
        img.save(output_dir + '/' + filename.replace('.bmp', '.jpg'))


def transform_dataset(input_dir, output_dir):
    # Transform the train images in the black and white one.

    for filename in os.listdir(input_dir):
        img_filename = input_dir + '/' + filename
        image = cv2.imread(img_filename)
        trs = image_transformer.image_transformation(image)
        cv2.imwrite(output_dir + '/' + filename, trs)


# !!!Probably this will not be used.
def transform_test_set(input_dir, output_dir):
    # Transform the test images in the black and white one.

    for filename in os.listdir(input_dir):
        img_filename = input_dir + '/' + filename
        image = cv2.imread(img_filename)
        trs = image_transformer.image_transformation(image)
        cv2.imwrite(output_dir + '/' + filename, trs)


# Delete the xml files into folder images of original marmot dataset.
def deleteXmlFromImages():
    dir = './Dataset/marmot_original/images'
    for filename in os.listdir(dir):
        st = str(filename)
        if st.endswith('.xml'):
            os.remove(dir + "/" + filename)

# Calc min and max size (height and width for datasets)
def calcMinMaxSize(img_dir):
    sizes = []
    for filename in os.listdir(img_dir):
        img = Image.open(img_dir + "/" + filename)
        sizes.append(img.size)
    minimum=sizes[0]
    minArea=sizes[0][0]*sizes[0][1]
    for size in sizes:
        if((size[0]*size[1])<minArea):
            minimum = size
            minArea = (size[0]*size[1])
    print('min ', minimum, 'minArea', minArea)
    max=sizes[0]
    maxArea=sizes[0][0]*sizes[0][1]
    for size in sizes:
        if((size[0]*size[1])>maxArea):
            max = size
            maxArea = (size[0]*size[1])
    print('max ', max, 'maxArea', maxArea)




if __name__ == '__main__':

    #calcMinMaxSize("./Dataset/icdar/images")
    #calcMinMaxSize("./Dataset/marmot/images")
    # deleteXmlFromImages()
    # Convert the icdar dataset.
    # deleteXmlFromImages()

    convert_icdar("./Dataset/icdar_2017/Annotations", "./Dataset/icdar_2017/Images", "./Dataset/icdar/labels",
                  "./Dataset/icdar/images", "./Dataset/icdar.names")

    # Generate test, validation and test sets for icdar.
    # Split the file randomly.
    fs = FileSplitter(1600)
    fs.split()
    # Generate the file that contains the list of the train, validation and test sets.
    # Input images in '../icdar/images', save the icdar_train.txt in the dataset folder.
    fs.get_train('icdar', '../Dataset/icdar/images', './Dataset/icdar_train.txt')
    #fs.get_train('icdar', '/content/gdrive/MyDrive/dataset/icdar', './Dataset/icdar_train.txt')
    # Input images in '../icdar/images', save the icdar_valid.txt in the dataset folder.
    #fs.get_train('icdar', '/content/gdrive/MyDrive/dataset/icdar', './Dataset/icdar_valid.txt')
    fs.get_valid('icdar', '../Dataset/icdar/images', './Dataset/icdar_valid.txt')
    # Input images in './Dataset/icdar/images', save the icdar_test.txt in the dataset folder.
    #fs.get_train('icdar', '/content/gdrive/MyDrive/dataset/icdar', './Dataset/icdar_test.txt')
    fs.get_test('icdar', '../Dataset/icdar/images', './Dataset/icdar_test.txt')

    # OPTIONAL: right know don't use these functions.
    # Transform the image in the dataset.
    # transform_dataset("./Dataset/icdar/images", "./Dataset/icdar_transformed/images")

    # Convert the marmot dataset.
    convert_marmot("./Dataset/marmot_original/labels", "./Dataset/marmot_original/images",
                   "./Dataset/marmot/labels", "./Dataset/marmot/images", "./Dataset/marmot.names")

    fs = FileSplitter(993)
    fs.split()
    # Generate the file that contains the list of the train, validation and test sets.
    # Input images in '../marmot/images', save the marmot_train.txt in the dataset folder.
    fs.get_train('marmot', './Dataset/marmot/images', './Dataset/marmot_train.txt')
    # Input images in '../marmot/images', save the marmot_valid.txt in the dataset folder.
    fs.get_valid('marmot', './Dataset/marmot/images', './Dataset/marmot_valid.txt')
    # Input images in '../marmot/images', save the marmot_test.txt in the dataset folder.
    fs.get_test('marmot', './Dataset/marmot/images', './Dataset/marmot_test.txt')
