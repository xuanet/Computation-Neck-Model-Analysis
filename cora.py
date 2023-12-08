import numpy as np
import matplotlib.pyplot as plt

def norm_data(data):
    """
    normalize data to have mean=0 and standard_deviation=1
    """
    mean_data=np.mean(data)
    std_data=np.std(data, ddof=1)
    #return (data-mean_data)/(std_data*np.sqrt(data.size-1))
    return (data-mean_data)/(std_data)


def ncc(data0, data1):
    """
    normalized cross-correlation coefficient between two data sets

    Parameters
    ----------
    data0, data1 :  numpy arrays of same size
    """
    print(data0.size)
    return (1.0/(data0.size-1)) * np.sum(norm_data(data0)*norm_data(data1))

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


[x, y] = grabdata("corridors/TensionCorridorFS2023.crv")
[a, b] = grabdata("6.5/6.5 Curves and Images/Tension.crv")

toe = int(len(a)/10)

a = a[toe:len(a)-toe]
b = b[toe:len(b)-toe]

ip = [0, 100, 200, 300]

higherSlope = 167.1
lowerSlope = 29.8
middleSlope = 98.5

middleCorridor = middleSlope*a

randArray = np.random.rand(800)

correlation = np.correlate(b, middleCorridor, mode='same')

print(b)
print(middleCorridor)
print(correlation)


print(len(correlation))


corx = np.linspace(-max(a)/2, max(a)/2, len(correlation))

# plt.plot(a, middleCorridor, label='corridor')
# plt.plot(a, b, label='ex')
plt.plot(corx, correlation, label='correlation')
plt.legend()
plt.show()

NCC = ncc(middleCorridor, b)

print("ncc: ", NCC)

print(len(middleCorridor))
print(len(b))
