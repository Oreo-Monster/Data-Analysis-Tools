
from spatialScan import SpatialScan
import glob
import re
import numpy as np
import PIL
import io
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class SpatiallySeparated(SpatialScan):

    def mkGIF(drPATH):
        try:
            allFiles = glob.glob(drPATH+'/*.dat')
        except Exception as e:
            print(f'ERROR: Could not open directory {drPATH}')
            print(e)
            return None
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
            ax = d.visualize()
            fig = ax.figure
            str = f't = {sort[idx[i]]}ps'
            ax.text(0.8, 0.9,str, horizontalalignment='center', verticalalignment='center', transform = ax.transAxes, fontsize=20)
            im = SpatiallySeparated.fig2img(fig)
            #im = PIL.Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
            IMobjs.append(im)

        IMobjs[0].save(drPATH+'/spot.gif', format='GIF', append_images=IMobjs[1:], save_all=True, duration=500, loop=0)
        
        return dataObjs

    def fig2img(fig):
        buf = io.BytesIO()
        fig.savefig(buf)
        buf.seek(0)
        img = PIL.Image.open(buf)
        return img

    def vis3D(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(self.data[0], self.data[1], self.data[2])


