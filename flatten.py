from __future__ import annotations
import math
import random
from typing import List, Tuple, Dict
from block import Block
import unittest


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    # TODO: Implement me
    lst = []
    n = 2 ** (block.max_depth - block.level)
    if len(block.children) == 0:
        for _ in range(n):
            for _ in range(n):
                ll = []
                ll.extend([block.colour])
            lst.append(ll)
        return lst
        # return [[block.colour] * n] * n
    else:
        lst = []
        for i in [1, 0]:
            lst.extend(_flatten(block.children[i]))
        i = 2
        a = _flatten(block.children[i])
        n = len(a)
        for c in range(n):
            h = lst[c]
            hh = a[c]
            h.extend(hh)
        i = 3
        a = _flatten(block.children[i])
        n = len(a)
        for c in range(n):
            h = lst[n + c]
            hh = a[c]
            h.extend(hh)
        return lst
