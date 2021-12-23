#!/usr/bin/env python

import os, sys
import random
import numpy as np
import argparse
import json
import copy

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# from mlc import mat_fi
from MLCSim import MLCSim

# https://stackoverflow.com/a/8391735/9047818
# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Restore
def enablePrint():
    sys.stdout = sys.__stdout__


def get_configs(b, c):
    configs = []
    if b == 2:
        if c == 2:
            configs = [
                [[1, 2], [0, 3]],  # 2.1213203435596424
                [[1, 3], [0, 2]],  # 3.5355339059327378
                [[2, 3], [0, 1]],  # 6.363961030678928
            ]
        elif c == 3:
            configs = [
                [[2, 3], [1, 4], [0, 5]],  # 10.816653826391969
                # [[2, 3], [1, 5], [0, 4]],  # 11.532562594670797
                # [[2, 4], [1, 3], [0, 5]],  # 11.532562594670797
                [[2, 5], [1, 4], [0, 3]],
                # [[4, 5], [1, 2], [0, 3]],  # 23.430749027719962
                # [[4, 5], [1, 3], [0, 2]],  # 23.515952032609693
                [[4, 5], [2, 3], [0, 1]],  # 23.811761799581316
            ]
        elif c == 4:
            configs = [
                [[3, 4], [2, 5], [1, 6], [0, 7]],  # 46.94944089123959
                # [[3, 4], [2, 5], [1, 7], [0, 6]],  # 47.40165257316106
                # [[3, 4], [2, 6], [1, 5], [0, 7]],  # 47.40165257316106
                [[3, 7], [2, 6], [1, 5], [0, 4]],
                # [[6, 7], [4, 5], [1, 2], [0, 3]],  # 87.61421117604152
                # [[6, 7], [4, 5], [1, 3], [0, 2]],  # 87.62942808592709
                [[6, 7], [4, 5], [2, 3], [0, 1]],  # 87.6826664740529
            ]
        elif c == 8:
            # 8 2-bit cells
            configs = [
                [[7, 8], [6, 9], [5, 10], [4, 11], [3, 12], [2, 13], [1, 14], [0, 15]],  # 11309.449430043634
                # [[7, 8], [6, 10], [5, 9], [4, 11], [3, 12], [2, 13], [1, 14], [0, 15]],  # 11309.656385300636
                # [[7, 8], [6, 9], [5, 10], [4, 11], [3, 12], [2, 13], [1, 15], [0, 14]],  # 11309.656385300636
                [[0, 8], [1, 9], [2, 10], [3, 11], [4, 12], [5, 13], [6, 14], [7, 15]],
                # [[14, 15], [12, 13], [10, 11], [8, 9], [6, 7], [4, 5], [1, 2], [0, 3]],  # 17071.805548811426
                # [[14, 15], [12, 13], [10, 11], [8, 9], [6, 7], [4, 5], [1, 3], [0, 2]],  # 17071.80558228349
                [[14, 15], [12, 13], [10, 11], [8, 9], [6, 7], [4, 5], [2, 3], [0, 1]],  # 17071.805699435714
            ]
    elif b == 3:
        if c == 2:
            # 2 3-bit cells
            configs = [
                [[2, 3, 4], [0, 1, 5]], # 4.949747468305833
                # [[1, 3, 4], [0, 2, 5]], # 7.7781745930520225
                # [[1, 2, 5], [0, 3, 4]], # 9.192388155425117
                [[0, 2, 4], [1, 3, 5]],
                # [[1, 4, 5], [0, 2, 3]], # 26.16295090390226
                # [[2, 4, 5], [0, 1, 3]], # 28.991378028648448
                [[3, 4, 5], [0, 1, 2]], # 34.64823227814083
            ]
        elif c == 3:
            # 3 3-bit cells
            configs = [
                [[4, 5, 6], [2, 3, 7], [0, 1, 8]],  # 78.0534005238294
                # [[4, 5, 6], [1, 3, 7], [0, 2, 8]],  # 79.5885251360605
                # [[3, 5, 6], [2, 4, 7], [0, 1, 8]],  # 79.8769887598007
                [[0, 3, 6], [1, 4, 7], [2, 5, 8]],
                # [[6, 7, 8], [1, 4, 5], [0, 2, 3]],  # 241.1769751309882
                # [[6, 7, 8], [2, 4, 5], [0, 1, 3]],  # 241.3386279345545
                [[6, 7, 8], [3, 4, 5], [0, 1, 2]],  # 241.7112602534961
            ]
        elif c == 4:
            # 4 3-bit cells
            configs = [
                [[6, 7, 8], [4, 5, 9], [2, 3, 10], [0, 1, 11]], #  730.7404349927089
                # [[6, 7, 8], [4, 5, 9], [1, 3, 10], [0, 2, 11]], #  731.6676727403866
                # [[6, 7, 8], [4, 5, 9], [1, 2, 11], [0, 3, 10]], #  732.1322171120005
                [[3, 7, 11], [2, 6, 10], [1, 9, 5], [0, 4, 8]],
                # [[9, 10, 11], [6, 7, 8], [1, 4, 5], [0, 2, 3]], # 1718.1552849883312
                # [[9, 10, 11], [6, 7, 8], [2, 4, 5], [0, 1, 3]], # 1718.17041743051
                [[9, 10, 11], [6, 7, 8], [3, 4, 5], [0, 1, 2]], # 1718.2053379422769
            ]
        elif c == 5:
            # 5 3-bit cells
            configs = [
                [[8, 9, 10], [6, 7, 11], [4, 5, 12], [2, 3, 13], [0, 1, 14]], #  6051.977511524642
                # [[8, 9, 10], [6, 7, 11], [4, 5, 12], [1, 3, 13], [0, 2, 14]], #  6052.653698998482
                # [[8, 9, 10], [6, 7, 11], [4, 5, 12], [1, 2, 14], [0, 3, 13]], #  6052.991888314405
                [[0, 5, 10], [1, 6, 11], [2, 7, 12], [3, 8, 13], [4, 9, 14]],
                # [[12, 13, 14], [9, 10, 11], [6, 7, 8], [1, 4, 5], [0, 2, 3]], # 12453.882478970161
                # [[12, 13, 14], [9, 10, 11], [6, 7, 8], [2, 4, 5], [0, 1, 3]], # 12453.884044746843
                [[12, 13, 14], [9, 10, 11], [6, 7, 8], [3, 4, 5], [0, 1, 2]], # 12453.887658076894
            ]
        elif c == 6:
            # 6 3-bit cells
            configs = [
                [[0, 1, 17], [2, 3, 16], [4, 5, 15], [6, 7, 14], [8, 9, 13], [10, 11, 12]],
                [[0, 6, 12], [1, 7, 13], [2, 8, 14], [3, 9, 15], [4, 10, 16], [5, 11, 17]],
                [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]],
            ]
    elif b == 4:
        if c == 2:
            configs = [
                [[3, 4, 5, 6], [0, 1, 2, 7]], # 10.606601717798213
                # [[2, 4, 5, 6], [0, 1, 3, 7]], # 16.263455967290593
                # [[1, 4, 5, 6], [0, 2, 3, 7]], # 19.091883092036785
                [[0, 2, 4, 6], [1, 3, 5, 7]],
                # [[2, 5, 6, 7], [0, 1, 3, 4]], # 142.12846301849606
                # [[3, 5, 6, 7], [0, 1, 2, 4]], # 147.78531726798843
                [[4, 5, 6, 7], [0, 1, 2, 3]], # 159.0990257669732
            ]
        elif c == 3:
            configs = [
                [[6, 7, 8, 9], [3, 4, 5, 10], [0, 1, 2, 11]], # 600.5622365750281,
                # [[6, 7, 8, 9], [2, 4, 5, 10], [0, 1, 3, 11]], # 603.8137129943307,
                # [[5, 7, 8, 9], [3, 4, 6, 10], [0, 1, 2, 11]], # 604.5982136923661,
                [[0, 3, 6, 9], [1, 4, 7, 10], [2, 5, 8, 11]],
                # [[8, 9, 10, 11], [2, 5, 6, 7], [0, 1, 3, 4]], # 2145.7676947889768
                # [[8, 9, 10, 11], [3, 5, 6, 7], [0, 1, 2, 4]], # 2145.9587600883665
                [[8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]], # 2146.3632031881275
            ]
        elif c == 4:
            configs = [
                [[9, 10, 11, 12], [6, 7, 8, 13], [3, 4, 5, 14], [0, 1, 2, 15]], # 11610.299576238333
                # [[9, 10, 11, 12], [6, 7, 8, 13], [2, 4, 5, 14], [0, 1, 3, 15]], # 11612.17580458833
                # [[9, 10, 11, 12], [6, 7, 8, 13], [1, 4, 5, 14], [0, 2, 3, 15]], # 11613.114149529401
                [[3, 7, 11, 15], [2, 6, 10, 14], [1, 5, 9, 13], [0, 4, 8, 12]],
                # [[12, 13, 14, 15], [8, 9, 10, 11], [2, 5, 6, 7], [0, 1, 3, 4]], # 30088.55184700653
                # [[12, 13, 14, 15], [8, 9, 10, 11], [3, 5, 6, 7], [0, 1, 2, 4]], # 30088.560931301894
                [[12, 13, 14, 15], [8, 9, 10, 11], [4, 5, 6, 7], [0, 1, 2, 3]], # 30088.580163410836
            ]
    return configs

def get_error_map(b, kind):
    error_map = []
    if b == 2:
        if kind == 'uniform':
            error_map = [
                [0.0,   0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.0],
            ]
        elif kind == 'split':
            error_map = [
                [0.0,    0.046],
                [0.046,  0.001],
                [0.001,  0.046],
                [0.046,   0.0],
            ]
    elif b == 3:
        if kind == 'uniform':
            error_map = [
                [0.0,   0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037,   0.0],
            ]
        elif kind == 'split':
            error_map = [
                [0.0,   0.0415],
                [0.0415, 0.0415],
                [0.0415, 0.0415],
                [0.0415,  0.001],
                [0.001,  0.0415],
                [0.0415, 0.0415],
                [0.0415, 0.0415],
                [0.0415,   0.0],
            ]
    elif b == 4:
        if kind == 'uniform':
            error_map = [
                [0.0,   0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.037],
                [0.037, 0.0],
            ]
        elif kind == 'split':
            error_map = [
                [0.0,   0.037],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925,  0.001],
                [0.001,   0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925, 0.03925],
                [0.03925,   0.0],
            ]
    return error_map


def inject_faults(mat, error_map, b):
    err_count = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            val = mat[i][j]
            new_val = val
            err_prob_l = error_map[val][0]
            err_prob_h = error_map[val][1]
            err_prob_s = err_prob_l + err_prob_h

            rand = random.random()
            if rand < err_prob_l:
                new_val -= 1
            elif err_prob_l < rand < err_prob_l + err_prob_h:
                new_val += 1

            if val != new_val:
                err_count += 1
                mat[i][j] = new_val

    return err_count

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', type=int, default=2,
                        choices=[2, 3, 4], help='bits per cell')
    parser.add_argument('-c', type=int, default=2,
                        choices=[2, 3, 4, 5, 6, 7, 8], help='num of cells')
    parser.add_argument('-f', help='config JSON')
    parser.add_argument('--arr-size', type=int, default=2**8, 
        help='size of the array to test')
    parser.add_argument('--iter-size', type=int, default=2**8, 
        help='number of arrays to test')
    parser.add_argument('--err-kind', default='uniform')
    parser.add_argument('--plot', action="store_true", default=False)

    args = parser.parse_args()

    configs = []

    if args.f is not None:
        print(f'Reading configs from file {args.f}')
        with open(args.f, 'r') as f:
            config = json.load(f)
    else:
        configs = get_configs(args.b, args.c)


    if configs == []:
        raise ValueError('No config loaded!')

    errs = [[] for i in range(len(configs))]
    errs_perc = [[] for i in range(len(configs))]
    total_count = 0

    b = len(configs[0][0])
    c = len(configs[0])

    error_map = get_error_map(b, args.err_kind)

    total_count = 0

    random.seed(0)
    for i in range(args.iter_size):
        # generate list of random values and encode them into a matrix
        mat = [[random.randint(0, 2**(b)-1) for _ in range(c)] for j in range(args.arr_size)]

        out_mat = copy.deepcopy(mat)

        inject_faults(out_mat, error_map, b)

        total_count += args.arr_size

        for config_i, config in enumerate(configs):
            mlc = MLCSim(config)

            # find errors in the result and save them
            for idx, line in enumerate(out_mat):
                dec_i = mlc.dec(list(map(int, mat[idx])))
                dec_o = mlc.dec(list(map(int, line)))
                if dec_i != dec_o:
                    # print(f'Config {config_i}: should be {int(dec_i)} is {dec_o}')
                    errs[config_i].append(abs(dec_o - dec_i))
                    errs_perc[config_i].append(abs(dec_o - dec_i) / 2**(b*c))

    print(f'{len(configs[0])} {len(configs[0][0])}-bit cells, {total_count} numbers tested:')
    for i, err in enumerate(errs):
        if len(err) == 0:
            print(f'Config {i} did not have errors')
        else:
            avg_err = np.average(err)
            avg_err_perc = avg_err / 2**(b*c) * 100
            print(f'Config {i} error count: {len(err):6d}, mean: {avg_err:8.3f}, stdev: {np.std(err):8.3f}, perc: {avg_err_perc:7.3f}%')

    if args.plot:
        plt.hist(
            errs_perc, 
            bins=[x/20 for x in range(0, 21)], 
            align='mid', 
            weights=[ [1/len(errs_perc[i]) for j in range(len(errs_perc[i]))] for i in range(len(errs_perc))]
            )
        plt.title(
            f'Distribution of errors for {c} {b}-bit cells, {args.arr_size} numbers for {args.iter_size} iterations, with {args.err_kind} threshold distribution')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.gca().set_ylim([0, 1])
        plt.xlabel('Percentage error')
        plt.ylabel('Number of errors')
        if len(configs) == 7:
            plt.legend(["Shell"]*3 + ["Stripe"] + ["Standard"]*3)
        elif len(configs) == 3:
            plt.legend(['Shell', 'Stripe', 'Standard'])
        plt.show()

if __name__=="__main__":
    main()
