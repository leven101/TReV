import matplotlib.pyplot as plt
import numpy as np

plt.ion()

a = np.array([[5, 5],
     [5, 5]])
plt.imshow(a, cmap='hot', interpolation='nearest')
plt.show()
plt.pause(1)

for i in range(4):
    if i == 0:
        a[0][0] = 6
        a[0][1] = 4
        a[1][0] = 4
        a[1][1] = 5
    elif i == 1:
        a[0][0] = 4
        a[0][1] = 6
        a[1][0] = 4
        a[1][1] = 5
    elif i == 2:
        a[0][0] = 5
        a[0][1] = 4
        a[1][0] = 4
        a[1][1] = 6
    elif i == 3:
        a[0][0] = 4
        a[0][1] = 5
        a[1][0] = 6
        a[1][1] = 4
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()
    plt.pause(0.5)