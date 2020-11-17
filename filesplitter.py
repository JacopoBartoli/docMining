# !!! Need to change this file.
import numpy as np


class FileSplitter:
    def __init__(self, dataset_size):
        # Each array contains the indices of the element of the validation and the train and test sets.
        self.train_set = []
        self.valid_set = []
        self.test_set = []
        # Number of element contained in the dataset.
        self.dataset_size = dataset_size

    # Divide randomly the dataset.
    def split(self, train_percentage=80, test_percentage=10):
        # Generate randomly the validation, test and train sets.
        # Generate sizes of the sets. Right now the percentages are T-V-T80-10-10.
        train_size = int((self.dataset_size*train_percentage)/100)
        test_size = int((self.dataset_size*test_percentage)/100)
        valid_size = self.dataset_size-train_size-test_size
        # Generate randomly the train
        self.train_set = np.random.random_integers(0, self.dataset_size-1, size=int(train_size))

        # Generate and insert the elements in the test set.
        for i in range(0, test_size):
            rand = np.random.random_integers(0, self.dataset_size-1, size=1)
            if rand not in self.train_set:
                self.test_set.append(rand)

        # Generate and insert the elements in the validation set.
        for i in range(0, valid_size):
            rand = np.random.random_integers(0, self.dataset_size-1, size=1)
            if (rand not in self.train_set) and (rand not in self.test_set):
                self.valid_set.append(rand)

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
            # Add the correct string format.
            """
            x=0
            for filename in in_path and x<self.train_set:
                out.write(in_path + '/' + filename)
                x=x+1
                """
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
            """
            x = 0
            for filename in in_path and x < self.valid_set:
                out.write(in_path + '/' + filename)
                x = x + 1
                """
        out.close()
        return self.valid_set

    # Create the .txt file that contains the name of the test files.
    # in_path: path where the image files can be found.
    # out_path: path where the .txt should be saved.
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
            """
            x = 0
            for filename in in_path and x < self.test_set:
                out.write(in_path + '/' + filename)
                x = x + 1
            """
        out.close()
        return self.test_set

