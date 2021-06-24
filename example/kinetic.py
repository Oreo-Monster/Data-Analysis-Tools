"""
Emerson Wright
MSU REU Grumstrup Group
Summer 2021
"""

from data import Data
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as wid
from scipy import optimize

'''
Object representation of Kinetic Scan data from LabView

Uses Data class for basic data manegment using numpy

Can produse double exponetial fits and visualize
'''

class KineticScan(Data):

    def __init__(self, filepath=None, label=""):
        '''
        Parameters
        --------------
        filepath: String. Path to the .dat file to be opened (includes .dat)
        label: String. A name for this object if working with a lot of them
        '''
        #Basic styling so plots arn't ugo
        plt.style.use('plotstyle.mplstyle')
        self.filename = filepath
        #Reading in the data
        if self.filename != None:
            self.kineticRead()
            self.formatData()
        self.label = label

    def kineticRead(self):
        '''Reads in the data using np.genfromtxt'''
        try:
            self.data = np.genfromtxt(self.filename, float)
            self.headers = ['time', 'dR/R', 'R']
            self.header2col = {'time':0, 'dR/R':1, 'R':2}
        except:
            print("Could not read file, please check file path")
            return

    def visualize(self, ax=None):
        '''Visualizes the data given and returns the axes'''
        if ax==None:
            fig, ax = plt.subplots()

        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Delta R/R')

        ax.plot(self.data[:,0], self.data[:,1], c='black')

        self.ax = ax
        return ax

    def formatData(self):
        '''Flips the sign of the axes and normalizes signal'''
        self.data *= -1
        dmin = -self.data[:,1].min()
        dmax = self.data[:,1].max() + dmin
        self.data[:,1] = (self.data[:,1]+dmin)/dmax
        return 

    def fitCurve(self):
        '''
        Fits a double exponetial for the whole scan
        Returns the tuple (y0, A1, A2, r1, r2)
        See dbexp for the formula used
        '''
        x = self.data[:,0].copy()
        y = self.data[:,1].copy()
        #t0 is at the max signal, dont want anything behind that
        x0idx = self.data[:,1].argmax()
        #Splitting up the data into x and y, x is time, y is singal
        x = x[x0idx:]
        y = y[x0idx:]
        #Using Scipy to fit the curve
        p,_ = optimize.curve_fit(self.dbexp, x,y)
        #Storing the params to be used for vis
        self.params = p
        return p

    def dbexp(self, x, y0, A1, A2, r1, r2):
        '''Used to fit the curve to the data, this is what scipy is optimizing'''
        x0 = x[0]
        res = y0 + A1*np.exp((-(x-x0))/r1) + A2*np.exp((-(x-x0))/r2)
        return res

    def customFit(self, x0, xend):
        '''
        Does a single exponetiall fit bewteen x0 and xend
        Returns parms = (y0, A1, r1)
        '''
        data = self.trimData(x0, xend)
        x = data[:,0]
        y = data[:,1]
        p,_=optimize.curve_fit(self.sgexp, x, y)
        return p
    
    def trimData(self, x0, xend):
        '''
        Trims the data to be between x0 and xend
        becareful that they are in the domain of the data
        the exact values dont need to apear
        '''
        data = self.data.copy()
        i = 0
        while x0 > data[i,0]:
            i += 1
        data = data[i:, :]
        i = 0
        while xend > data[i,0]:
            i += 1 
        data = data[:i, :]
        return data

    def sgexp(self, x, y0, A1, r1):
        '''Single exponetial, similar to dbexp'''
        x0 = x[0]
        res = y0 + A1*np.exp((-(x-x0))/r1)
        return res

    def plotFit(self, x0 = None, xend = None, params=None, ax=None):
        '''
        Plots the fited curve onto the data
        Parametes
        -------------
        x0: int. If using customFit, lowerbound for the fit
        xend: int. If using customFit, upperbound for the fit
        params: tupe. Parameters of the fitted curve, use in not doing dbexp
        ax: axes to be plotted on, defaults to the axes in self.ax (created in self.visualize())
        '''
        if ax is None:
            ax = self.ax
        
        if params is None:
            params = self.params

        if len(params) == 5:
            #Db exponential
            y0, A1, A2, r1, r2 = params
            #Getting the x data
            x = self.data[:,0].copy()
            x0idx = self.data[:,1].argmax()
            x = x[x0idx:]
            ax.plot(x, self.dbexp(x, y0, A1, A2, r1, r2), c='r')
            #Used to add text to plot
            pstring = [f'y0 = {y0:.2f}',f'A1 = {A1:.2f}', f'A2 = {A2:.2f}', fr'$\tau$1 = {r1:.2f}', fr'$\tau$2 = {r2:.2f}']
        else:
            #Custom Fit
            y0, A1, r1= params
            data = self.trimData(x0, xend)
            x = data[:,0]
            ax.plot(x, self.sgexp(x, y0, A1, r1), c='r')
            pstring = [f'y0 = {y0:.2f}',f'A1 = {A1:.2f}', fr'$\tau$1 = {r1:.2f}']
        
        #Adding all the text to the string
        for i, str in enumerate(pstring):
            ax.text(0.8, 0.9-i*0.06,str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=12)
        return ax
        
    def interactiveVis(self):
        '''
        Creates a interactive visual plot that lets you 
        select an area to be fitted with single exponetial curve

        NOTE: a SpanSelector object is returned, and it must be stored to not be garbage collected
        '''
        self.visualize()
        return wid.SpanSelector(self.ax, onselect=self.onSelect, direction='horizontal')


    def onSelect(self, xmin, xmax):
        '''This code excicutes when part of the plot is selected'''
        p = self.customFit(xmin, xmax)
        self.plotFit(xmin, xmax, p)  
        