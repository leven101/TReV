import os
import csv
import numpy as np
import logging
from collections import defaultdict


def setup_logging():
    log_format = '%(asctime)s %(levelname)-7s %(name)-20s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)


def load_esense_csv(path):
    logging.info('Processing file {}'.format(path))
    exp_name = None
    data_map = defaultdict(lambda: [])
    headers = None
    with open(path, 'r') as fin:
        fcsv = csv.reader(fin, delimiter=';')
        for i, row in enumerate(fcsv):
            if i == 1:
                exp_name = row[1]
            elif i == 24:
                headers = row
            elif i > 24:
                for j, header in enumerate(headers):
                    data_map[header].append(row[j])
    return exp_name, data_map


def avg_scr_peaks(gsr_map, n=4):
    x = np.array(gsr_map['MICROSIEMENS'], dtype=float)
    x_avg = np.zeros(x.size)
    for i in range(x.size):
        # get sum of pre context
        prev_beg = -1 if i == 0 else 0 if i < n else i - n
        prev_end = -1 if i == 0 else i if i > 0 else 0
        prev_sum = np.sum(x[prev_beg:prev_end], dtype=float)

        # get sum of post context
        post_beg = -1 if i >= x.size - 1 else i + 1 if i + 1 < x.size - 1 else x.size - 1
        post_end = -1 if i >= x.size - 1 else x.size if i + n >= x.size else i + n + 1
        post_sum = np.sum(x[post_beg:post_end], dtype=float)

        # compute average
        avg_i = (prev_sum + post_sum) / ((prev_end - prev_beg) + (post_end - post_beg))

        # subtract from current value
        x_avg[i] = x[i] - avg_i
    gsr_map['PHASIC'] = x_avg


def count_peaks(gsr_map):
    # first pass to get onset and offset markers
    x = gsr_map['PHASIC']
    onset = None
    peak_coords = []
    for i in range(x.size):
        if x[i] > 0.01 and onset is None:
            onset = i
        elif x[i] < 0 and onset:
            peak_coords.append([onset, i])  # i is offset
            onset = None
    print('Total number of peaks: {}'.format(len(peak_coords)))

    # second pass to get amplitude
    x = np.array(gsr_map['MICROSIEMENS'], dtype=float)
    for i in range(len(peak_coords)):
        onset = peak_coords[i][0]
        offset = peak_coords[i][1]
        amplitude = np.max(x[onset:offset]) - x[onset]
        peak_coords[i].append(amplitude)
    gsr_map['PEAKS'] = peak_coords


def run_analysis(flist):
    for fcsv in flist:
        exp_name, data_map = load_esense_csv(fcsv)
        avg_scr_peaks(data_map)
        count_peaks(data_map)


if __name__ == '__main__':
    setup_logging()
    parent_dir = '/Users/alevenberg/Downloads/eSense_Skin Response_20190409'
    flist = [os.path.join(parent_dir, x) for x in os.listdir(parent_dir)]
    run_analysis(flist)


