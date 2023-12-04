import numpy as np
import matplotlib.pyplot as plt

def grabdata(crv_file): #when calling files, make sure to specify r'filepath'
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

def grabdata_corr(crv_file):
    with open(crv_file, 'r') as fid1:
        header = [next(fid1) for _ in range(8)]
        ptsline = header[5]
        pts = int(ptsline.split('=')[1])
        data_lines = list(fid1)
        print(data_lines)
        data_lines.remove('endcurve\t\t\t\n')

    out = [tuple(map(float, line.split())) for line in data_lines]
    out = np.array(out, dtype='float')
    x = out[:,0]
    y = out[:,1]
    return x,y

def grabdata_rect_corr(crv_file):
    with open(crv_file, 'r') as fid1:
        header = [next(fid1) for _ in range(8)]
        ptsline = header[5]
        pts = int(ptsline.split('=')[1])
        data_lines = list(fid1)
        print(data_lines)
        data_lines.remove('endcurve\n')

    out = [tuple(map(float, line.split(','))) for line in data_lines]
    out = np.array(out, dtype='float')
    x = out[:,0]
    y = out[:,1]
    return x,y


def partition(array, startDirection):
    inflectionPoints = [0]
    index = 1
    if startDirection == "i":
        while index < len(array)-1:
            p = indexDecreasing(array, index)
            print("P is", str(p))
            print("YOu have ended")
            inflectionPoints.append(p)
            index = p+1
            if (index < len(array)-1):
                p = indexIncreasing(array, index)
                inflectionPoints.append(p)
                index = p+1
            else:
                break

    elif startDirection == "d":
        while index < len(array)-1:
            p = indexIncreasing(array, index)
            inflectionPoints.append(p)
            index = p+1
            if (index < len(array)-1):
                p = indexDecreasing(array, index)
                inflectionPoints.append(p)
                index = p+1
            else:
                break
    
    return inflectionPoints


def indexDecreasing(array, startIndex):
    for i in range(startIndex, len(array)):
        print(i)
        if array[i]<=array[i-1]:
            return i
    return len(array)

def indexIncreasing(array, startIndex):
    for i in range(startIndex, len(array)):
        if array[i]>=array[i-1]:
            return i
    return len(array)


def makePlot(x, y, ip, bounds):

    xPartition = [0]*(len(ip)-1)
    yPartition = [0]*(len(ip)-1)
    
    for i in range(len(ip)-1):
        xPartition[i]=(x[ip[i]:ip[i+1]])
        yPartition[i]=(y[ip[i]:ip[i+1]])
        # plt.plot(xPartition[i], yPartition[i], label = bounds[i%3])


    # plt.legend()
    # plt.title("Tension Corridor")
    # plt.xlabel("Displacement (mm)")
    # plt.ylabel("Load (Nm)")
    # plt.show()

    return [xPartition, yPartition]


def areaBetweenCurves(top, middle, step):
    if (len(top)!=len(middle)):
        raise Exception("arrays have different lengths") 
    sum = 0
    for i in range(len(top)):
        sum += (top[i]-middle[i])
    print(type(sum))  
    return step*abs(sum)




if __name__ == "__main__":
    pass

[x, y] = grabdata("corridors/TensionCorridorFS2023.crv")
[a, b] = grabdata("6.5/6.5 Curves and Images/Tension.crv")


toe = int(len(a)/10)

a = a[toe:len(a)-toe]
b = b[toe:len(b)-toe]





factor = float(len(a)/len(x))
print(factor)

bounds = ["higher", "lower", "middle"]

ip = [0, 100, 200, 300]



[x, y] = makePlot(x, y, ip, bounds)

step = abs(x[0][1]-x[0][0])

# area = areaBetweenCurves(y[1], y[0], step)

# print(area)


higherSlope = 167.1
lowerSlope = 29.8

inPoint = 0
outPoint = 0

ex = []
ey = []

pex = []
pey = []


for i in range(len(ip)-1):
    # middleIndex = int(len(x[i])/2)
    # # print(middleIndex)
    # deltaY = y[i][middleIndex]-y[i][0]
    # deltaX = x[i][middleIndex]-x[i][0]
    # print("slope i: ", deltaY/deltaX)
    plt.plot(x[i], y[i], label = bounds[i%3])

for i in range(len(a)):
    if a[i]*lowerSlope <= b[i] <= a[i]*higherSlope:
        pex.append(a[i])
        pey.append(b[i])
        inPoint += 1
    else:
        outPoint += 1
        ex.append(a[i])
        ey.append(b[i])

print("# points inside: ", inPoint)
print("# points outside: ", outPoint)
print("fraction points inside: ", inPoint/len(a))

plt.plot(pex, pey, label = 'inside')
plt.plot(ex, ey, linestyle='dotted', label = 'outside')
plt.legend()
plt.title("Tension Corridor")
plt.xlabel("Displacement (mm)")
plt.ylabel("Load (N)")
plt.show()
















