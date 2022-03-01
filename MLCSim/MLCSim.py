#!/usr/bin/env python

import os, sys
import argparse
import json
from ast import literal_eval

class MLCSim():
    def __init__(self, config):
        self.b = len(config[0])
        self.c = len(config)
        self.L = self.b * self.c
        self.config = config

    def checkVal(self, val):
        if val > 2**self.L - 1:
            raise ValueError(
                f"Value '{val}' is too large to store in {self.L} bits")

    def checkCells(self, cells):
        for i in cells:
            if i > 2**self.b - 1:
                raise ValueError(f"Cell value '{i}' is too large")

    def enc(self, val):
        self.checkVal(val)
        out = []
        for cell in self.config:
            count = 0
            for i, bit in enumerate(cell):
                count += bool(val & 2**bit) << i
            out.append(count)
        return out

    def dec(self, cells):
        self.checkCells(cells)
        out = 0
        for d, cell in enumerate(self.config):
            for i, bit in enumerate(cell):
                out += bool(cells[d] & 2**i) * 2**bit
        return out


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-b', type=int, default=2, choices=range(1,5), help='bits per cell')
    parser.add_argument('-c', type=int, default=2, choices=range(1,5), help='num of cells')
    parser.add_argument('-f', required=True, help="cell config json")
    parser.add_argument('action', choices=['enc', 'dec'], help="action to take on value")
    parser.add_argument('val', help='val to {en,de}code')

    args = parser.parse_args()

    with open(args.f, 'r') as infile:
        config = json.load(infile)

    mlc = MLCSim(args.b, args.c, config)

    if args.action == 'enc':
        print(mlc.enc(int(args.val)))
    elif args.action == 'dec':
        cells = literal_eval(args.val)
        print(mlc.dec(cells))

if __name__=="__main__":
    main()