#!/usr/bin/env python

import random

try:
    from .MLCSim import MLCSim
except ImportError:
    from MLCSim import MLCSim


def generateMatrix(b: int, c: int, arr_size: int) -> list:
    """Generates a matrix of random values of a given size

    Args:
        b (int): Bits per cell
        c (int): Number of cells
        arr_size (int): Size of the array

    Returns:
        list: List of lists representing the array
    """
    # generate list of random values and encode them into a matrix
    return [
        [random.randint(0, 2 ** (b) - 1) for _ in range(c)] for j in range(arr_size)
    ]


def injectFaults(mat: list, error_map: dict, b: int) -> int:
    """Inject faults into an MLC matrix

    Args:
        mat (list): Matrix to inject faults into
        error_map (dict): Error map dictionary
        b (int): Bits per cell

    Returns:
        int: Number of injected errors in the matrix
    """
    err_count = 0
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            val = mat[i][j]
            new_val = val
            err_prob_l = error_map[val][0]
            err_prob_h = error_map[val][1]

            rand = random.random()
            if rand < err_prob_l:
                new_val -= 1
            elif err_prob_l < rand < err_prob_l + err_prob_h:
                new_val += 1

            if val != new_val:
                err_count += 1
                mat[i][j] = new_val

    return err_count


def calcErrMagnitude(
    configs: dict, in_mat: list, out_mat: list, errs: list, errs_perc: list
):
    """Calculates the magnitude of errors difference between two matrices

    Args:
        configs (dict): Cell configuration
        in_mat (list): Clean matrix
        out_mat (list): Dirty/error matrix
        errs (list): Magnitude of error appended to at index corresponding to the index of the config
        errs_perc (list): Percent magnitude of error appended to at index corresponding to the index of the config
    """
    for config_idx, config in enumerate(configs):
        mlc = MLCSim(config)

        # find errors in the result and save them
        for idx, line in enumerate(out_mat):
            dec_i = mlc.dec(list(map(int, in_mat[idx])))
            dec_o = mlc.dec(list(map(int, line)))
            if dec_i != dec_o:
                # print(f'Config {config_i}: should be {int(dec_i)} is {dec_o}')
                errs[config_idx].append(abs(dec_o - dec_i))
                errs_perc[config_idx].append(abs(dec_o - dec_i) / 2 ** (mlc.b * mlc.c))
