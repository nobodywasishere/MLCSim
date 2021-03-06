#!/usr/bin/env python

"""Script for plotting different cell configurations

When called directly as main, it will create a pyplot showing the
steps sizes between each threshold level in an encoded MLC value.

3 cells, 3 bits per cell, `split-1` threshold distribution

![](../steps-split-1-3_3.png)

3 cells, 3 bits per cell, `uniform` threshold distribution

![](../steps-uniform-3_3.png)
"""

from ast import Import
from typing import List, Union
import numpy as np  # type: ignore
import argparse
import json

import matplotlib.pyplot as plt  # type: ignore


try:
    from cconfigs import calcCellDeltaList, sortConfigs  # type: ignore
    from dist import genErrorMap  # type: ignore
except ImportError:
    from mlcsim.cconfigs import calcCellDeltaList, sortConfigs
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

    # configs = findAllConfigs(b, c)
    # configs = get_configs(b, c)
    with open(args.thr) as f:
        thr_map = json.load(f)
    error_map = genErrorMap(thr_map, b)
    all_configs = sortConfigs(b, c, error_map)

    configs = (
        all_configs[:2] + [all_configs[int(len(all_configs) / 2)]] + all_configs[-2:]
    )

    steps: List[List[List[List[int]]]] = []
    for config in configs:
        config_steps: List[List[int]] = []
        for cell in config[1]:
            config_steps.append(calcCellDeltaList(cell))
        n = [config_steps, config[1], config[0], config[2]]
        if n not in steps:
            steps.append(n)

    print(steps)

    fig, axs = plt.subplots(len(steps), sharex=True)
    plt.legend([f"Cell {j}" for j in reversed(range(len(steps[0])))])
    plt.yticks(range(0, 2 ** (b * c), 2))
    plt.xticks(range(0, 2**b))
    plt.xlabel("Set cell level")
    plt.ylabel("Cell value")

    for i in range(len(steps)):

        for j in range(len(steps[i][0])):
            x_axis = np.array([2**i for i in range(len(steps[i][0]) + 1)])
            axs[i].plot(  # type: ignore
                [sum(steps[i][0][j][:k]) for k in range(len(steps[i][0][j]) + 1)]
            )

        axs[i].title.set_text(  # type: ignore
            f"{steps[i][1]} encoding, {steps[i][2]:0.5f} stdev, {steps[i][3]:0.5f} sum*err"
        )
        axs[i].set_ylim([0, 2 ** (b * c)])  # type: ignore
        axs[i].set_yscale("symlog", base=2)  # type: ignore

    fig.tight_layout()  # type: ignore
    plt.show()


if __name__ == "__main__":
    _main()
