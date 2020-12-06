import numpy as np
import os
import xml.etree.ElementTree as Et

class FileSplitter:
    def __init__(self, dataset_size):
        # Each array contains the indices of the element of the validation and the train and test sets.
        self.train_set = []
        self.valid_set = []
        self.test_set = []
        # Number of element contained in the dataset.
        self.dataset_size = dataset_size

    # Divide randomly the dataset
    def split(self,  train_percentage=80, test_percentage=10):

            # Generate randomly the validation, test and train sets.
            # Generate sizes of the sets. Right now the percentages are T-V-T80-10-10.
            train_size = int((self.dataset_size*train_percentage)/100)
            test_size = int((self.dataset_size*test_percentage)/100)
            valid_size = self.dataset_size-train_size-test_size
            # Generate randomly the train

            self.train_set = np.random.random_integers(0, self.dataset_size - 1, size=int(train_size))
            #self.train_set = np.random.random_integers(0, self.dataset_size-1, size=int(train_size))

            # Generate and insert the elements in the test set.
            for i in range(0, test_size):
                rand = np.random.random_integers(0, self.dataset_size-1)
                if rand not in self.train_set:
                    self.test_set.append(rand)

            # Generate and insert the elements in the validation set.
            for i in range(0, valid_size):
                rand = np.random.random_integers(0, self.dataset_size-1)
                if (rand not in self.train_set) and (rand not in self.test_set):
                    self.valid_set.append(rand)

    #Divide randomly dataset with percentage with or without table
    def splitInPercentage(self,  dataset, train_percentage=80, test_percentage=10):

        train_size = int((self.dataset_size * train_percentage) / 100)
        test_size = int((self.dataset_size * test_percentage) / 100)
        valid_size = self.dataset_size - train_size - test_size
        trainTable = []
        trainNoTable = []
        validTable = []
        validNoTable = []
        allTable = []
        allNoTAble = []
        percentageTable = 0
        percentageNoTable = 0
        if dataset == 'icdar':
            percentageTable = 34
            percentageNoTable = 66
            # Scroll through all the files and split between tables and non-tables
            for filename in os.listdir("./Dataset/icdar_2017/Annotations"):
                tree = Et.parse("./Dataset/icdar_2017/Annotations/" + filename)
                root = tree.getroot()
                # Storing the corresponding image to the file.
                isTable = False
                for child in root:
                    if child.tag == 'tableRegion':
                        isTable = True
                if (isTable == True):
                    allTable.append(filename.replace('.xml', '.txt'))
                elif (isTable == False):
                    allNoTAble.append(filename.replace('.xml','.txt'))
        elif dataset == 'marmot':
            percentageTable = 49
            percentageNoTable = 51
            # Scroll through all the files and split between tables and non-tables
            for filename in os.listdir("./Dataset/marmot_original/labels"):
                tree = Et.parse("./Dataset/marmot_original/labels/" + filename)
                root = tree.getroot()
                # Storing the corresponding image to the file.
                isTable = False
                for child in root:
                    for item in child:
                        st = str(item.attrib)
                        if st == "{'Label': 'Table'}":
                            isTable = True
                if (isTable == True):
                    allTable.append(filename.replace('.xml', '.txt'))
                elif (isTable == False):
                    allNoTAble.append(filename.replace('.xml', '.txt'))

        trainTableSize = int((train_size * percentageTable) / 100)
        trainNoTableSize = int((train_size * percentageNoTable) / 100)
        validTableSize = int((valid_size * percentageTable) / 100)
        validNoTableSize = int((valid_size * percentageNoTable) / 100)


        np.random.shuffle(allTable)
        np.random.shuffle(allNoTAble)

        # Create two train set, one with tables and one without tables
        for i in range(0, trainTableSize):
            trainTable.append(allTable.pop(0))
        for i in range(0, trainNoTableSize):
            trainTable.append(allNoTAble.pop(0))

        # Create two valid set, one with tables and one without tables
        for i in range(0, validTableSize):
                validTable.append(allTable.pop(0))
        for i in range(0, validNoTableSize):
                 validNoTable.append(allNoTAble.pop(0))

        # Create the test set with the remaining data
        self.test_set = []
        self.test_set.extend(allTable)
        self.test_set.extend(allNoTAble)

        # Join the train and valid set
        trainTable.extend(trainNoTable)
        self.train_set = trainTable
        validTable.extend(validNoTable)
        self.valid_set = validTable

        # Shuffle sets
        np.random.shuffle(self.train_set)
        np.random.shuffle(self.valid_set)
        np.random.shuffle(self.test_set)



    # Create the .txt file that contains the name of the train files.
    # in_path: path where the image files can be found.
    # out_path: path where the .txt should be saved.
    def get_train(self, dataset, in_path, out_path):
        out = open(out_path, "w+")
        if dataset == 'icdar':
            for i in self.train_set:
                if i >= 1000:
                    out.write(in_path+'/POD_' + str(i) + '.jpg' + '\n')
                elif i >= 100:
                    out.write(in_path+'/POD_0' + str(i) + '.jpg' + '\n')
                elif i >= 10:
                    out.write(in_path+'/POD_00' + str(i) + '.jpg' + '\n')
                elif i < 10:
                    out.write(in_path+'/POD_000' + str(i) + '.jpg' + '\n')

        elif dataset == 'marmot':
            marmot_images = []
            for filename in os.listdir("./Dataset/marmot/images"):
                marmot_images.append(filename)
            for i in self.train_set:
                out.write(in_path + '/' + str(marmot_images[i]) + '\n')
        out.close()
        return self.train_set

        # Create the .txt file that contains the name of the train files.
        # in_path: path where the image files can be found.
        # out_path: path where the .txt should be saved.
    def get_trainInPercentage(self, in_path, out_path):
            out = open(out_path, "w+")
            for i in self.train_set:
                i = str(i)
                i = i.replace('.txt', '.jpg')
                out.write(in_path + '/' + i + '\n')
            out.close()
            return self.train_set

    # Create the .txt file that contains the name of the validation files.
    # in_path: path where the image files can be found.
    # out_path: path where the .txt should be saved.
    def get_valid(self, dataset, in_path, out_path):
        out = open(out_path, "w+")
        if dataset == 'icdar':
            for i in self.valid_set:
                if i >= 1000:
                    out.write(in_path+'/POD_' + str(i) + '.jpg' + '\n')
                elif i >= 100:
                    out.write(in_path+'/POD_0' + str(i) + '.jpg' + '\n')
                elif i >= 10:
                    out.write(in_path+'/POD_00' + str(i) + '.jpg' + '\n')
                elif i < 10:
                    out.write(in_path+'/POD_000' + str(i) + '.jpg' + '\n')
        elif dataset == 'marmot':
            marmot_images = []
            for filename in os.listdir("./Dataset/marmot/images"):
                marmot_images.append(filename)
            for i in self.valid_set:
                out.write(in_path + '/' + str(marmot_images[i])  + '\n')
        out.close()
        return self.valid_set


    def get_validInPercentage(self, in_path, out_path):
            out = open(out_path, "w+")
            for i in self.valid_set:
                i = str(i)
                i = i.replace('.txt', '.jpg')
                out.write(in_path + '/' + i + '\n')
            out.close()
            return self.valid_set


    # Create the .txt file that contains the name of the test files.
    # in_path: path where the image files can be found.
    # out_path: path where the .txt should be saved.
    # in_path refers to the path that image will have when used by the darknet script. Need to adjust this name.
    def get_test(self, dataset, in_path, out_path):
        out = open(out_path, "w+")
        if dataset == 'icdar':
            for i in self.test_set:
                if i >= 1000:
                    out.write(in_path+'/POD_' + str(i) + '.jpg' + '\n')
                elif i >= 100:
                    out.write(in_path+'/POD_0' + str(i) + '.jpg' + '\n')
                elif i >= 10:
                    out.write(in_path+'/POD_00' + str(i) + '.jpg' + '\n')
                elif i < 10:
                    out.write(in_path+'/POD_000' + str(i) + '.jpg' + '\n')
        elif dataset == 'marmot':
            marmot_images = []
            for filename in os.listdir("./Dataset/marmot/images"):
                marmot_images.append(filename)
            for i in self.test_set:
                out.write(in_path + '/' + str(marmot_images[i]) + '\n')
        out.close()
        return self.test_set


    def get_testInPercentage(self, in_path, out_path):
        out = open(out_path, "w+")
        for i in self.test_set:
            i = str(i)
            i = i.replace('.txt', '.jpg')
            out.write(in_path + '/' + i + '\n')
        out.close()
        return self.test_set