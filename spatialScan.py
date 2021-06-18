"""
Emerson Wright
MSU REU Grumstrup Group
Summer 2021
"""

from data import Data
import numpy as np
import matplotlib.pyplot as plt
import palettable


'''
Object representation of Spatial Scan data from LabView (Both SS and SO)

Uses Data class for basic data manegment using numpy

'''

class SpatialScan(Data):

    def __init__(self, filepath=None, label=""):
        self.filename = filepath
        if self.filename != None:
            self.spatialRead()
            self.row, self.col = self.findDimentions()
        self.label = label

    def spatialRead(self):
        try:
            self.data = np.genfromtxt(self.filename, float)
            self.headers = ['x', 'y', 'dR/R', 'R']
            self.header2col = {'x':0, 'y':1, 'dR/R':2, 'R':3}
        except:
            print("Could not read file, please check file path")
            return

    def findDimentions(self):
        row=1
        while self.data[row, 1] == self.data[0,1]:
            row += 1

        col = self.get_num_samples()//row

        return (row, col)

    def visualize(self, ax=None, cmap=palettable.scientific.sequential.Imola_20.mpl_colormap):
        if ax == None:
            fig, ax = plt.subplots()

        ax.set_xlabel('X (um)')
        ax.set_ylabel('Y (um)')

        im = self.data[:, 2].copy().reshape((self.row, self.col))
        for i in np.arange(self.row, step=2):
            im[i,:] = np.flip(im[i,:])
        im = np.flip(im)
        bounds = (self.data[0,0], self.data[self.row,0],self.data[0,1], self.data[-1,1])
        ax.imshow(im, cmap=cmap, extent=bounds)

        return ax