import numpy as np
import matplotlib.pyplot as plt

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

plt.plot(d, lowM)
plt.plot(d, highM)
plt.plot(d, middle)

plt.show()