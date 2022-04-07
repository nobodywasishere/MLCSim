#!/usr/bin/env python

import random
import numpy as np
import argparse
import json
import copy
from pprint import pprint

# import matplotlib.pyplot as plt
# from matplotlib.ticker import PercentFormatter

try:
    from .MLCSim import MLCSim
    from .configs import sortConfigs
    from .mat import generateMatrix, injectFaults, calcErrMagnitude
    from .dist import genErrorMap
except ImportError:
    from MLCSim import MLCSim
    from configs import sortConfigs
    from mat import generateMatrix, injectFaults, calcErrMagnitude
    from dist import genErrorMap


def __main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b", type=int, default=2, choices=[2, 3, 4], help="bits per cell"
    )
    parser.add_argument(
        "-c", type=int, default=2, choices=[2, 3, 4, 5, 6, 7, 8], help="num of cells"
    )
    parser.add_argument("-f", help="config JSON")
    parser.add_argument(
        "--arr-size", type=int, default=2**8, help="size of the array to test"
    )
    parser.add_argument(
        "--iter-size", type=int, default=2**8, help="number of arrays to test"
    )
    parser.add_argument("--thr", required=True, help="Threshold map to test")
    parser.add_argument("--plot", action="store_true", default=False)

    args = parser.parse_args()

    b = args.b
    c = args.c

    # Load the threshold map from file and generate the requisite error map
    with open(args.thr) as f:
        thr_map = json.load(f)
        error_map = genErrorMap(thr_map, b)

    # Load the cell configurations from file (if needed)
    # otherwise generate the best and worst configs to test
    if args.f is not None:
        print(f"Reading configs from file {args.f}")
        with open(args.f, "r") as f:
            configs = json.load(f)
    else:
        all_configs = sortConfigs(args.b, args.c, error_map)
        if len(all_configs) > 5:
            configs = [
                all_configs[0][1], all_configs[1][1], all_configs[2][1], 
                all_configs[-1][1], all_configs[-2][1], all_configs[-3][1]
            ]
        else:
            configs = [all_configs[i][1] for i in range(len(all_configs))]

    errs = [[] for i in range(len(configs))]
    errs_perc = [[] for i in range(len(configs))]

    if configs == []:
        raise ValueError("No config loaded!")

    # Generate random values, inject errors into them,
    # and find the magnitude of the errors for all the configs
    print('Running simulations...')
    random.seed(0)
    for i in range(args.iter_size):

        mat = generateMatrix(b, c, args.arr_size)
        out_mat = copy.deepcopy(mat)

        injectFaults(out_mat, error_map, b)

        calcErrMagnitude(configs, mat, out_mat, errs, errs_perc)

    # Print the results of the simulation
    print(
        f"{len(configs[0])} {len(configs[0][0])}-bit cells, {args.iter_size*args.arr_size} numbers tested:"
    )
    for i in range(len(configs)):
        print(f"Config {i}: {configs[i]}")

    for i, err in enumerate(errs):
        if len(err) == 0:
            print(f"Config {i} did not have errors")
        else:
            avg_err = np.average(err)
            avg_err_perc = avg_err / 2 ** (b * c) * 100
            print(
                f"Config {i} error count: {len(err):6d}, mean: {avg_err:8.3f}, stdev: {np.std(err):8.3f}, perc: {avg_err_perc:7.3f}%"
            )

    if args.plot:
        plt.hist(
            errs_perc,
            bins=[x / 20 for x in range(0, 21)],
            align="mid",
            weights=[
                [1 / len(errs_perc[i]) for j in range(len(errs_perc[i]))]
                for i in range(len(errs_perc))
            ],
        )
        plt.title(
            f"Distribution of errors for {c} {b}-bit cells, {args.arr_size} numbers for {args.iter_size} iterations, using {args.thr}"
        )
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.gca().set_ylim([0, 1])
        plt.xlabel("Percentage error")
        plt.ylabel("Number of errors")
        plt.legend([f"{configs[i]}" for i in range(len(errs_perc))])
        plt.show()


if __name__ == "__main__":
    __main()
