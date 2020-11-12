import xml.etree.ElementTree as et
import os
from rectangle import Rectangle
from filesplitter import FileSplitter
from PIL import Image
import cv2
import image_transformer


def create_rectangle(points, img_width=1, img_height=1):
    # Create a bounding box in darknet format.

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
    # Get the list of all the classes of the ICDAR dataset.
    class_dict = {}
    index = 0
    for filename in os.listdir(dir_path):
        tree = et.parse(dir_path + '/' + filename)
        root = tree.getroot()
        for child in root:
            if child.tag not in class_dict:
                class_dict[child.tag] = index
                index = index + 1
    return class_dict


def save_classes(classes, path):
    # Store all the classes in a file
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
    print(class_dict)
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


def convert_train():
    # Convert unlabeled images in Darknet format.

    # Path of the folder which contains test images.
    in_test_dir = "./Dataset/icdar_2017/other"
    # Path of the folder which will contains test images.
    out_test_dir = "./Dataset/icdar/test"

    for filename in os.listdir(in_test_dir):
        img_filename = in_test_dir + '/' + filename
        img = Image.open(img_filename)
        img.save(out_test_dir + '/' + filename.replace('.bmp', '.jpg'))


def transform_training_set():
    # Transform the image in the black and white one.
    # Path of the train set directory.
    train_dir = "./Dataset/icdar/images"
    for filename in os.listdir(train_dir):
        img_filename = train_dir + '/' + filename
        image = cv2.imread('./Dataset/icdar/images/POD_0067.jpg')
        trsf = image_transformer.image_trasformation(image)
        cv2.imwrite(train_dir + '/' + filename.replace('.bmp', '.jpg'), trsf)


if __name__ == '__main__':
    icdar_to_darknet()
    fs = FileSplitter(1600)
    fs.split()
    convert_train()
