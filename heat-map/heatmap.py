import numpy as np
import matplotlib.pyplot as plt

class HeatMap:
    def __init__(self):
        plt.ion()
        self.r_ = 2  # matrix rows
        self.c_ = 2  # matrix cols
        self.h_ = 1  # max energy per cell
        self.m_ = self.h_ / 2.  # mid energy per cell
        self.totalE = self.h_ * (self.r_ + self.c_)
        self.downResVec = [([1, 1]), ([1, 2])]
        self.upResVec = [([2, 1]), ([2, 2])]
        self.init_heatmap()
        # self.show_heatmap(2)

    def show_heatmap(self, wait):
        im = plt.imshow(self.responseVectors, cmap=plt.cm.coolwarm, interpolation='none')
        plt.colorbar(im)
        plt.show()
        plt.pause(wait)
        plt.close()

    def init_heatmap(self):
        self.responseVectors = np.full((2 + self.r_, 2 + self.c_), self.m_)
        self.responseVectors[0] = np.arange(.1, .4, .1)
        self.responseVectors[1][0] = .4
        self.responseVectors[1][-1] = 1
        self.responseVectors[-1] = np.arange(.6, 1, .1)

    def visualize_ratio(self, bass, treble, wait=1):
        # print('{} : {}'.format(bass, treble))
        per_bass_cell_energy = (bass * self.totalE) / len(self.downResVec)
        per_treble_cell_energy = (treble * self.totalE) / len(self.upResVec)
        self.responseVectors[self.downResVec] = per_bass_cell_energy
        self.responseVectors[self.upResVec] = per_treble_cell_energy
        self.show_heatmap(wait)


if __name__ == '__main__':
    hm = HeatMap()
    hm.visualize_ratio(0.6, 0.4)
    hm.visualize_ratio(0.5, 0.5)
    hm.visualize_ratio(0.4, 0.6)

