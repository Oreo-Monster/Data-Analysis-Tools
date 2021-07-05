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
        '''
        Parameters
        --------------
        filepath: String. Path to the .dat file to be opened (includes .dat)
        label: String. A name for this object if working with a lot of them
        '''
        plt.style.use('plotstyle.mplstyle')
        self.filename = filepath
        if self.filename != None:
            self.spatialRead()
            self.row, self.col = self.findDimentions()
        self.label = label
        self.findDimentions()

    def spatialRead(self):
        '''Reads in the data using np.genfromtxt()'''
        try:
            self.data = np.genfromtxt(self.filename, float)
            self.headers = ['x', 'y', 'dR/R', 'R']
            self.header2col = {'x':0, 'y':1, 'dR/R':2, 'R':3}
        except:
            print("Could not read file, please check file path")
            return

    def findDimentions(self):
        '''Figures out how many cols and rows their are'''
        row=1
        while self.data[row, 1] == self.data[0,1]:
            row += 1

        col = self.get_num_samples()//row

        return (row, col)

    def shape(self):
        return (self.row, self.col)

    def minMax(self):
        xmin, xmax, ymin, ymax = (self.data[0,0], self.data[self.row,0],self.data[0,1], self.data[-1,1])
        return (xmin,xmax,ymin,ymax)

    def makeIM(self):
        '''Creates the image for a heat mape using dR/R, accounts for raster pattern'''
        im = self.data[:, 2].copy().reshape((self.row, self.col))
        for i in np.arange(self.row, step=2):
            im[i,:] = np.flip(im[i,:])
        im = np.flip(im)
        return im

    def xyIM(self):
        im = self.data.copy().reshape((self.row, self.col, 3))
        for i in np.arange(self.row, step=2):
            im[i,:,:] = np.flip(im[i,:,:])
        im = np.flip(im)
        return im

    def visualize(self, ax=None, cmap=palettable.scientific.sequential.Imola_20.mpl_colormap):
        '''Creates a heat map of the signal, returns the Axes object'''
        if ax == None:
            fig, ax = plt.subplots()

        ax.set_xlabel('X (um)')
        ax.set_ylabel('Y (um)')

        im = self.data[:, 2].copy().reshape((self.col, self.row))
        for i in np.arange(self.col, step=2):
            im[i,:] = np.flip(im[i,:])
        im = np.flip(im)
        bounds = self.minMax()
        ax.imshow(im, cmap=cmap, extent=bounds)

        return ax