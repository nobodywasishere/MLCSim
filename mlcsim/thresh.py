#!/usr/bin/env python

"""Threshold functions

This module provides functions for creating threshold maps.

When called directly as main, it allows for creating a threshold
map based on the number of bits per cell, the std dev of each 
threshold level, and the threshold distribution.

```
$ python -m mlcsim.thresh --help

usage: thresh.py [-h] [-d D] [-e E] [-f F] [--plot] [--scale-e]

options:
  -h, --help  show this help message and exit
  -d D        Threshold distribution
  -e E        Threshold stdev for 2 bits per cell
  -f F        Threshold map json to output
  --plot
  --scale-e   Scale -e with MLC size to preserve overlap
```

Currently supported threshold distributions are `uniform`, and
`split-n` where increasing `n` increases the amount of separation in
the center. 


`uniform` threshold distribution:

![`uniform` threshold distribution](../thr-uniform.png)

`split-1` threshold distribution:

![`split-1` threshold distribution](../thr-split-1.png)

`split-2` threshold distribution:

![`split-2` threshold distribution](../thr-split-2.png)
"""

import argparse
from pprint import pprint
import json
from typing import List, Tuple

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.stats import norm


def generateThresh(b: int, e: float, dist: str) -> List[Tuple[float, float]]:
    """Generates a threshold map

    Args:
        b (int): bits per cell
        e (float): std dev between levels
        dist (str): threshold distribution (uniform or split-*)

    Raises:
        ValueError: if dist is not uniform or split-*

    Returns:
        list: threshold map
    """
    if dist == "uniform":
        temp: List[Tuple[float, float]] = []
        for i in range(2 ** (b)):
            temp.append((float(i) / (2 ** (b) - 1), e))
        return temp
    elif dist[:5] == "split":
        if "-" in dist:
            center = float(dist.split("-")[1])
        else:
            center = e

        temp = []
        for i in range(2 ** (b - 1)):
            temp.append((i / (2 ** (b) + center / 2 - 1), e))

        for i in reversed(range(len(temp))):
            temp.append((1 - temp[i][0], e))
        return temp
    else:
        raise ValueError(f"Unknown threshold distribution: {dist}")


def _main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", default="uniform", help="Threshold distribution")
    parser.add_argument(
        "-e", type=float, default="0.04", help="Threshold stdev for 2 bits per cell"
    )
    parser.add_argument("-f", help="Threshold map json to output")
    parser.add_argument("--plot", action="store_true")
    parser.add_argument(
        "--scale-e",
        action="store_true",
        help="Scale -e with MLC size to preserve overlap",
    )

    args = parser.parse_args()

    thr_map = {}

    for b in range(2, 5):
        if args.scale_e:
            e = args.e * 6 / (2 ** (b + 1) - 2)
        else:
            e = args.e
        thr_map[b] = generateThresh(b, e, args.d)

    if args.f:
        with open(args.f, "w") as f:
            json.dump(thr_map, f)
    else:
        pprint(thr_map)

    # # https://www.statology.org/plot-normal-distribution-python/
    # if args.plot:
    #     fig, axs = plt.subplots(len(thr_map))

    #     # x-axis ranges from -5 and 5 with .001 steps
    #     x = np.arange(0, 1, 0.001)

    #     # define multiple normal distributions
    #     for b in range(2, 5):
    #         axs[b - 2].title.set_text(f"σ: {thr_map[b][1][1]:0.5f}")
    #         for n in thr_map[b]:
    #             axs[b - 2].plot(x, norm.pdf(x, n[0], n[1]), label=f"μ: {n[0]}")
    #         # axs[b-2].legend()

    #     # add legend to plot
    #     # plt.legend()
    #     fig.suptitle(f"{args.d} thresh dist")
    #     plt.show()


if __name__ == "__main__":
    _main()


"""
Preserving overlap equation for different thresholds
`|` marks a cell level, `++` marks the overlap or center between cells

0                                                                                                        1
|---------------------------------------------------++---------------------------------------------------|
|----------------++----------------|----------------++----------------|----------------++----------------|
|------++------|------++------|------++------|------++------|------++------|------++------|------++------|
|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|--++--|

- 1 bpc,   2 lvls: 1/2 distance
- 2 bpc,   4 lvls: 1/6 distance
- 3 bpc,   8 lvls: 1/14 distance
- 4 bpc,  16 lvls: 1/30 distance
- n bpc, 2^n lvls: 1/(2^(n+1)-2) distance
"""
