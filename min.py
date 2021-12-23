#!/usr/bin/env python

import os, sys
import argparse
from itertools import permutations, combinations
from statistics import stdev, mean
from rich import print as pprint
import json
from math import factorial

# https://stackoverflow.com/a/42304815/9047818
def part(agents, items):
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
            for result in part(agents[1:], remainder):
                result[agents[0]] = selection
                yield result

def findAllConfigs(bits_per_cell, num_cells):
    num_perms = factorial(bits_per_cell*num_cells)/(factorial(num_cells)
                                                    * factorial(bits_per_cell)**num_cells)

    print(f'Calculating {num_perms} permutations...')
    if num_perms > 1e7:
        if not input(f'Warning: there are {int(num_perms)} configs to check, '
            '\nthis may cause performance issues. Continue? ').lower() in ['', 'y', 'yes']:
            exit(1)

    configs = []
    dups = 0

    c = 0
    configs = []
    for i in part(list(range(num_cells)), list(range(bits_per_cell*num_cells))):
        configs.append([j for j in i.values()])

    return configs

    # # Commented out bc very inefficient
    # # Essentially brute forces all permutations and takes only those
    # #   that will work, using a lot more space than necessary
    # perm_range = range(1, bits_per_cell*num_cells)
    # num_perms = len(list(permutations(perm_range)))
    # print(num_perms)
    # for p in permutations(perm_range):
    #     q = [0] + list(p)
    #     cells = sorted([
    #         sorted(q[(x*bits_per_cell):(x*bits_per_cell)+bits_per_cell])
    #         for x in range(num_cells)
    #     ])
    #     if cells not in configs:
    #         configs.append(cells)
    #     else:
    #         dups += 1
    # print(f'there were {dups} duplicates out of {num_perms}')
    # return configs

def calcCellDelta(cell, bpc):
    cell = [2**x for x in cell]
    return sum([2**i * (cell[bpc-i-1] - sum(cell[0:bpc-i-1])) for i in range(bpc)])

def calcCellDeltaList(cell, bpc):
    # cell = [2**x for x in cell]
    # out = []
    # for i in range(bpc):
    #     [out.append((cell[bpc-i-1] - sum(cell[0:bpc-i-1]))) for _ in range(2**i)]
    # return out
    out = []
    prev_val = 0
    for i in range(1, 2**bpc):
        curr_val = 0
        for idx, j in enumerate(list(bin(i)[2:].rjust(bpc, '0'))):
            # print(idx, j)
            curr_val += 2**cell[bpc - idx - 1] * int(j)
            pass

        out.append(curr_val - prev_val)
        prev_val = curr_val
    return out

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', type=int, default=2, 
                        choices=range(1, 5), help='bits per cell')
    parser.add_argument('-c', type=int, default=2,
                        choices=range(1, 10), help='num of cells')
    parser.add_argument('-o', type=str, help='output ')

    args = parser.parse_args()

    num_bits = args.b * args.c

    print(f'Calculating configs...')

    configs = findAllConfigs(args.b, args.c)

    print(f"There are {len(configs)} configs")
    # pprint(configs)

    minstd = 2**num_bits
    minstdcfg = None
    minavg = 2**num_bits
    minavgcfg = None

    perfs = []

    print(f'Calculating step sizes...')
    for config in configs:
        steps = [calcCellDelta(cell, args.b) for cell in config]
        std = stdev(steps)
        perfs.append([std, str(config), steps])
        if std < minstd:
            minstd = std
            minstdcfg = config
    
    print(f'The minimum config by stdev with stdev={minstd:.4f} is:')
    pprint(minstdcfg)

    if args.o is not None:
        with open(args.o, 'w') as outfile:
            json.dump(minstdcfg, outfile)

    perfs.sort()
    pprint(perfs[:3])
    pprint(perfs[-3:])

if __name__=="__main__":
    main()
