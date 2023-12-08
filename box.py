import numpy as np
import matplotlib.pyplot as plt

class Box():
    def __init__(self, bl, tr, exp, type):
        self.bl = bl
        self.tr = tr
        self.exp = exp
        self.type = type

    def createArrayFromCRV(self, crv_file): #when calling files, make sure to specify r'filepath'
        with open(crv_file, 'r') as fid1:
            header = [next(fid1) for _ in range(8)]
            ptsline = header[5]
            pts = int(ptsline.split('=')[1])
            data_lines = list(fid1)
            data_lines.remove('endcurve\n')

        out = [tuple(map(float, line.split())) for line in data_lines]
        out = np.array(out, dtype='float')
        x = out[:,0]
        y = out[:,1]
        return x,y
    
    def findIndex(self, arr, type):
        arr = list(arr)
        if type == "min":
            return arr.index(min(arr))
        return arr.index(max(arr))
    
    def runTest(self, title, xlabel, ylabel):
        boxX = [self.bl[0], self.tr[0], self.tr[0], self.bl[0], self.bl[0]]
        boxY = [self.bl[1], self.bl[1], self.tr[1], self.tr[1], self.bl[1]]

        [time, y] = self.createArrayFromCRV(self.exp)
        index = self.findIndex(y, self.type)
        extremeTime = [time[index]]
        extremeY = [y[index]]

        if self.bl[0] <= extremeTime[0] <= self.tr[0] and self.bl[1] <= extremeY[0] <= self.tr[1]:
            print("True/In")
        else:
            print("False/Out")     

        plt.plot(boxX, boxY, label='corridor') 
        plt.plot(time, y, label= 'experiment')
        plt.scatter(extremeTime, extremeY, label='extrema', color='red')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.show()



