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
    sum_player_pocket = sum(board.pockets[player])
    sum_opponent_pocket = sum(board.pockets[opponent])

    # Difference in store count
    diff_store = board.mancalas[player] - board.mancalas[opponent]
    total_store = board.mancalas[player] + board.mancalas[opponent]
    diff_stone = sum_player_pocket - sum_opponent_pocket

    pocket_num = len(board.pockets[player])
    player_empty = 0
    curr_capture = 0
    opponent_capture = 0
    opponent_empty = 0
    for i, stones in enumerate(board.pockets[player]):
        # Compute capture for the current player
        if stones == 0:
            curr_capture += board.pockets[opponent][pocket_num - i - 1]
        # Compute potential capture for the opponent
        if board.pockets[opponent][pocket_num - i - 1] == 0:
            opponent_capture += stones
    player_empty += sum(1 for stones in board.pockets[player] if stones == 0)
    opponent_empty += sum(1 for stones in board.pockets[opponent] if stones == 0)

    total_stones = total_store + sum_player_pocket + sum_opponent_pocket
    total_score = diff_store * 2 + diff_stone
    # Define game states
    # Start
    # Empty opponent, focus on capture
    if total_store < (total_stones / 4):
        total_score += opponent_empty * 2 + curr_capture * 2
        total_score -= player_empty * 2
        total_score -= opponent_capture
        total_score -= board.pockets[player][pocket_num - 1] * 2
    # End
    # Empty opponent, focus on capture
    # Prevent opponent from capture
    elif total_store > (3 * total_stones / 4):
        total_score += opponent_empty * 5 + curr_capture * 2
        total_score -= player_empty
        total_score -= opponent_capture * 2
        total_score += board.pockets[player][pocket_num - 1]
    # Middle
    else:
        total_score += opponent_empty * 3 + curr_capture * 1.5
        total_score -= player_empty * 1.5
        total_score -= opponent_capture * 1.5
        total_score += board.pockets[player][pocket_num - 1] * 1.5

    return total_score
