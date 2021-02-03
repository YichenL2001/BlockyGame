"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    lst = []
    a = random.choice(['p', 'b'])
    colourss = [(1, 128, 181), (199, 44, 58), (138, 151, 71),
                (255, 211, 92)][:]
    for _ in range(num_goals):
        colour = random.choice(colourss)
        if a == 'p':
            lst.append(PerimeterGoal(colour))
        else:
            lst.append(BlobGoal(colour))
        colourss.remove(colour)
    return lst


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
    lst = []
    n = 2 ** (block.max_depth - block.level)
    if len(block.children) == 0:
        for _ in range(n):
            ll = []
            for _ in range(n):
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
            lst[c].extend(a[c])

        i = 3
        a = _flatten(block.children[i])
        # n = len(a)
        for c in range(n):
            lst[n + c].extend(a[c])
        return lst
    # same thing as above, better formatted
    # lst = []
    # if len(block.children) == 0:
    #     for _ in range(2 ** (block.max_depth - block.level)):
    #         ll = []
    #         for _ in range(2 ** (block.max_depth - block.level)):
    #             ll.extend([block.colour])
    #         lst.append(ll)
    #     return lst
    # else:
    #     lst = []
    #     for index in [1, 0]:
    #         lst.extend(_flatten(block.children[index]))
    #     index = 2
    #     flattened = _flatten(block.children[index])
    #     for index2 in range(len(flattened)):
    #         lst[index2].extend(flattened[index2])
    #     index = 3
    #     flattened = _flatten(block.children[index])
    #     for index2 in range(len(flattened)):
    #         lst[len(flattened) + index2].extend(flattened[index2])
    #     return lst

    # version 2. not correct
    # n = 2 ** (block.max_depth - block.level)
    # if len(block.children) == 0:
    #   return [[block.colour] * n] * n
    # elif block.level == block.max_depth - 1:
    #     c = block.children
    #     return [[c[1].colour, c[2].colour], [c[0].colour, c[3].colour]]
    # # elif block.level != block.max_depth - 1:
    # else:
    #     lst = [[], [], [], []]
    #     for i in range(4):
    #         if i == 0 or i == 3:
    #             a = _flatten(block.children[i])
    #             if len(a) == 2:
    #                 lst[2].extend(a[0])
    #                 lst[3].extend(a[1])
    #             else:
    #                 lst[0].extend(a[0])
    #                 lst[1].extend(a[1])
    #                 lst[2].extend(a[2])
    #                 lst[3].extend(a[3])
    #         else:
    #             b = _flatten(block.children[i])
    #             if len(b) == 2:
    #                 lst[0].extend(b[0])
    #                 lst[1].extend(b[1])
    #             else:
    #                 lst[0].extend(b[0])
    #                 lst[1].extend(b[1])
    #                 lst[2].extend(b[2])
    #                 lst[3].extend(b[3])
    #     return lst

    # version 1 (does not work because position rounded is not accurate to sort)
    # units = _get_units(block)
    # # {(1,0):(10,10,10),(0,0):(10,10,10)}
    # s = []
    # for p in units.keys():
    #     s.append(p)
    # s.sort()
    # # [(0,0),(1,0)]
    # lst = [[units[s[0]]]]
    # for i in range(len(s)):
    #     if i == 0:
    #         pass
    #     elif s[i][0] == s[i-1][0]:
    #         lst[-1].append(units[s[i]])
    #     else:
    #         lst.append([units[s[i]]])
    # return lst

# def _get_units(block: Block) -> Dict[Tuple[int, int], Tuple[int, int, int]]:
#     """Return a dictionary representing <block> as unit cells.
#     Each key is the cell location.
#     Each item is represented by a tuple of 3 ints, which is the colour
#     of the block at the cell location.
#     """
#     everything = {}
#     if block.level == block.max_depth:    # and len(block.children) == 0
#         # block is unit cell.
#         everything[block.position] = block.colour
#     elif block.level != block.max_depth and len(block.children) == 0:
#         # block can be smashed
#         for i in range(4):
#             new = Block(_children_positions(block)[i],
#                         round(block.size / 2.0), block.colour,
#                         block.level + 1, block.max_depth)
#             news = _get_units(new)
#             for pos in news:
#                 everything[pos] = news[pos]
#     else:
#         # block has children
#         for child in block.children:
#             news = _get_units(child)
#             for pos in news:
#                 everything[pos] = news[pos]
#     return everything


# def _children_positions(self) -> List[Tuple[int, int]]:
#     """Return the positions of this Block's four children.
#
#     The positions are returned in this order: upper-right child, upper-left
#     child, lower-left child, lower-right child.
#     """
#     x = self.position[0]
#     y = self.position[1]
#     size = self._child_size()
#
#     return [(x + size, y), (x, y), (x, y + size), (x + size, y + size)]


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """
    A player goal in the game of Blocky which is to get the most units of colour
    c on the outer perimeter of the board.
    """
    def score(self, board: Block) -> int:
        flat = _flatten(board)
        score = 0
        perimeter = []
        for c in flat[0]:
            perimeter.append(c)
        for c in flat[-1]:
            perimeter.append(c)
        for column in flat[:]:
            perimeter.extend([column[0], column[-1]])
        for c in perimeter:
            if c == self.colour:
                score += 1
        return score

    def description(self) -> str:
        return 'Player with most units of colour c on the outer ' \
               'perimeter of the board wins.'


class BlobGoal(Goal):
    """
    A player goal in the game of Blocky which is to get the most unit cells in
    the largest blob of the given colour.
    """
    def score(self, board: Block) -> int:
        scores = []
        flat = _flatten(board)
        n = len(flat)
        visited = []
        for i in range(n):
            visited.append([])
            for j in range(n):
                visited[i].append(-1)
        for i in range(n):
            for j in range(n):
                scores.append(self._undiscovered_blob_size((i, j),
                                                           flat, visited))
        return max(scores)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        x = pos[0]
        y = pos[1]
        if x < 0 or y < 0 or x >= len(board) or y >= len(board) or \
                visited[x][y] != -1:
            # pos is out of bound or visited
            return 0
        # pos is not visited
        # 0 <= x < len(board), 0 <= y < len(board)
        elif board[x][y] != self.colour:
            # visit the pos, not target colour
            visited[x][y] = 0
            return 0
        else:
            # visit the pos, target colour
            visited[x][y] = 1
            # visit the left, right, lower, upper ones
            # don't need to consider out-of-bound. the base case handles that.
            n = 1 + self._undiscovered_blob_size((x - 1, y), board, visited) + \
                self._undiscovered_blob_size((x + 1, y), board, visited) + \
                self._undiscovered_blob_size((x, y - 1), board, visited) +\
                self._undiscovered_blob_size((x, y + 1), board, visited)
            return n

    def description(self) -> str:
        return 'The player with the most unit cells in ' \
               'the largest blob of colour c wins.'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
    # from block import Block
    # from settings import COLOUR_LIST
    # from example_tests import set_children
    # board = Block((0, 0), 750, None, 0, 2)
    #
    # # Level 1
    # colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    # set_children(board, colours)
    #
    # # Level 2
    # colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    # set_children(board.children[1], colours)
    #
    # print(_flatten(board))
