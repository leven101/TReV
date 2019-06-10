import os
import csv
import numpy as np
import logging
from collections import defaultdict

var_to_select = ['AVERAGE OF SESSION', 'SDNN', 'RMSDD', 'Stress Index',
                 'AVERAGE RR', 'Average HF', 'Average LF', 'LF/HF ratio']

def setup_logging():
    log_format = '%(asctime)s %(levelname)-7s %(name)-20s:%(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)


def load_esense_csv(path):
    logging.info('Processing file {}'.format(path))
    exp_name = None
    data_map = defaultdict(float)
    with open(path, 'r') as fin:
        fcsv = csv.reader(fin, delimiter=';')
        for i, row in enumerate(fcsv):
            if row[0] == 'RECORDING NAME':
                exp_name = row[1]
            elif row[0] in var_to_select:
                data_map[row[0]] = float(row[1].split()[0])
    return exp_name, data_map


def run_bl_vs_trev_analysis(flist):
    total_stats = {'bl': defaultdict(float), 'trev': defaultdict(float)}
    for fcsv in flist:
        exp_name, data_map = load_esense_csv(fcsv)
        logging.info('Processing experiment {}'.format(exp_name))
        exp_type = 'bl' if 'Baseline-' in exp_name else 'trev'
        total_stats[exp_type]['exp_cnt'] += 1
        for var in var_to_select:
            total_stats[exp_type][var] += data_map[var]
    print(total_stats)
    for exp_type in total_stats:
        print('Exp Type: {}'.format(exp_type))
        for var in var_to_select:
            avg = total_stats[exp_type][var] / total_stats[exp_type]['exp_cnt']
            print('\t{}: {}'.format(var, avg))


if __name__ == '__main__':
    # setup_logging()
    parent_dir = '/Users/abby/Documents/TREV/biometrics/eSense_Pulse'
    flist = [os.path.join(parent_dir, x) for x in os.listdir(parent_dir) if x.endswith('.csv')]
    logging.info('Loaded {} experiments'.format(len(flist)))
    run_bl_vs_trev_analysis(flist)
