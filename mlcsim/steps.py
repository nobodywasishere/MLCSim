#!/usr/bin/env python

"""Script for finding configurations

When called directly as main, it will provide the 'scores' of
all the possible configurations.

```
$ python -m mlcsim.steps --help

usage: steps.py [-h] [-b {2,3,4}] [-c {2,3,4,5,6,7,8}] --thr THR

options:
  -h, --help          show this help message and exit
  -b {2,3,4}          bits per cell
  -c {2,3,4,5,6,7,8}  num of cells\
  --thr THR           Threshold map JSO
```

Prints out a pretty markdown table

```sh
$ ./mlcsim/steps.py --thr config/thr-split-1.json -b 2 -c 3

Calculating 15.0 permutations...
| config                     |        stdev |    sum * err |
|----------------------------|--------------|--------------|
| `[[2, 3], [1, 4], [0, 5]]` | 0.0010835747 | 0.0049746942 |
| `[[2, 3], [1, 5], [0, 4]]` | 0.0010840178 | 0.0049746942 |
| `[[2, 4], [1, 3], [0, 5]]` | 0.0010840178 | 0.0049746942 |
| `[[2, 4], [1, 5], [0, 3]]` | 0.0010846822 | 0.0049746942 |
| `[[2, 5], [1, 3], [0, 4]]` | 0.0010853461 | 0.0049746942 |
| `[[2, 5], [1, 4], [0, 3]]` | 0.0010855673 | 0.0049746942 |
| `[[3, 4], [2, 5], [0, 1]]` | 0.0024939156 | 0.0092341522 |
| `[[3, 5], [2, 4], [0, 1]]` | 0.0024946857 | 0.0092341522 |
| `[[3, 4], [1, 2], [0, 5]]` | 0.0026877419 | 0.0078143329 |
| `[[3, 4], [1, 5], [0, 2]]` | 0.0026880545 | 0.0078143329 |
| `[[3, 5], [1, 2], [0, 4]]` | 0.0026889923 | 0.0078143329 |
| `[[3, 5], [1, 4], [0, 2]]` | 0.0026891262 | 0.0078143329 |
| `[[4, 5], [2, 3], [0, 1]]` | 0.0056367465 | 0.0149134295 |
| `[[4, 5], [1, 2], [0, 3]]` | 0.0059556212 | 0.0134936102 |
| `[[4, 5], [1, 3], [0, 2]]` | 0.0059556414 | 0.0134936102 |

$ ./mlcsim/steps.py --thr config/thr-uniform.json -b 2 -c 3

Calculating 15.0 permutations...
| config                     |        stdev |    sum * err |
|----------------------------|--------------|--------------|
| `[[2, 3], [1, 4], [0, 5]]` | 0.0003343276 | 0.0019472414 |
| `[[2, 3], [1, 5], [0, 4]]` | 0.0003564553 | 0.0019472414 |
| `[[2, 4], [1, 3], [0, 5]]` | 0.0003564553 | 0.0019472414 |
| `[[2, 4], [1, 5], [0, 3]]` | 0.0003872836 | 0.0019472414 |
| `[[2, 5], [1, 3], [0, 4]]` | 0.0004158326 | 0.0019472414 |
| `[[2, 5], [1, 4], [0, 3]]` | 0.0004249229 | 0.0019472414 |
| `[[3, 4], [1, 2], [0, 5]]` | 0.0004249229 | 0.0019472414 |
| `[[3, 4], [1, 5], [0, 2]]` | 0.0004553120 | 0.0019472414 |
| `[[3, 4], [2, 5], [0, 1]]` | 0.0005162753 | 0.0019472414 |
| `[[3, 5], [1, 2], [0, 4]]` | 0.0005362441 | 0.0019472414 |
| `[[3, 5], [1, 4], [0, 2]]` | 0.0005468288 | 0.0019472414 |
| `[[3, 5], [2, 4], [0, 1]]` | 0.0005724352 | 0.0019472414 |
| `[[4, 5], [1, 2], [0, 3]]` | 0.0007242115 | 0.0019472414 |
| `[[4, 5], [1, 3], [0, 2]]` | 0.0007268450 | 0.0019472414 |
| `[[4, 5], [2, 3], [0, 1]]` | 0.0007359881 | 0.0019472414 |
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
    print(
        "|"
        + ("-" * (len(str(sums[0][1])) + 4))
        + "|"
        + ("-" * 14)
        + "|"
        + ("-" * 14)
        + "|"
    )
    for thing in sums:
        print(f"| `{thing[1]}` | {thing[0]:10.10f} | {thing[2]:10.10f} |")


if __name__ == "__main__":
    _main()
