#!/usr/bin/env python

import argparse
import json
from pprint import pprint

import numpy as np
import scipy.stats as ss

# https://stackoverflow.com/a/32574638/9047818
# https://stackoverflow.com/a/13072714/9047818
# Find the midpoint between two normal distributions
def normalMidpoint(mean_a, mean_b, std_a, std_b):
    a = 1/(2*std_a**2) - 1/(2*std_b**2)
    b = mean_b/(std_b**2) - mean_a/(std_a**2)
    c = mean_a**2 /(2*std_a**2) - mean_b**2 / (2*std_b**2) - np.log(std_b/std_a)
    roots = np.roots([a, b, c])
    masked = np.ma.masked_outside(roots, mean_a, mean_b)
    return masked[~masked.mask]

# https://www.askpython.com/python/normal-distribution
# Find the chance of a normal distribution above/below a given value
def normalChance(mean, stdev, thr):
    chance = ss.norm(loc = mean, scale = stdev).cdf(thr)
    return float(chance if mean > thr else 1 - chance)

# Generate an error map from a threshold map
def genErrorMap(thr_maps, bpc, lv=1):
    if bpc not in thr_maps.keys():
        raise ValueError(f'Threshold map does not have values for {bpc} levels')
    thr_map = thr_maps[bpc]
    err_map = [[0.0]]

    for i in range(len(thr_map) - lv):
        mid = normalMidpoint(
            thr_map[i][0], thr_map[i+lv][0],
            thr_map[i][1], thr_map[i+lv][1]
        )
        up = normalChance(thr_map[i][0], thr_map[i][1], mid)
        dn = normalChance(thr_map[i+lv][0], thr_map[i+lv][1], mid)

        err_map[i].append(up)
        err_map.append([dn])

    err_map[-1].append(0.0)

    return err_map

def chanceTwoLevelErr(thr_map, err=1e-20):
    if len(thr_map) > 2:
        for i in range(len(thr_map) - 2):
            mid = normalMidpoint(
                thr_map[i][0], thr_map[i+2][0],
                thr_map[i][1], thr_map[i+2][1]
            )
            up = normalChance(thr_map[i][0], thr_map[i][1], mid)
            dn = normalChance(thr_map[i+2][0], thr_map[i+2][1], mid)
            if up > err:
                return up
            elif dn > err:
                return dn
    return 0

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', type=int, default=2, 
                        choices=range(1, 5), help='bits per cell')
    parser.add_argument('-f', required=True,
                        help='Threshold map json to convert')
    parser.add_argument('-o', type=str, help='output to file')
    parser.add_argument('--lvls', type=int, default=1, 
        help='check likelihood of different than 1-level errors')

    args = parser.parse_args()

    with open(args.f) as f:
        thr_map = json.load(f)

    err_map = genErrorMap(thr_map, str(args.b), lv=args.lvls)

    if args.o:
        with open(args.o, 'w') as f:
            json.dump(err_map, f)
    else:
        pprint(err_map)

if __name__=="__main__":
    main()