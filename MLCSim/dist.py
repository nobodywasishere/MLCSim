#!/usr/bin/env python

"""Distribution functions

This module provides functions for dealing with normal distributions
and generating error maps.

When called directly as main, it allows for converting a threshold map
into an error map.

```
$ python -m MLCSim.dist --help

usage: dist.py [-h] [-b {1,2,3,4}] -f F [-o O]

options:
  -h, --help    show this help message and exit
  -b {1,2,3,4}  bits per cell
  -f F          Threshold map json to convert
  -o O          output to file
```
"""

import argparse
import json
from pprint import pprint

import numpy as np
import scipy.stats as ss

# https://stackoverflow.com/a/32574638/9047818
# https://stackoverflow.com/a/13072714/9047818
def normalMidpoint(mean_a: float, mean_b: float, std_a: float, std_b: float) -> float:
    """Find the midpoint between two normal distributions

    Args:
        mean_a (float): Mean of first distribution
        mean_b (float): Mean of second distribution
        std_a (float): Std dev of first distribution
        std_b (float): Std dev of second distribution

    Returns:
        float: Midpoint between distributions
    """
    a = 1 / (2 * std_a**2) - 1 / (2 * std_b**2)
    b = mean_b / (std_b**2) - mean_a / (std_a**2)
    c = (
        mean_a**2 / (2 * std_a**2)
        - mean_b**2 / (2 * std_b**2)
        - np.log(std_b / std_a)
    )
    roots = np.roots([a, b, c])
    masked = np.ma.masked_outside(roots, mean_a, mean_b)
    return masked[~masked.mask]


# https://www.askpython.com/python/normal-distribution
def normalChance(mean: float, stdev: float, thr: float) -> float:
    """Find the chance of a normal distribution above/below a given value

    Args:
        mean (float): Mean of the distribution
        stdev (float): Std dev of the distribution
        thr (float): Threshold to check above/below

    Returns:
        float: Chance for threshold to end up above/below the given point in the distribution
    """
    chance = ss.norm(loc=mean, scale=stdev).cdf(thr)
    return float(chance if mean > thr else 1 - chance)


def genErrorMap(thr_maps: dict, bpc: int) -> list:
    """Generate an error map from a threshold map

    Args:
        thr_maps (dict): Threshold map
        bpc (int): Bits per cell

    Raises:
        ValueError: if the given bpc is not in the threshold map

    Returns:
        list: Error map from the threshold map
    """
    if str(bpc) not in thr_maps.keys():
        raise ValueError(f"Threshold map does not have values for {bpc} levels")
    thr_map = thr_maps[str(bpc)]
    err_map = [[0.0]]

    for i in range(len(thr_map) - 1):
        mid = normalMidpoint(
            thr_map[i][0], thr_map[i + 1][0], thr_map[i][1], thr_map[i + 1][1]
        )
        up = normalChance(thr_map[i][0], thr_map[i][1], mid)
        dn = normalChance(thr_map[i + 1][0], thr_map[i + 1][1], mid)

        err_map[i].append(up)
        err_map.append([dn])

    err_map[-1].append(0.0)

    return err_map


def _main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b", type=int, default=2, choices=range(1, 5), help="bits per cell"
    )
    parser.add_argument("-f", required=True, help="Threshold map json to convert")
    parser.add_argument("-o", type=str, help="output to file")

    args = parser.parse_args()

    with open(args.f) as f:
        thr_map = json.load(f)

    err_map = genErrorMap(thr_map, args.b)

    if args.o:
        with open(args.o, "w") as f:
            json.dump(err_map, f)
    else:
        pprint(err_map)


if __name__ == "__main__":
    _main()
