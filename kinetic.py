"""
Emerson Wright
MSU REU Grumstrup Group
Summer 2021
"""

from data import Data
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

'''
Object representation of Kinetic Scan data from LabView

Uses Data class for basic data manegment using numpy

'''

class KineticScan(Data):

    def __init__(self, filepath=None, label=""):
        plt.style.use('plotstyle.mplstyle')
        self.filename = filepath
        if self.filename != None:
            self.kineticRead()
            self.formatData()
        self.label = label

    def kineticRead(self):
        try:
            self.data = np.genfromtxt(self.filename, float)
            self.headers = ['time', 'dR/R', 'R']
            self.header2col = {'time':0, 'dR/R':1, 'R':2}
        except:
            print("Could not read file, please check file path")
            return

    def visualize(self, ax=None):
        if ax==None:
            fig, ax = plt.subplots()

        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Delta R/R')

        ax.plot(self.data[:,0], self.data[:,1], c='black')

        return ax

    def formatData(self):
        self.data *= -1
        dmin = -self.data[:,1].min()
        dmax = self.data[:,1].max() + dmin
        self.data[:,1] = (self.data[:,1]+dmin)/dmax
        return 

    def fitCurve(self):
        x = self.data[:,0].copy()
        y = self.data[:,1].copy()
        x0idx = self.data[:,1].argmax()
        x = x[x0idx:]
        y = y[x0idx:]
        p,_ = optimize.curve_fit(self.dbexp, x,y)
        return p


    def dbexp(self, x, y0, A1, A2, r1, r2):
        x0 = x[0]
        res = y0 + A1*np.exp((-(x-x0))/r1) + A2*np.exp((-(x-x0))/r2)
        return res

    def plotFit(self, params, ax=None):
        y0, A1, A2, r1, r2 = params
        if ax==None:
            fig, ax = plt.subplots()

        x = self.data[:,0].copy()
        x0idx = self.data[:,1].argmax()
        x = x[x0idx:]

        ax.plot(x, self.dbexp(x, y0, A1, A2, r1, r2), c='r')
        pstring = [f'y0 = {y0:.2f}',f'A1 = {A1:.2f}', f'A2 = {A2:.2f}', fr'$\tau$1 = {r1:.2f}', fr'$\tau$2 = {r1:.2f}']
        for i, str in enumerate(pstring):
            ax.text(0.8, 0.9-i*0.06,str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=12)





        return ax
        
        