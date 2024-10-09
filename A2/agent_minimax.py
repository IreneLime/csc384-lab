###############################################################################
# This file implements various minimax search agents.
#
# CSC 384 Assignment 2 Starter Code
# version 2.0
###############################################################################
from wrapt_timeout_decorator import timeout

from mancala_game import play_move
from utils import *


def minimax_max_basic(board, curr_player, heuristic_func):
    """
    Perform Minimax Search for MAX player.

    Return the best move and its minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function

    :return the best move and its minimax value according to minimax search.
    """
    # Obtain all possible moves, if terminal then return None
    all_possible_moves = board.get_possible_moves(curr_player)
    if not all_possible_moves:
        return None, heuristic_func(board, curr_player)

    # Initialize best move and best value
    h_value = -math.inf
    best_move = -math.inf

    # max_{s' in succ(s)} minimax-value(s')
    for move in all_possible_moves:
        next_board = play_move(board, curr_player, move)
        # Update if the new value is more than the previous optimal value
        _, value = minimax_min_basic(
            next_board, get_opponent(curr_player), heuristic_func
        )
        if value > h_value:
            h_value = value
            best_move = move

    return best_move, h_value


def minimax_min_basic(board, curr_player, heuristic_func):
    """
    Perform Minimax Search for MIN player.

    Return the best move and its minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function

    :return the best move and its minimax value according to minimax search.
    """
    # Obtain all possible moves, if terminal then reurn None
    all_possible_moves = board.get_possible_moves(curr_player)
    if not all_possible_moves:
        return None, heuristic_func(board, get_opponent(curr_player))

    # Initialize best move and best value
    h_value = math.inf
    best_move = math.inf

    # min_{s' in succ(s)} minimax-value(s')
    for move in all_possible_moves:
        next_board = play_move(board, curr_player, move)
        _, value = minimax_max_basic(
            next_board, get_opponent(curr_player), heuristic_func
        )
        # Update if the new value is less than the previous optimal value
        if value < h_value:
            h_value = value
            best_move = move
    return best_move, h_value


def minimax_max_limit(board, curr_player, heuristic_func, depth_limit):
    """
    Perform Minimax Search for MAX player up to the given depth limit.

    Return the best move and its estimated minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit

    :return the best move and its minimmax value estimated by our heuristic function.
    """
    # Obtain all possible moves, if terminal then reurn None
    all_possible_moves = board.get_possible_moves(curr_player)
    if not all_possible_moves:
        return None, heuristic_func(board, curr_player)

    # Initialize best move and best value
    h_value = -math.inf
    best_move = board

    for move in all_possible_moves:
        next_board = play_move(board, curr_player, move)
        # If the current value is greater than the best value: optimal
        _, value = minimax_min_basic(next_board, curr_player, heuristic_func)
        if value > h_value:
            h_value = value
            best_move = move
    return best_move, h_value


def minimax_min_limit(board, curr_player, heuristic_func, depth_limit):
    """
    Perform Minimax Search for MIN player  up to the given depth limit.

    Return the best move and its estimated minimax value.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit

    :return the best move and its minimmax value estimated by our heuristic function.
    """
    # Obtain all possible moves, if terminal then return None
    all_possible_moves = board.get_possible_moves(curr_player)
    if not all_possible_moves:
        return None, heuristic_func(board, curr_player)

    # Initialize best move and best value
    h_value = math.inf
    best_move = board

    for move in all_possible_moves:
        next_board = play_move(board, curr_player, move)
        # If the current value is less than the best value: optimal
        _, value = minimax_max_basic(next_board, curr_player, heuristic_func)
        if value < h_value:
            h_value = value
            best_move = next_board
    return best_move, h_value


def minimax_max_limit_opt(
    board, curr_player, heuristic_func, depth_limit, optimizations
):
    """
    Perform Minimax Search for MAX player up to the given depth limit with the option of caching states.
    Return the best move and its minimmax value estimated by our heuristic function.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the ccurrent player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its minimmax value estimated by our heuristic function.
    """

    raise NotImplementedError


def minimax_min_limit_opt(
    board, curr_player, heuristic_func, depth_limit, optimizations
):
    """
    Perform Minimax Search for MIN player up to the given depth limit with the option of caching states.
    Return the best move and its minimmax value estimated by our heuristic function.
    If the board is a terminal state, return None as its best move.

    :param board: the current board
    :param curr_player: the current player
    :param heuristic_func: the heuristic function
    :param depth_limit: the depth limit
    :param optimizations: a dictionary to contain any data structures for optimizations.
        You can use a dictionary called "cache" to implement caching.
    :return the best move and its minimmax value estimated by our heuristic function.
    """

    raise NotImplementedError


###############################################################################
## DO NOT MODIFY THE CODE BELOW.
###############################################################################


@timeout(TIMEOUT, timeout_exception=AiTimeoutError)
def run_minimax(curr_board, player, limit, optimizations, hfunc):
    if optimizations is not None:
        opt = True
    else:
        opt = False

    if opt:
        move, value = minimax_max_limit_opt(
            curr_board, player, hfunc, limit, optimizations
        )
    elif limit >= 0:
        move, value = minimax_max_limit(curr_board, player, hfunc, limit)
    else:
        move, value = minimax_max_basic(curr_board, player, hfunc)

    return move, value
