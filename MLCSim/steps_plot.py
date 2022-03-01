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
from simulation import get_configs


def main():

    b = 3
    c = 4

    # configs = findAllConfigs(b, c)
    configs = get_configs(b, c)

    steps = []
    maxval = 0
    for config in configs:
        config_steps = []
        for cell in config:
            config_steps.append(calcCellDeltaList(cell, b))
        steps.append(config_steps)

    print(steps)

    fig, axs = plt.subplots(len(steps), sharex=True)
    # plt.legend([f'Cell {j}' for j in reversed(range(len(steps[0])))])
    # plt.yticks(range(0, 2**(b*c), 2))
    plt.xticks(range(0, 2**b))
    plt.xlabel('Set cell level')
    plt.ylabel('Cell value')

    labels = ['Shell', 'Stripe', 'Standard', 'Other']

    for i in range(len(steps)):

        for j in range(len(steps[i])):
            x_axis = np.array([2**i for i in range(len(steps[i][0])+1)])
            axs[i].plot([sum(steps[i][j][:k]) for k in range(len(steps[i][j]) + 1)])

        axs[i].title.set_text(f'{labels[i]} encoding')
        axs[i].set_ylim([0, 2**(b*c)])
        axs[i].set_yscale('symlog', base=2)
        
    # fig.tight_layout()
    plt.show()

if __name__=="__main__":
    main()