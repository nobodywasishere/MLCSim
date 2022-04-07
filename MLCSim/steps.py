#!/usr/bin/env python

import argparse
import json

try:
    from .configs import sortConfigs
    from .dist import genErrorMap
except ImportError:
    from configs import sortConfigs
    from dist import genErrorMap


def __main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b", type=int, default=2, choices=[2, 3, 4], help="bits per cell"
    )
    parser.add_argument(
        "-c", type=int, default=2, choices=[2, 3, 4, 5, 6, 7, 8], help="num of cells"
    )
    parser.add_argument("-f", required=True, help="Cell configuration JSON")
    parser.add_argument("--thr", required=True, help="Threshold map JSON")

    args = parser.parse_args()

    b = args.b
    c = args.c

    with open(args.thr) as f:
        thr_map = json.load(f)

    error_map = genErrorMap(thr_map, b)

    sums = sortConfigs(b, c, error_map)

    print(
        "config".ljust(len(str(sums[0][1]))), "stdev".rjust(11), "sum * err".rjust(11)
    )
    for thing in sums:
        print(f"{thing[1]}: {thing[0]:10.5f}, {thing[2]:10.5f}")


if __name__ == "__main__":
    __main()
