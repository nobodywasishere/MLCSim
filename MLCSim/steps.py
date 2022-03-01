#!/usr/bin/env python

import argparse
from statistics import stdev

from min import findAllConfigs, calcCellDeltaList

from simulation import get_error_map

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

    b = args.b
    c = args.c
    L = b*c

    sums = []

    error_map = get_error_map(b, args.err_kind)
    # print(error_map)

    for config in findAllConfigs(b, c):
        config_steps = [calcCellDeltaList(cell, b) for cell in config]

        err_sum = 0
        errs = []
        for cell in config_steps:
            l = []
            for i in range(2**b - 1):
                l.append((error_map[i][1] + error_map[i+1][0]) * cell[i])
            err_sum += sum(l)
            errs.append(sum(l))


        sums.append((stdev(errs), config, err_sum))
        # print()

    sums.sort()
    print('config'.ljust(len(str(sums[0][1]))), 'stdev'.rjust(11), 'sum * err'.rjust(11))
    for thing in sums:
        print(f'{thing[1]}: {thing[0]:10.5f}, {thing[2]:10.5f}')

if __name__=="__main__":
    main()