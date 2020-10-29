# !!! Need to change this file.
import numpy as np


class FileSplitter:
    def __init__(self, dataset_size):
        # Indices of the element of the validation and the train set
        self.train_set = []
        self.valid_set = []
        self.dataset_size = dataset_size

    def split(self, train_percentage=20):
        train_size = self.dataset_size/train_percentage
        valid_size = self.dataset_size-train_size
        self.train_set = np.random.random_integers(0, 1599, size=int(train_size))
        for i in range(0, self.dataset_size):
            if i not in self.train_set:
                self.valid_set.append(i)
        self.get_train()
        self.get_valid()

    def get_train(self):
        out = open('./Dataset/icdar_train.txt', "w+")
        for i in self.train_set:
            if i >= 1000:
                out.write('../icdar/images/train/POD_' + str(i) + '.jpg' + '\n')
            elif i >= 100:
                out.write('../icdar/images/train/POD_0' + str(i) + '.jpg' + '\n')
            elif i >= 10:
                out.write('../icdar/images/train/POD_00' + str(i) + '.jpg' + '\n')
            elif i < 10:
                out.write('../icdar/images/train/POD_000' + str(i) + 'jpg' + '\n')
        out.close()
        return self.train_set

    def get_valid(self):
        out = open('./Dataset/icdar_valid.txt', "w+")
        for i in self.valid_set:
            if i >= 1000:
                out.write('../icdar/images/train/POD_' + str(i) + '.jpg' + '\n')
            elif i >= 100:
                out.write('../icdar/images/train/POD_0' + str(i) + '.jpg' + '\n')
            elif i >= 10:
                out.write('../icdar/images/train/POD_00' + str(i) + '.jpg' + '\n')
            elif i < 10:
                out.write('../icdar/images/train/POD_000' + str(i) + 'jpg' + '\n')
        out.close()
        return self.valid_set


