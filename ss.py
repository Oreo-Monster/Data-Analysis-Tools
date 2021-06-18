
from spatialScan import SpatialScan
import glob
import re
import numpy as np

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

        return dataObjs



