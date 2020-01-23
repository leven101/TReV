import numpy as np
import matplotlib.pyplot as plt

r_ = 2  # matrix rows
c_ = 2  # matrix cols
l_ = 0  # low energy
h_ = 10  # high energy
m_ = h_ / 2  # mid energy
plt.ion()


def select_next_cell():
    row = np.random.randint(1, r_+1)
    col = np.random.randint(1, c_+1)
    return row, col


def show_heatmap(data, wait):
    im = plt.imshow(data, cmap=plt.cm.coolwarm, interpolation='none')
    plt.colorbar(im)
    plt.show()
    plt.pause(wait)
    plt.close()


def init_erv():
    m = np.full((2+r_, 2+c_), m_)
    m[0] = np.arange(4)
    m[1][0] = 4
    m[1][-1] = 10
    m[-1] = np.arange(6, 10)
    return m


erv = init_erv()
print(erv)
show_heatmap(erv, 1.0)

for _ in range(10):
    cell = select_next_cell()
    print('\n\n\nSelected cell {}'.format(cell))
    while erv[cell] != h_:
        erv[cell] += 1
        for i in range(1, r_+1):
            for j in range(1, c_+1):
                if (i, j) != cell and erv[(i, j)] > 0:
                    erv[(i, j)] -= 1
        show_heatmap(erv, 0.001)
        print(erv)


