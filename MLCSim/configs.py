#!/usr/bin/env python

"""Cell configuration functions

This module provides functions for finding/handling cell
configurations.

When called directly as main, it outputs a list of the best
and wost configs.

```
$ python -m MLCSim.configs --help

usage: configs.py [-h] [-b {1,2,3,4}] [-c {1,2,3,4,5,6,7,8,9}] [-o O]

options:
  -h, --help            show this help message and exit
  -b {1,2,3,4}          bits per cell
  -c {1,2,3,4,5,6,7,8,9}
                        num of cells
  -o O                  output to file
```
"""

import argparse
from itertools import combinations
from statistics import stdev
from pprint import pprint
import json
from math import factorial

# https://stackoverflow.com/a/42304815/9047818
def _part(agents, items):
    if len(agents) == 1:
        yield {agents[0]: items}
    else:
        quota = len(items) // len(agents)
        for indexes in combinations(range(len(items)), quota):
            # Don't move the 0 from the 0th agent
            if indexes[0] != 0:
                continue
            remainder = items[:]
            selection = [remainder.pop(i) for i in reversed(indexes)][::-1]
            for result in _part(agents[1:], remainder):
                result[agents[0]] = selection
                yield result


def findAllConfigs(bits_per_cell: int, num_cells: int) -> list:
    """Calculates all possible cell configurations

    Args:
        bits_per_cell (int): Bits per cell
        num_cells (int): Number of cells

    Returns:
        list: List of all possible cell configurations
    """
    num_perms = factorial(bits_per_cell * num_cells) / (
        factorial(num_cells) * factorial(bits_per_cell) ** num_cells
    )

    print(f"Calculating {num_perms} permutations...")
    if num_perms > 1e7:
        if not input(
            f"Warning: there are {int(num_perms)} configs to check, "
            "\nthis may cause performance issues. Continue? "
        ).lower() in ["", "y", "yes"]:
            exit(1)

    configs = []
    dups = 0

    c = 0
    configs = []
    for i in _part(list(range(num_cells)), list(range(bits_per_cell * num_cells))):
        configs.append([j for j in i.values()])

    return configs


def sortConfigs(b: int, c: int, error_map: dict) -> list:
    """Generates all cell configs and sorts them by their delta and error sum

    Args:
        b (int): Bits per cell
        c (int): Number of cells
        error_map (dict): Error map dictionary

    Returns:
        list: All configs sorted by delta and error sum
    """
    sums = []

    for config in findAllConfigs(b, c):
        config_steps = [calcCellDeltaList(cell, b) for cell in config]

        err_sum = 0
        errs = []
        for cell in config_steps:
            l = []
            for i in range(2**b - 1):
                l.append((error_map[i][1] + error_map[i + 1][0]) * cell[i])
            err_sum += sum(l)
            errs.append(sum(l))

        sums.append((stdev(errs), config, err_sum))
        # print()

    sums.sort()
    return sums


def calcCellDelta(cell: list, bpc: int) -> int:
    """Calculates the sum of the step sizes for a cell

    Args:
        cell (list): List of bits in a cell (i.e. [0, 1, 2, 3])
        bpc (int): Bits per cell

    Returns:
        int: Sum of the step sizes between levels in the cell
    """
    cell = [2**x for x in cell]
    return sum(
        [2**i * (cell[bpc - i - 1] - sum(cell[0 : bpc - i - 1])) for i in range(bpc)]
    )


def calcCellDeltaList(cell: list, bpc: int) -> list:
    """Calculates the list of step sizes for a cell

    Args:
        cell (list): List of bits in a cell (i.e. [0, 1, 2, 3])
        bpc (int): Bits per cell

    Returns:
        list: List of step sizes between levels in the cell
    """
    out = []
    prev_val = 0
    for i in range(1, 2**bpc):
        curr_val = 0
        for idx, j in enumerate(list(bin(i)[2:].rjust(bpc, "0"))):
            # print(idx, j)
            curr_val += 2 ** cell[bpc - idx - 1] * int(j)
            pass

        out.append(curr_val - prev_val)
        prev_val = curr_val
    return out


def _main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b", type=int, default=2, choices=range(1, 5), help="bits per cell"
    )
    parser.add_argument(
        "-c", type=int, default=2, choices=range(1, 10), help="num of cells"
    )
    parser.add_argument("-o", type=str, help="output to file")

    args = parser.parse_args()

    num_bits = args.b * args.c

    print(f"Calculating configs...")

    configs = findAllConfigs(args.b, args.c)

    print(f"There are {len(configs)} configs")
    # pprint(configs)

    minstd = 2**num_bits
    minstdcfg = None
    minavg = 2**num_bits
    minavgcfg = None

    perfs = []

    print(f"Calculating step sizes...")
    for config in configs:
        steps = [calcCellDelta(cell, args.b) for cell in config]
        std = stdev(steps)
        perfs.append([std, str(config), steps])
        if std < minstd:
            minstd = std
            minstdcfg = config

    print(f"The minimum config by stdev with stdev={minstd:.4f} is:")
    pprint(minstdcfg)

    if args.o is not None:
        with open(args.o, "w") as outfile:
            json.dump(minstdcfg, outfile)

    perfs.sort()
    pprint(perfs[:3])
    pprint(perfs[-3:])


if __name__ == "__main__":
    _main()
