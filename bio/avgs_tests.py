import numpy as np


def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[N:] - cumsum[:-N]) / float(N)


def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def compute_centered(x, n=4):
    x_avg = np.zeros(x.size)
    for i in range(x.size):
        ## get sum of pre context
        prev_beg = -1 if i == 0 else 0 if i < n else i - n
        # prev_end = -1 if i == 0 else i - 1 if i - 1 >= 0 else 0  # actual index end
        prev_end = -1 if i == 0 else i if i > 0 else 0  # non-inclusive end
        prev_sum = np.sum(x[prev_beg:prev_end], dtype=float)

        ## get sum of post context
        post_beg = -1 if i >= x.size - 1 else i + 1 if i + 1 < x.size - 1 else x.size - 1
        # post_end = -1 if i >= x.size - 1 else x.size - 1 if i + n >= x.size else i + n # actual index end
        post_end = -1 if i >= x.size - 1 else x.size if i + n >= x.size else i + n + 1  # non-inclusive end
        post_sum = np.sum(x[post_beg:post_end], dtype=float)

        ## compute average
        avg = (prev_sum + post_sum) / ((prev_end - prev_beg) + (post_end - post_beg))

        print('current index: {}'.format(i))
        print('\tprev start: {}\tend: {}\tsum: {}'.format(prev_beg, prev_end, prev_sum))
        print('\tpost start: {}\tend: {}\tsum: {}'.format(post_beg, post_end, post_sum))
        print('\taverage: {}'.format(avg))

        ## subtract from current value
        x_avg[i] = x[i] - avg
    return x_avg


x = np.arange(10)
x_avg = compute_centered(x)
print(x)
print(x_avg)

# n_x = running_mean(x, 8)
# print(n_x)
#
# n_x = moving_average(x, 8)
# print(n_x)
