
from spatialScan import SpatialScan
import glob
import re
import numpy as np
import PIL
import io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import interpolate


class SpatiallySeparated(SpatialScan):

    def mkGIF(drPATH, destPATH = "", name='spot', verbose=False):
        '''
        This is a weird function, should really be made a method
        But I don't want to break any code
        Parameters:
        -------------------
        drPATH: str. Path to the directory containing all input files
            NOTE they must have a time stamp from the autogalvo in the name
        destPATH: str. File path to where the GIF should be stored (defaults to drPATH)
        name: str. Name of the GIF file (defaults to 'spot')
        verbose: bool. If True, print out file name as they get plotted
        '''
        if len(destPATH) == 0:
            destPATH = drPATH

        #Getting all the files
        try:
            allFiles = glob.glob(drPATH+'/*.dat')
        except Exception as e:
            print(f'ERROR: Could not open directory {drPATH}')
            print(e)
            return None
        #Creating all the objects
        dataObjs = []
        sort = []
        for fpath in allFiles:
            try:
                #Getting the file name and trimming .dat extention and /
                fname = re.search('[\\\/](R\d_)?D\d-.+', fpath)[0][1:-4]
            except:
                print(f'ERROR: Could not open {fpath}: Bad re exspression')
                continue
                
            try:
                if 'GV' in fname:
                    data = SpatiallySeparated(filepath=fpath, label=fname)
                    dataObjs.append(data)
                    #The slice strips off the t-
                    t = re.search('t-\d+', fname)[0][2:]
                    sort.append(int(t))
            except Exception as e:
                print(f'ERROR: Could not read {fpath}: {e.__class__}')
                print(e)

        #Sorting to the correct order
        dataObjs = np.array(dataObjs)
        sort = np.array(sort)
        idx = np.argsort(sort)
        dataObjs = dataObjs[idx]
        IMobjs = []
        for i, d in enumerate(dataObjs):
            if verbose:
                print(f'{name}-{i}')
            ax = d.visualize(cmap='inferno')
            fig = ax.figure
            #Adding timestamp to plots
            str = f't = {sort[idx[i]]}ps'
            ax.text(0.8, 0.9,str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=20)
            #Making a PIL Image object of the figure
            im = SpatiallySeparated.fig2img(fig)
            plt.close()
            IMobjs.append(im)

        try:
            #Saving allt the PIL images into one gif
            IMobjs[0].save(f'{destPATH}/{name}.gif', format='GIF', append_images=IMobjs[1:], save_all=True, duration=500, loop=0)
        except Exception as e:
            print(f'ERROR: could not open destination PATH:')
            print(e)
        
        return dataObjs

    def fig2img(fig):
        '''Fancy code to not have to save the plt as a file first'''
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = PIL.Image.open(buf)
        return img

    def vis3D(self, Rmax=0):
        ''''Incomplete, do not use. Trying to visualize the spot diffusion 3D'''
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        xmin, xmax, ymin, ymax = self.minMax()
        dif = (xmax-xmin, ymax-ymin)
        x = np.arange(xmin, xmax, dif[0]/self.col)
        y = np.arange(ymin, ymax, dif[0]/self.row)
        x, y = np.meshgrid(x,y)
        z = self.makeIM()
        z *= -1
        if Rmax == 0:
            z /= z.max()
        else:
            z /= Rmax
        ax.plot_surface(x, y, z, cmap='inferno', vmin=0, vmax=1)
        ax.set_xlabel(r'X ($\mu$m)', labelpad=15)
        ax.set_ylabel(r'Y ($\mu$m)', labelpad=15)
        ax.set_zlabel(r'$\Delta$R/R', labelpad=15)
        ax.set_zbound(0,1.0)

        return ax
    
    def mkGIF3D(drPATH, destPATH = "", name='spot', verbose=False):
            '''
            This is a weird function, should really be made a method
            But I don't want to break any code
            Parameters:
            -------------------
            drPATH: str. Path to the directory containing all input files
                NOTE they must have a time stamp from the autogalvo in the name
            destPATH: str. File path to where the GIF should be stored (defaults to drPATH)
            name: str. Name of the GIF file (defaults to 'spot')
            verbose: bool. If True, print out file name as they get plotted
            '''
            if len(destPATH) == 0:
                destPATH = drPATH

            #Getting all the files
            try:
                allFiles = glob.glob(drPATH+'/*.dat')
            except Exception as e:
                print(f'ERROR: Could not open directory {drPATH}')
                print(e)
                return None
            #Creating all the objects
            dataObjs = []
            sort = []
            for fpath in allFiles:
                try:
                    #Getting the file name and trimming .dat extention and /
                    fname = re.search('[\\\/](R\d_)?D\d-.+', fpath)[0][1:-4]
                except:
                    print(f'ERROR: Could not open {fpath}: Bad re exspression')
                    continue
                    
                try:
                    if 'GV' in fname:
                        data = SpatiallySeparated(filepath=fpath, label=fname)
                        dataObjs.append(data)
                        #The slice strips off the t-
                        t = re.search('t-\d+', fname)[0][2:]
                        sort.append(int(t))
                except Exception as e:
                    print(f'ERROR: Could not read {fpath}: {e.__class__}')
                    print(e)

            #Sorting to the correct order
            dataObjs = np.array(dataObjs)
            sort = np.array(sort)
            idx = np.argsort(sort)
            dataObjs = dataObjs[idx]
            IMobjs = []

            Rmax = -(dataObjs[0].data[:,2].min())

            for i, d in enumerate(dataObjs):
                if verbose:
                    print(f'{name}-{i}')
                ax = d.vis3D(Rmax=Rmax)
                fig = ax.figure
                #Adding timestamp to plots
                str = f't = {sort[idx[i]]}ps'
                ax.text(0.8, 0.9, 0.9, str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=20)
            
                #Making a PIL Image object of the figure
                im = SpatiallySeparated.fig2img(fig)
                plt.close()
                IMobjs.append(im)

            try:
                #Saving allt the PIL images into one gif
                IMobjs[0].save(f'{destPATH}/{name}.gif', format='GIF', append_images=IMobjs[1:], save_all=True, duration=500, loop=0)
            except Exception as e:
                print(f'ERROR: could not open destination PATH:')
                print(e)
            
            return dataObjs

    def threshold(self, percentMax):
        Rmax = np.max((self.data[:,2]**2)**0.5)
        tresh = percentMax * Rmax
        for dp, i in enumerate(self.data[:,2]):
            if ((dp)**2)**0.5 < tresh:
                self.data[i,2] = 0