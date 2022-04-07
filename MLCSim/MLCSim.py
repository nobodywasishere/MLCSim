#!/usr/bin/env python

import os, sys
import argparse
import json
from ast import literal_eval


class MLCSim:
    def __init__(self, config: list):
        """init MLCSim

        Args:
            config (list): Cell configuration
        """
        self.b = len(config[0])
        self.c = len(config)
        self.L = self.b * self.c
        self.config = config

    def checkVal(self, val: int):
        """Check if value can be stored in the MLC

        Args:
            val (int): Value to be checked

        Raises:
            ValueError: If value is too large
        """
        if val > 2**self.L - 1:
            raise ValueError(f"Value '{val}' is too large to store in {self.L} bits")

    def checkCells(self, cells: list):
        """Checks the value of each cell to make sure they're not too large

        Args:
            cells (list): Cells to be checked

        Raises:
            ValueError: If cell value is too large
        """
        for i in cells:
            if i > 2**self.b - 1:
                raise ValueError(f"Cell value '{i}' is too large")

    def enc(self, val: int) -> list:
        """Encode a value to MLC cells

        Args:
            val (int): Value to be encoded

        Returns:
            list: List representing the cells values
        """
        self.checkVal(val)
        out = []
        for cell in self.config:
            count = 0
            for i, bit in enumerate(cell):
                count += bool(val & 2**bit) << i
            out.append(count)
        return out

    def dec(self, cells: list) -> int:
        """Decode a value to MLC cells

        Args:
            cells (list): List representing the cells values

        Returns:
            int: Encoded value
        """
        self.checkCells(cells)
        out = 0
        for d, cell in enumerate(self.config):
            for i, bit in enumerate(cell):
                out += bool(cells[d] & 2**i) * 2**bit
        return out


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", required=True, help="cell config json")
    parser.add_argument(
        "action", choices=["enc", "dec"], help="action to take on value"
    )
    parser.add_argument("val", help="val to {en,de}code")

    args = parser.parse_args()

    with open(args.f, "r") as infile:
        config = json.load(infile)

    mlc = MLCSim(config)

    if args.action == "enc":
        print(mlc.enc(int(args.val)))
    elif args.action == "dec":
        cells = literal_eval(args.val)
        print(mlc.dec(cells))


if __name__ == "__main__":
    main()
