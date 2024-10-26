###############################################################################
# This file contains helper functions and the heuristic functions
# for our AI agents to play the Mancala game.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################

import sys
import math

###############################################################################
### DO NOT MODIFY THE CODE BELOW

### Global Constants ###
TOP = 0
BOTTOM = 1
TIMEOUT = 60


### Errors ###
class InvalidMoveError(RuntimeError):
    pass


class AiTimeoutError(RuntimeError):
    pass


### Functions ###
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_opponent(player):
    if player == BOTTOM:
        return TOP
    return BOTTOM


### DO NOT MODIFY THE CODE ABOVE
###############################################################################


def heuristic_basic(board, player):
    """
    Compute the heuristic value of the current board for the current player
    based on the basic heuristic function.

    :param board: the current board.
    :param player: the current player.
    :return: an estimated utility of the current board for the current player.
    """
    return board.mancalas[player] - board.mancalas[get_opponent(player)]


def heuristic_advanced(board, player):
    """
    Compute the heuristic value of the current board for the current player
    based on the advanced heuristic function.

    :param board: the current board object.
    :param player: the current player.
    :return: an estimated heuristic value of the current board for the current player.
    """
    total_score = 0
    opponent = get_opponent(player)
    diff_store = board.mancalas[player] - board.mancalas[opponent]
    total_score += diff_store
    # If the current player has empty pockets
    for i, value in enumerate(board.pockets[player]):
        if value == 0:
            total_score += board.pockets[opponent][i]
    # If the opponent player has empty pockets
    for i, value in enumerate(board.pockets[opponent]):
        if value == 0:
            total_score -= board.pockets[player][i]

    return total_score
