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


[a, b] = grabdata("FlexionCorridorFS2023.crv")

toe = int(len(a)/10)

a = a[toe:len(a)-toe]
b = b[toe:len(b)-toe]

maxTime = 140
d = np.linspace(0, 106, 107)
lowM = np.zeros(107)
highM = np.zeros(107)



# Section 1 = [0,23]

for i in range(17):
    highM[i] = 14.0/17*i


# Section 2 = [23,68]

for i in range(17, 40):
    highM[i] = 7.0/(75-17)*(i-18)+14

# Section 3 = [68,91]

for i in range(40, 75):
    highM[i] = 7.0/(75-17)*(i-17)+14
    lowM[i] = 18.0/(106-40)*(i-40)


# Section 4 = [91,140]

for i in range(75, 79):
    highM[i] = (45-21)/(4.0)*(i-75)+21
    lowM[i] = 18.0/(106-40)*(i-40)


for i in range(79, 107):
    highM[i] = 45
    lowM[i] = 18.0/(106-40)*(i-40)






# middle corridor

middle = np.linspace(0, 106, 107)
for i in range(len(middle)):
    middle[i] = (lowM[i]+highM[i])/2

plt.plot(d, lowM)
plt.plot(d, highM)
plt.plot(d, middle)
# plt.plot(a, b)
plt.show()


# calculating % inside corridors

inPoints = 0
outPoints = 0

a = -d
b = middle

ex = []
ey = []

for i in range(len(a)):
    current = a[i]
    currentY = b[i]
    if -23<=current<=0:
        if 0>=currentY>=(-7/-23.0)*current:
            inPoints += 1
            ex.append(current)
            ex.append(currentY)
            continue
        outPoints += 1
        continue
    if -68<=current<=-23:
        if 0>=currentY>=-7:
            inPoints += 1
            ex.append(current)
            ex.append(currentY)
            continue
        outPoints += 1
        continue
    if -91<=current<=-68:
        if 0>=currentY>=-7+(-18.0/(-124+68))*(current+68):
            inPoints += 1
            ex.append(current)
            ex.append(currentY)
            continue
        outPoints += 1
        continue
    if (-20.0/(-140+91))*(current+91)>=currentY>=-7+(-18.0/(-124+68))*(current+68):
        inPoints += 1
        ex.append(current)
        ex.append(currentY)
        continue
    else:
        outPoints += 1
        print(current)
    continue




print(inPoints)
print(inPoints/len(a))
        
