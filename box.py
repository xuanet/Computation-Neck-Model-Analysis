


botLeft = [1, 1]
topRight = [2, 2]

[x, y] = "randomFile"

extremeIndex = y.index(max(y))

xval = x[extremeIndex]
yval = y[extremeIndex]

if botLeft[0] <= xval <= topRight[0] and botLeft[1] <= yval <= topRight[1]:
    print("IN")
else:
    print("OUT")