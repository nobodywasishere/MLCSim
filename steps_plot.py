#!/usr/bin/env python

import os, sys
import random
import numpy as np
import argparse
import json
import copy

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from min import findAllConfigs, calcCellDeltaList


def main():

    b = 3
    c = 2

    configs = findAllConfigs(b, c)

    steps = []
    maxval = 0
    for config in configs:
        config_steps = []
        for cell in config:
            config_steps.append(calcCellDeltaList(cell, b))
        steps.append(config_steps)

    print(steps)

    maxval = 0
    for i in steps:
        for j in i:
            for k in j:
                if k > maxval:
                    maxval = k

    fig, axs = plt.subplots(len(steps), sharex=True)
    plt.legend([f'Cell {j}' for j in reversed(range(len(steps[0])))])
    plt.xticks(range(0, b + 1))
    plt.ylabel('Step size')
    plt.xlabel('Cell level')

    for i in range(len(steps)):

        for j in range(len(steps[i])):
            x_axis = np.array([2**i for i in range(len(steps[i][0]))])

            # axs[i].bar(x_axis - 0.1, steps[i][0], width=0.2)
            axs[i].bar([i + (j)/5 - 0.2/b  for i in range(len(steps[i][j]))], steps[i][j], width=0.2)

        # axs[i].title.set_text(f'Config {list(reversed(configs[i]))}')
        axs[i].set_ylim([0, maxval + 1])
        
    fig.tight_layout()
    plt.show()

if __name__=="__main__":
    main()