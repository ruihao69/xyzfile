import re
import numpy as np

class XYZFile(object):


    def __init__(self, filename):
        self.fhandle = open(filename, 'r')
        self.length = int(self.fhandle.readline())
        self.data = np.empty((self.length*3), dtype=float)
        self.load_next_frame(is_first = True)

    def __iter__(self):
        return self

    def __next__(self):
        self.load_next_frame()
        return self.data

    def load_next_frame(self, is_first = False):
        exists = self.fhandle.readline()
        if len(exists) == 0:
            raise StopIteration()
        if not is_first:
            self.fhandle.readline()

        for i in range(self.length):
            parts = re.split(' +', self.fhandle.readline().strip())
            self.data[i*3:i*3+3] = parts[1:]
