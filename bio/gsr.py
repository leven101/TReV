import os
import csv
import numpy as np
import logging
from collections import defaultdict

var_to_select = ['AVERAGE OF SESSION', 'TOTAL SCR', '% of SCR OF SESSION']
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
            if row[0] == 'RECORDING NAME':
                exp_name = str(row[1])
            elif row[0] in var_to_select:
                data_map[row[0]] = float(row[1].split()[0].strip('%'))
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
        elif x[i] < 0 and onset is not None:
            peak_coords.append([onset, i])  # i is offset
            onset = None
    logging.info('Total number of peaks: {}'.format(len(peak_coords)))

    # second pass to get amplitude
    x = np.array(gsr_map['MICROSIEMENS'], dtype=float)
    for i in range(len(peak_coords)):
        onset = peak_coords[i][0]
        offset = peak_coords[i][1]
        amplitude = np.max(x[onset:offset]) - x[onset]
        peak_coords[i].append(amplitude)
    gsr_map['PEAKS'] = peak_coords


def run_bl_vs_trev_analysis(flist):
    peak_stats = {'bl': defaultdict(float), 'trev': defaultdict(float)}
    for fcsv in flist:
        exp_name, data_map = load_esense_csv(fcsv)
        logging.info('Processing experiment {}'.format(exp_name))
        avg_scr_peaks(data_map)
        count_peaks(data_map)
        exp_type = 'bl' if 'Baseline-' in exp_name else 'trev'
        peak_stats[exp_type]['exp_cnt'] += 1.0
        peak_stats[exp_type]['peak_cnt'] += float(len(data_map['PEAKS']))
        for _, _, amp in data_map['PEAKS']:
            peak_stats[exp_type]['amp'] += amp
        for var in var_to_select:
            peak_stats[exp_type][var] += data_map[var]
    logging.info(peak_stats)
    for exp_type in peak_stats:
        print('Exp Type: {}'.format(exp_type))
        avg_peaks = peak_stats[exp_type]['peak_cnt'] / peak_stats[exp_type]['exp_cnt']
        print('\tavg peaks: {}'.format(avg_peaks))
        peak_cnt = peak_stats[exp_type]['peak_cnt']
        avg_amp = (peak_stats[exp_type]['amp'] / peak_cnt) if peak_cnt > 0 else 0
        print('\tavg amplitude: {}'.format(avg_amp))
        for var in var_to_select:
            avg = peak_stats[exp_type][var] / peak_stats[exp_type]['exp_cnt']
            print('\t{}: {}'.format(var, avg))
    return peak_stats


def run_combined():
    parent_dir = '/Users/abby/Documents/TREV/biometrics/eSense_Skin Response_20190421'
    flist = [os.path.join(parent_dir, x) for x in os.listdir(parent_dir) if x.endswith('.csv')]
    logging.info('Loaded {} experiments'.format(flist))
    run_bl_vs_trev_analysis(flist)


def run_pair_wise_compare():
    parent_dir = '/Users/abby/Documents/TREV/biometrics/eSense_Skin Response'
    flist = [os.path.join(parent_dir, x) for x in os.listdir(parent_dir) if x.endswith('.csv')]
    name_2_exp = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [])))  # name -> exp_type -> values
    # load data per volunteer
    for fcsv in flist:
        exp_name, data_map = load_esense_csv(fcsv)
        name = exp_name.split('-')[-1]
        avg_scr_peaks(data_map)
        count_peaks(data_map)
        exp_type = 'bl' if 'Baseline-' in exp_name else 'trev'
        name_2_exp[name]['num-peaks'][exp_type].append(len(data_map['PEAKS']))  # total number of peaks

        avg_peak_amp = 0  # average amplitude of each peak
        for _, _, amp in data_map['PEAKS']:
            avg_peak_amp += amp
        if avg_peak_amp > 0:
            avg_peak_amp = avg_peak_amp/len(data_map['PEAKS'])
        name_2_exp[name]['amp'][exp_type].append(avg_peak_amp)

    # compute pairwise differences
    diff_dict = defaultdict(lambda: defaultdict(int))
    for _, signal_map in name_2_exp.items():
        for signal, val_map in signal_map.items():
            vs_diff = None
            for exp_type, ar in val_map.items():
                for i in range(len(ar)-1):
                    for j in range(i + 1, len(ar)):
                        diff_dict[signal][exp_type + '-only-diff'] += abs(ar[i] - ar[j])
                        diff_dict[signal][exp_type + '-num-comparisons'] += 1
                if vs_diff is None:
                    vs_diff = sum(ar)
                else:
                    vs_diff = abs(vs_diff - sum(ar))
                    diff_dict[signal]['vs_diff-num-comparisons'] += 1
            diff_dict[signal]['vs_diff'] += vs_diff
    for signal, vals in diff_dict.items():
        print(signal)
        print(vals)


def run_per_name():
    parent_dir = '/Users/abby/Documents/TREV/biometrics/eSense_Skin Response'
    flist = [os.path.join(parent_dir, x) for x in os.listdir(parent_dir) if x.endswith('.csv')]
    names_map = defaultdict(lambda: [])
    for fcsv in flist:
        exp_name, data_map = load_esense_csv(fcsv)
        # TREV-2-Stephen
        name = exp_name.split('-')[-1]
        names_map[name].append(fcsv)
    diff_map = defaultdict(lambda: defaultdict(int))
    ratio = 1.5
    num_above_ratio = 0
    for k,v in names_map.items():
        print(k)
        map = run_bl_vs_trev_analysis(v)
        diff_map[k]['cnt_diff'] = abs(map['bl']['peak_cnt'] - map['trev']['peak_cnt'])
        diff_map[k]['bl_avg_peaks'] = map['bl']['peak_cnt'] / map['bl']['exp_cnt']
        diff_map[k]['trev_avg_peaks'] = map['trev']['peak_cnt'] / map['trev']['exp_cnt']
        if diff_map[k]['trev_avg_peaks'] >= ratio * diff_map[k]['bl_avg_peaks'] or \
            diff_map[k]['bl_avg_peaks'] >= ratio * diff_map[k]['trev_avg_peaks']:
            num_above_ratio += 1
    for k,v in diff_map.items():
        print(k)
        for k2,v2 in v.items():
            print('\t', k2, v2)
    print('ratio: ', ratio)
    print('num_above_ratio: ', num_above_ratio)
    print('total participants: ', len(names_map))


def run_per_directory():
    parent_dir = '/Users/abby/Documents/TREV/biometrics/'
    dir_list = [x for x in os.listdir(parent_dir) if x.startswith('eSense_Skin Response_')]
    full_stats = defaultdict(lambda: defaultdict)
    for dir_path in dir_list:
        logging.info('Processing {}...'.format(dir_path))
        flist = [os.path.join(parent_dir, dir_path, x)
                 for x in os.listdir(os.path.join(parent_dir, dir_path)) if x.endswith('.csv')]
        print('Processing experiment ', dir_path)
        dir_stats = run_bl_vs_trev_analysis(flist)
        print(dir_stats)
        full_stats[dir_path] = dir_stats


if __name__ == '__main__':
    setup_logging()
    # run_pair_wise_compare()
    # run_combined()
    run_per_name()





