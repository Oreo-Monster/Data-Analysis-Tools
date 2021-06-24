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
            print(f'Could not read file: {self.filename}, please check file path')
            return

    def visualize(self, ax=None):
        '''Visualizes the data given and returns the axes'''
        plt.style.use('plotstyle.mplstyle')
        if ax==None:
            fig, ax = plt.subplots()

        ax.set_xlabel('Time (ps)')
        ax.set_ylabel('Delta R/R')

        ax.plot(self.data[:,0], self.data[:,1], c='black')

        self.ax = ax
        self.ax.figure.set_size_inches(7,7)
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

    def customFit(self, x0, xend, fitType='sgexp'):
        '''
        Does a single exponetiall fit bewteen x0 and xend
        Returns parms = (y0, A1, r1)
        '''
        data = self.trimData(x0, xend)
        x = data[:,0]
        y = data[:,1]
        if fitType == 'sgexp':
            p,_=optimize.curve_fit(self.sgexp, x, y)
        elif fitType == 'dbexp':
            p,_=optimize.curve_fit(self.dbexp, x, y)
        else:
            raise Exception('Invalid type for Custom Fit')
        return p
    
    def trimData(self, x0, xend):
        '''
        Trims the data to be between x0 and xend
        becareful that they are in the domain of the data
        the exact values dont need to apear
        '''
        data = self.data.copy()
        if x0 is not None and x0 > data[0,0]:
            i = 0
            while x0 > data[i,0]:
                i += 1
            data = data[i:, :]
        else:
            x0idx = np.argmax(data[:,2])
            data = data[x0idx:, :]
        if xend is not None and xend < data[-1,0]:
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

    def plotFit(self, x0 = None, xend = None, params=None, ax=None, addText=True, color='r'):
        '''
        Plots the fited curve onto the data
        Parametes
        -------------
        x0: int. If using customFit, lowerbound for the fit
        xend: int. If using customFit, upperbound for the fit
        params: tupe. Parameters of the fitted curve, use in not doing dbexp
        ax: axes to be plotted on, defaults to the axes in self.ax (created in self.visualize())
        addText: bool. if True, values of parameters will be added to the plot, if false they will be 
                       returned as a list of string (ax, params)
        color: str. Color of the fit, must be a matplotlib color
        '''
        if ax is None:
            ax = self.ax
        
        if params is None:
            params = self.params

        data = self.trimData(x0, xend)

        if len(params) == 5:
            func = self.dbexp
            pstring = [f'y0 = {params[0]:.2f}',f'A1 = {params[1]:.2f}', f'A2 = {params[2]:.2f}', fr'$\tau$1 = {params[3]:.2f}', fr'$\tau$2 = {params[4]:.2f}']
        elif len(params) == 3:
            func = self.sgexp
            pstring = [f'y0 = {params[0]:.2f}',f'A1 = {params[1]:.2f}', fr'$\tau$1 = {params[2]:.2f}']

        #Getting the x data
        x = data[:,0]
        #Plottting
        ax.plot(x, func(x, *params), c=color)
       
        #Adding all the text to the plot
        if addText:
            for i, str in enumerate(pstring):
                ax.text(0.8, 0.9-i*0.06,str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=12)
            return ax
        else:
            return ax, pstring
        
    def interactiveVis(self):
        '''
        Creates a interactive visual plot that lets you 
        select an area to be fitted with single exponetial curve
        '''
        #Getting a fresh plot
        self.visualize()
        #Need the space on the side
        self.ax.figure.set_size_inches(10,7)
        #Fitting the plot to be square and off to the side
        self.ax.set_position([0.09,0.092,0.6,0.9])
        #This object allows the user to select part of the plot to fit
        #When an area is selected, self.onSelect is run
        selector = wid.SpanSelector(self.ax, onselect=self.onSelect, direction='horizontal', useblit=True)
        #This feild stores what type of fit is used, either 'sgexp' or 'dbexp'
        #The radio buttons will change this
        self.fitType = 'sgexp'
        #Axes for the radio buttons
        rax = plt.axes([0.72, 0.84, 0.25, 0.15])
        #Creating radio buttons
        radio = wid.RadioButtons(rax, ['Single Exponetial','Double Exponetial'], [True, False], 'red')
        #Setting up the behavior for button change
        radio.on_clicked(self.typeSelect)
        #Setting the font for all the labels
        [l.set_fontsize(12) for l in radio.labels]
        #Axes to show the fit equations
        self.eqax = plt.axes([0.72, 0.675, 0.25,0.15], xticks=[], yticks=[])
        #THis feild stores the possible colors for fit
        self.c = ['red', 'blue', 'green', 'purple', 'orange']
        #Stores what fit we are on
        self.cIDX = 0
        #Axes to draw the parameters to when things are fitted
        self.legend = plt.axes([0.72, 0.09, 0.25,0.57], xticks=[], yticks=[])
        #Storing these objects so they wont be garbage collected
        self.interactives = selector, radio
        return

    def onSelect(self, xmin, xmax):
        '''This code excicutes when part of the plot is selected'''
        #Getting the fit using the selected fitType
        p = self.customFit(xmin, xmax, fitType=self.fitType)
        #Plotting the fit with the right color and storing the string returned
        _, pstring = self.plotFit(xmin, xmax, params=p, addText=False, color=self.c[self.cIDX])
        #Writes parameters to legend
        self.updateLegend(pstring)
        #Increments to the next color
        self.cIDX += 1
        return

    def typeSelect(self, fitType):
        '''Runs when the radio buttons are pressed'''
        labelDict = {'Single Exponetial':'sgexp', 'Double Exponetial':'dbexp'}
        #Stores what function should be run to add the text to the legend
        eqSTR = {'sgexp': self.sgexpSTR, 'dbexp': self.dbexpSTR}
        #Getting the right string
        fitType = labelDict[fitType]
        #Updating equation
        self.eqax.clear()
        self.eqax.set_xticks([])
        self.eqax.set_yticks([])
        #Runs the correct equation string function
        eqSTR[fitType]()
        #Sets the new fitType
        self.fitType = fitType

    def dbexpSTR(self):
        '''Writes the double exponetial to the equation box'''
        str1 = r'$y=y_{0}+A_{1}exp(\frac{-(x-x_{0})}{\tau_{1}})$'
        str2 = r'$+A_{2}exp(\frac{-(x-x_{0})}{\tau_{2}})$'
        self.eqax.text(0.075,0.6,str1, fontsize=14)
        self.eqax.text(0.325, 0.25, str2, fontsize=14)

    def sgexpSTR(self):
        '''Writes the single exponetial to the equation box'''
        str1 = r'$y=y_{0}+A_{1}exp(\frac{-(x-x_{0})}{\tau_{1}})$'
        self.eqax.text(0.075,0.4,str1, fontsize=14)
    
    def updateLegend(self, pstring):
        '''Writes the parameters to the legend when a new fit is made'''
        #Getting the text color to match fit color
        color = self.c[self.cIDX]
        #Controls where in the legend the string is drawn
        startPos = 0.95 - 0.2*(self.cIDX)
        #Loops through string list and writes each one with the correct offset
        for i, str in enumerate(pstring):
            #Makes two columns
            x = 0.05 + 0.5*(i%2)
            y = startPos-int(i/2)*0.06
            self.legend.text(x, y, str, fontsize=12, color=color)
            