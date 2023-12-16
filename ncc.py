import numpy as np
from scipy.interpolate import splev, splrep
import matplotlib.pyplot as plt

class NCC():
    def __init__(self, lower, middle, upper, exp, exp2=None, corridor=None):
        self.lowerSlope = lower
        self.middleSlope = middle
        self.higherSlope = upper
        self.exp = exp
        self.exp2 = exp2 if exp2 is not None else 0
        self.corridor = corridor if corridor is not None else 0

    def createArrayFromCRVSimple(self, crv_file): #when calling files, make sure to specify r'filepath'
        fid1 = open(crv_file, 'r')
        data_lines = list(fid1)
        out = [tuple(map(float, line.split(","))) for line in data_lines]
        out = np.array(out, dtype='float')
        x = out[:,0]
        y = out[:,1]
        return x,y
    
    def createArrayFromCRV(self, crv_file): #when calling files, make sure to specify r'filepath'
        with open(crv_file, 'r') as fid1:
            header = [next(fid1) for _ in range(8)]
            ptsline = header[5]
            pts = int(ptsline.split('=')[1])
            data_lines = list(fid1)
            if 'endcurve\n' in data_lines:
                data_lines.remove('endcurve\n')

        out = [tuple(map(float, line.split())) for line in data_lines]
        out = np.array(out, dtype='float')
        x = out[:,0]
        y = out[:,1]
        return x,y
    
    def createArrayFromCRVComma(self, crv_file): #when calling files, make sure to specify r'filepath'
        with open(crv_file, 'r') as fid1:
            header = [next(fid1) for _ in range(8)]
            ptsline = header[5]
            pts = int(ptsline.split('=')[1])
            data_lines = list(fid1)
            data_lines.remove('endcurve\n')

        out = [tuple(map(float, line.split(","))) for line in data_lines]
        out = np.array(out, dtype='float')
        x = out[:,0]
        y = out[:,1]
        return x,y
    
    def pruneData(self, arr, fraction):
        toe = int(len(arr)*fraction)
        return arr[toe:len(arr)-toe]
    
    def runTest(self, pruneFraction, testType, title=None):
        # x and y are experimental data
        if testType == "headlag":
            [x, y] = self.createArrayFromCRVSimple(self.corridor)
            x = self.pruneData(x, pruneFraction)
            y = self.pruneData(y, pruneFraction)
        elif testType != "eam":
            [x, y] = self.createArrayFromCRV(self.exp)
            x = self.pruneData(x, pruneFraction)
            y = self.pruneData(y, pruneFraction)
        inPointsX = []
        inPointsY = []
        outPointsX = []
        outPointsY = []
        inPoints = 0
        outPoints = 0


        if testType == "tension":

            x = list(x)
            y = list(y)

            maxIndex = y.index(max(y))

            x = x[:maxIndex+1]
            y = y[:maxIndex+1]

            dspan = [0, 15]
            lc = [self.lowerSlope*x for x in dspan]
            hc = [self.higherSlope*x for x in dspan]

            mdspan = np.linspace(0, 15, 1000)
            mc = [self.middleSlope*x for x in mdspan]

            for i in range(len(x)):
                if x[i]*self.lowerSlope <= y[i] <= x[i]*self.higherSlope:
                    inPointsX.append(x[i])
                    inPointsY.append(y[i])
                    inPoints += 1
                else:
                    outPointsX.append(x[i])
                    outPointsY.append(y[i])
                    outPoints += 1

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(x))
            
            # middle = mc[:len(inPointsY)]
            minIndex = min(len(mc), len(y))
            a = y[:minIndex]
            b = mc[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(dspan, lc, label = 'lower corridor')
            plt.plot(mdspan, mc, label = 'middle corridor')
            plt.plot(dspan, hc, label = 'higher corridor')
            plt.plot(inPointsX, inPointsY, label = 'inside points')
            plt.plot(outPointsX, outPointsY, label = 'outside points', linestyle='dotted')

            plt.legend()
            plt.title("Tension Test")
            plt.xlabel("Displacement (mm)")
            plt.ylabel("Force (N)")
            plt.show()

            return
            
            
                
        if testType == "compression":

            x = list(x)
            y = list(y)

            minIndex = y.index(min(y))

            x = x[:minIndex+1]
            y = y[:minIndex+1]

            dspan = [-15, 0]
            lc = [0, 0]
            hc = [self.higherSlope*x for x in dspan]

            mdspan = np.linspace(-15, 0, 1000)
            mc = [self.middleSlope*x for x in mdspan]

            for i in range(len(x)):
                if x[i]*self.lowerSlope >= y[i] >= x[i]*self.higherSlope:
                    inPointsX.append(x[i])
                    inPointsY.append(y[i])
                    inPoints += 1
                else:
                    outPointsX.append(x[i])
                    outPointsY.append(y[i])
                    outPoints += 1

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(x))
            
            minIndex = min(len(mc), len(y))
            a = y[:minIndex]
            b = mc[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(dspan, lc, label = 'lower corridor')
            plt.plot(mdspan, mc, label = 'middle corridor')
            plt.plot(dspan, hc, label = 'higher corridor')
            plt.plot(inPointsX, inPointsY, label = 'inside points')
            # plt.plot(outPointsX, outPointsY, label = 'outside points', linestyle='dotted')

            plt.legend()
            plt.title("Compression Test")
            plt.xlabel("Displacement (mm)")
            plt.ylabel("Force (N)")
            plt.show()

            return

        if testType == "flexion":

            # Change experimental data (rad -> angle), (Nmm -> Nm)

            tempx = [rad*57.3 for rad in x]
            tempy = [nmm/1000 for nmm in y]

            tempx = list(tempx)
            tempy = list(tempy)

            maxIndex = tempx.index(max(tempx))
            tempx = tempx[:maxIndex]
            tempy = tempy[:maxIndex]

            x = tempx
            y = tempy

            maxTime = 106
            d = np.linspace(0, maxTime, maxTime+1)
            lowM = np.zeros(maxTime+1)
            middle = np.zeros(maxTime+1)
            highM = np.zeros(maxTime+1)

            # Section 1 = [0,17]

            for i in range(18):
                highM[i] = 14.0*i/17.0

            # Section 2 = [17,75]

            for i in range(18, 76):
                highM[i] = 7.0*(i-17)/(75-17)+highM[17]

            # Section 3 = [75,79]
            for i in range(76, 80):
                highM[i] = 24.0*(i-75)/(4.0)+highM[75]

            # Section 4 = [79,107]

            for i in range(80, 107):
                highM[i] = highM[79]

            for i in range(41,107):
                lowM[i] = 18*(i-40)/(106-40)

            for i in range(len(middle)):
                middle[i] = (lowM[i]+highM[i])/2 
            

            for i in range(len(x)):

                if x[i] < 17:
                    if 0 <= y[i] <= x[i]*14.0/17:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if 17 <= x[i] < 75:
                    if max(0,18*(x[i]-40)/(106-40)) <= y[i] <= 7.0*(x[i]-17)/(75-17)+highM[17]:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if 75 <= x[i] < 79:
                    if max(0,18*(x[i]-40)/(106-40)) <= y[i] <= 24.0*(x[i]-75)/(4.0)+highM[75]:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if 79 <= x[i]:
                    
                    if 18*(x[i]-40)/(106-40) <= y[i] <= highM[79]:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(x))

            minIndex = min(len(middle), len(y))
            a = y[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(d, lowM, label = 'lower corridor')
            plt.plot(d, middle, label = 'middle corridor')
            plt.plot(d, highM, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)


            plt.legend()
            plt.title("Flexion Test")
            plt.xlabel("Moment (Nm)")
            plt.ylabel("Angle (degrees))")
            plt.show()

            return
        

        if testType == "extension":

            # Change experimental data (rad -> angle), (Nmm -> Nm)

            tempx = [rad*57.3 for rad in x]
            tempy = [nmm/1000 for nmm in y]

            tempx = list(tempx)
            tempy = list(tempy)

            maxIndex = tempx.index(min(tempx))
            tempx = tempx[:maxIndex]
            tempy = tempy[:maxIndex]

            x = tempx
            y = tempy

            maxTime = 140
            d = np.linspace(0, maxTime, maxTime+1)
            lowM = np.zeros(maxTime+1)
            middle = np.zeros(maxTime+1)
            highM = np.zeros(maxTime+1)

            # Section 1 = [0,23]

            for i in range(24):
                highM[i] = -7.0*i/23.0

            # Section 2 = [23,68]

            for i in range(24, 69):
                highM[i] = highM[23]

            # Section 3 = [68,91]

            for i in range(69, 92):
                highM[i] = -18.0*(i-68)/(56.0)+highM[68]


            # Section 4 = [91,140]

            for i in range(92, 141):
                lowM[i] = -20.0*(i-91)/(140.0-91)

            for i in range(92, 141):
                highM[i] = -18.0*(i-68)/(56.0)+highM[68]

            for i in range(len(middle)):
                middle[i] = (lowM[i]+highM[i])/2 


            # Flipping corridors
            d = -d
            d = np.flip(d)
            highM = np.flip(highM)
            middle = np.flip(middle)
            lowM = np.flip(lowM)

            for i in range(len(x)):

                if x[i] > -24:
                    if -7.0*x[i]/23.0 <= y[i] <= 0:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if -24 >= x[i] > -68:
                    if highM[maxTime-23] <= y[i] <= 0:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if -68 >= x[i] > -91:
                    if -18.0*(x[i]+68)/(-56.0)+highM[maxTime-68] <= y[i] <= 0:
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

                if -91 >= x[i]:
                    if -18.0*(x[i]+68)/(-56.0)+highM[maxTime-68] <= y[i] <= -20.0*(x[i]+91)/(-140.0+91):
                        inPointsX.append(x[i])
                        inPointsY.append(y[i])
                        inPoints += 1
                    else:
                        outPointsX.append(x[i])
                        outPointsY.append(y[i])
                        outPoints += 1
                    continue

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(x))

            minIndex = min(len(middle), len(y))
            a = y[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(d, lowM, label = 'lower corridor')
            plt.plot(d, middle, label = 'middle corridor')
            plt.plot(d, highM, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)

            plt.legend()
            plt.title("Extension Test")
            plt.xlabel("Moment (Nm)")
            plt.ylabel("Angle (degrees)")
            plt.show()

            return  


        if testType == "eam":

            [x,y] = self.createArrayFromCRVComma(self.corridor)
            maxPointX = max(x)

            spl = splrep(x[:51],y[:51])

            decreasingX = x[51:]
            decreasingY = y[51:]

            spl2 = splrep(decreasingX[::-1], decreasingY[::-1])
    
            x2 = np.arange(0, maxPointX, 1)
            y2 = splev(x2, spl)
            y3 = splev(x2, spl2)

            [ex,ey] = self.createArrayFromCRV(self.exp)
            maxPointX = max(ex)
            spl = np.polyfit(ex,ey, 10)
            ex2 = np.arange(0, maxPointX, 1)
            ey2 = np.polyval(spl, ex2)

            # inPointsX = []
            # inPointsY = []
            # outPointsX = []
            # outPointsY = []
 
            for i in range(len(ey2)):
                if y3[i] <= ey2[i] <= y2[i]:
                    inPoints += 1
                    inPointsX.append(ex2[i])
                    inPointsY.append(ey2[i])
                else:
                    outPoints += 1
                    outPointsX.append(ex2[i])
                    outPointsY.append(ey2[i])

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(ey2))
            # making middle corridor

            middle = []

            for i in range(len(x2)):
                middle.append((y2[i]+y3[i])/2)

            minIndex = min(len(middle), len(ey2))
            a = ey2[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(x2, y2, label = 'higher corridor')
            plt.plot(x2, middle, label='middle corridor')
            plt.plot(x2, y3, label = 'lower corridor')
            # plt.plot(ex2, ey2, label = 'experiment')
            # plt.plot(dspan, hc, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)
            plt.legend()
            plt.title(title)
            plt.xlabel("Time (ms)")
            plt.ylabel("Displacement (mm)")
            plt.show()

            return
        
        if testType == "headlag":

            maxPointX = max(x)

            spl = splrep(x[:75],y[:75])

            decreasingX = x[75:-1]
            decreasingY = y[75:-1]

            spl2 = splrep(decreasingX[::-1], decreasingY[::-1])
    
            x2 = np.arange(0, maxPointX, 1)
            y2 = splev(x2, spl)
            y3 = splev(x2, spl2)


            [ex,ey] = self.createArrayFromCRV(self.exp)
            maxPointX = max(ex)
            maxPointY = max(ey)

            maxPointIndex = list(ey).index(maxPointY)
            ex = ex[:maxPointIndex]
            ey = ey[:maxPointIndex]
            spl = np.polyfit(ex,ey, 10)
            ex2 = np.arange(0, maxPointX, 1)
            ey2 = np.polyval(spl, ex2)

            # inPointsX = []
            # inPointsY = []
            # outPointsX = []
            # outPointsY = []

            # print(len(y2))
            # print(len(ey2))
            # print(len(y3))
 
            for i in range(min(len(ex2), len(y2))):
                if y2[i] <= ey2[i] <= y3[i]:
                    inPoints += 1
                    inPointsX.append(ex2[i])
                    inPointsY.append(ey2[i])
                else:
                    outPoints += 1
                    outPointsX.append(ex2[i])
                    outPointsY.append(ey2[i])

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(ey2))

            # making middle corridor

            middle = []

            for i in range(len(x2)):
                middle.append((y2[i]+y3[i])/2)

            minIndex = min(len(middle), len(ey2))
            a = ey2[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)


            plt.plot(x2, y2, label = 'lower corridor')
            plt.plot(x2, middle, label='middle corridor')
            plt.plot(x2, y3, label = 'higher corridor')
            # plt.plot(ex2, ey2, label = 'experiment')
            # plt.plot(dspan, hc, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)

            plt.legend()
            plt.title(title)
            plt.xlabel("Neck Angle (degrees)")
            plt.ylabel("Head Angle (degrees)")
            plt.show()

            return
        
        if testType == "nbdl":
            [x, z] = self.createArrayFromCRV("corridors/NBDLDispCorridor.crv")

            [t, ex] = self.createArrayFromCRV(self.exp)
            [t, ez] = self.createArrayFromCRV(self.exp2)

            # ex = [40+x for x in ex]
            # ez = [150+z for z in ez]

            # plt.plot(ex, ez)
            # plt.show()

            # x = list(x)
            # z = list(z)
            # maxIndex = x.index(max(x))

            # x = x[:maxIndex]
            # z = z[:maxIndex]

        

            maxPointX = max(x)
            maxIndex = list(x).index(maxPointX)

            # print(x[maxIndex:])
            spl = np.polyfit(x[:maxIndex],z[:maxIndex], 2)

            decreasingX = x[maxIndex+1:-1]
            decreasingZ = z[maxIndex+1:-1]

            spl2 = np.polyfit(decreasingX[::-1], decreasingZ[::-1], 2)
    
            x2 = np.arange(40, maxPointX, 1)
            y2 = np.polyval(spl, x2)
            y3 = np.polyval(spl2, x2)


            # [ex,ey] = self.createArrayFromCRV(self.exp)
            maxPointX = max(ex)
            # maxPointY = max(ey)

            maxPointIndex = list(ex).index(maxPointX)
            ex = ex[:maxPointIndex]
            ez = ez[:maxPointIndex]

            spl = np.polyfit(ex, ez, 10)
            ex2 = np.arange(40, maxPointX, 1)
            ey2 = np.polyval(spl, ex2)

            # print(ey2)

            # plt.plot(ex2, ey2, label='ex')
            # plt.plot(x2, y2, label='low cor')
            # plt.plot(x2, y3, label='high cor')
            # plt.legend()
            # plt.show()

            # inPointsX = []
            # inPointsY = []
            # outPointsX = []
            # outPointsY = []

            print(len(y2))
            print(len(ey2))
            print(len(y3))

 
            for i in range(min(len(ey2), len(y2))):
                if y2[i] <= ey2[i] <= y3[i]:
                    inPoints += 1
                    inPointsX.append(ex2[i])
                    inPointsY.append(ey2[i])
                else:
                    outPoints += 1
                    outPointsX.append(ex2[i])
                    outPointsY.append(ey2[i])

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(ey2))
            # making middle corridor

            middle = []

            for i in range(len(x2)):
                middle.append((y2[i]+y3[i])/2)

            minIndex = min(len(middle), len(ey2))
            a = ey2[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(x2, y2, label = 'lower corridor')
            plt.plot(x2, middle, label='middle corridor')
            plt.plot(x2, y3, label = 'higher corridor')
            # plt.plot(ex2, ey2, label = 'experiment')
            # plt.plot(dspan, hc, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)


            plt.legend()
            plt.title(title)
            plt.xlabel("X Displacement (mm)")
            plt.ylabel("Y Displacement (mm)")
            plt.show()

            return
            
            
        if testType == "rvel":

            [x, y] = self.createArrayFromCRVComma(self.corridor)

            # [x,y] = self.createArrayFromCRVComma(self.corridor)
            maxPointX = max(x)
            maxPointY = max(y)

            maxIndex = list(x).index(maxPointX)

            # print(maxPointY)


            spl = splrep(x[:maxIndex+1],y[:maxIndex+1])

            # print(x[:100])
            # print(x[100:])

            decreasingX = x[maxIndex+1:]
            decreasingY = y[maxIndex+1:]

            spl2 = splrep(decreasingX[::-1], decreasingY[::-1])
    
            x2 = np.arange(0, maxPointX, 1)
            y2 = splev(x2, spl)
            y3 = splev(x2, spl2)

            [ex,ey] = self.createArrayFromCRV(self.exp)
            maxPointX = max(ex)
            spl = splrep(ex,ey)
            ex2 = np.arange(0, maxPointX, 1)
            ey2 = splev(ex2, spl)

            # inPointsX = []
            # inPointsY = []
            # outPointsX = []
            # outPointsY = []
 
            for i in range(len(ey2)):
                if y3[i] <= ey2[i] <= y2[i]:
                    inPoints += 1
                    inPointsX.append(ex2[i])
                    inPointsY.append(ey2[i])
                else:
                    outPoints += 1
                    outPointsX.append(ex2[i])
                    outPointsY.append(ey2[i])

            print("# points inside: ", inPoints)
            print("# points outside: ", outPoints)
            print("fraction points inside: ", inPoints/len(ey2))
            # making middle corridor

            middle = []

            for i in range(len(x2)):
                middle.append((y2[i]+y3[i])/2)

            minIndex = min(len(middle), len(ey2))
            a = ey2[:minIndex]
            b = middle[:minIndex]
            
            NCC = self.ncc(a, b)
            print("ncc: ", NCC)

            plt.plot(x2, y2, label = 'higher corridor')
            plt.plot(x2, middle, label='middle corridor')
            plt.plot(x2, y3, label = 'lower corridor')
            # plt.plot(ex2, ey2, label = 'experiment')
            # plt.plot(dspan, hc, label = 'higher corridor')
            plt.scatter(inPointsX, inPointsY, label = 'inside points', color='black', marker='.', s=10)
            plt.scatter(outPointsX, outPointsY, label = 'outside points', color='red', marker='.', s=10)

            plt.legend()
            plt.title(title)
            plt.xlabel("Time (ms)")
            plt.ylabel("Head Angular Velocity (deg/s)")
            plt.show()

            return


    def ncc(self, data0, data1):
        """
        normalized cross-correlation coefficient between two data sets

        Parameters
        ----------
        data0, data1 :  numpy arrays of same size
        """
        return (1.0/(len(data0)-1)) * np.sum(self.norm_data(data0)*self.norm_data(data1))
    
    def norm_data(self, data):
        """
        normalize data to have mean=0 and standard_deviation=1
        """
        mean_data=np.mean(data)
        std_data=np.std(data, ddof=1)
        #return (data-mean_data)/(std_data*np.sqrt(data.size-1))
        return (data-mean_data)/(std_data)

        

    