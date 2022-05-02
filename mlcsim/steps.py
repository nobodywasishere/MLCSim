#!/usr/bin/env python

"""Script for finding configurations

When called directly as main, it will provide the 'scores' of
all the possible configurations.

```
$ python -m MLCSim.steps --help

usage: steps.py [-h] [-b {2,3,4}] [-c {2,3,4,5,6,7,8}] --thr THR

options:
  -h, --help          show this help message and exit
  -b {2,3,4}          bits per cell
  -c {2,3,4,5,6,7,8}  num of cells\
  --thr THR           Threshold map JSO
```
"""

import argparse
from ast import Import
import json

try:
    from cconfigs import sortConfigs  # type: ignore
    from dist import genErrorMap  # type: ignore
except ImportError:
    from mlcsim.cconfigs import sortConfigs
    from mlcsim.dist import genErrorMap


def _main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-b", type=int, default=2, choices=[2, 3, 4], help="bits per cell"
    )
    parser.add_argument(
        "-c", type=int, default=2, choices=[2, 3, 4, 5, 6, 7, 8], help="num of cells"
    )
    parser.add_argument("--thr", required=True, help="Threshold map JSON")

    args = parser.parse_args()

    b = args.b
    c = args.c

    with open(args.thr) as f:
        thr_map = json.load(f)

    error_map = genErrorMap(thr_map, b)

    sums = sortConfigs(b, c, error_map)

    print(
        "|",
        "config".ljust(len(str(sums[0][1])) + 2),
        "|",
        "stdev".rjust(12),
        "|",
        "sum * err".rjust(12),
        "|",
    )
    print("|" + ("-" * (len(str(sums[0][1])) + 4)) + "|" + ("-" * 14) + "|" + ("-" * 14) + "|")
    for thing in sums:
        print(f"| `{thing[1]}` | {thing[0]:10.10f} | {thing[2]:10.10f} |")


if __name__ == "__main__":
    _main()
