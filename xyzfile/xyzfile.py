import re
import numpy as np

class XYZFile(object):


    def __init__(self, filename):
        self.fhandle = open(filename, 'r')
        self.length = int(self.fhandle.readline())

        # element info
        self.elements = ['placeholder']*self.length
        self.get_elements(filename)

        # xyz data into flatten numpy array
        self.xyz = np.empty((self.length*3), dtype=float)
        self.load_next_frame(is_first = True)

    def __iter__(self):
        return self

    def __next__(self):
        self.load_next_frame()
        return self.xyz

    def get_elements(self, filename):
        """
        obtains element info from only the first frame
        """
        with open(filename) as xyzfile:
            head = [next(xyzfile) for x in range(self.length+2)][2:]
            for ii in range(self.length):
                self.elements[ii] = re.split(' +', head[ii].strip())[0]

    def load_next_frame(self, is_first = False):
        exists = self.fhandle.readline()
        if len(exists) == 0:
            raise StopIteration()
        if not is_first:
            self.fhandle.readline()

        for i in range(self.length):
            parts = re.split(' +', self.fhandle.readline().strip())
            self.xyz[i*3:i*3+3] = parts[1:]
