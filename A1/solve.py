############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 1
## v1.0
## Implemented by Irene Li
############################################################

from typing import List
import heapq
from heapq import heappush, heappop
import time
import argparse
import math  # for infinity
import copy

from board import *


def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """

    return sorted(state.board.storage) == sorted(state.board.boxes)


def get_path_helper(state, path_list):
    path_list.append(state)
    if state.depth == 0:
        return path_list

    path_list = get_path_helper(state.parent, path_list)
    return path_list


def get_path(state):
    """
    Return a list of states containing the nodes on the path
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """

    path_list = []
    path_list = get_path_helper(state, path_list)
    return path_list[::-1]


def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """

    successor_list = []
    # robots = state.board.robots
    for i, pos in enumerate(state.board.robots):
        movement = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in movement:
            boxes = []
            robots = []

            test_pos = (pos[0] + dx, pos[1] + dy)

            # Robot cannot walk into another robot or the wall
            if (test_pos in state.board.robots) or (test_pos in state.board.obstacles):
                continue

            if test_pos in state.board.boxes:
                new_box = (test_pos[0] + dx, test_pos[1] + dy)

                # if test_pos in state.board.storage:
                #     continue

                # Robot cannot push 2 boxes or a box into other robots or the wall
                if (
                    (new_box in state.board.robots)
                    or (new_box in state.board.obstacles)
                    or (new_box in state.board.boxes)
                ):
                    continue

                # Create a new set of box positions
                boxes = [
                    new_box if box_pos == test_pos else box_pos
                    for box_pos in state.board.boxes
                ]
            else:
                boxes = state.board.boxes

            # Update the robot positions
            robots = [
                test_pos if r_pos == pos else r_pos for r_pos in state.board.robots
            ]
            succ_board = Board(
                state.board.name,
                state.board.width,
                state.board.height,
                robots,
                boxes,
                state.board.storage,
                state.board.obstacles,
            )
            f = state.depth + 1 + state.hfn(succ_board)
            succ_state = State(
                copy.deepcopy(succ_board),
                state.hfn,
                f,
                state.depth + 1,
                state,
            )
            successor_list.append(succ_state)

    return successor_list


def dfs_visit(state, visited):

    if is_goal(state):
        print(state.board)
        return state, visited

    visited.append(copy.deepcopy(state.id))

    # Loop through all successors of the current state and perform depth-first search
    for new_state in get_successors(state):
        if new_state.id not in visited:
            s, visited = dfs_visit(new_state, visited)
            if s != None and is_goal(s):
                print(s.board)
                return s, visited
    return None, visited


def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    init_state = State(init_board, heuristic_zero, 0, 0)
    last_state, visited = dfs_visit(init_state, [])
    if last_state != None:
        path = get_path(last_state)
        return path, len(path) - 1
    return [], -1


def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """

    frontier = []  # Contains sets with f value and state object pairs
    visited = {}  # Dictionary with state board id and state object
    init_state = State(init_board, heuristic_basic, heuristic_basic(init_board), 0)
    heapq.heappush(frontier, (init_state.f, init_state))

    # When frontier is not empty
    while frontier:
        (_, state) = heapq.heappop(frontier)

        # Return final goal
        if is_goal(state):
            path = get_path(state)
            return path, len(path) - 1
        visited[state.id] = state

        # Add new paths to frontier
        for new_state in get_successors(state):
            # New board configuration
            if new_state.id not in visited:
                heapq.heappush(frontier, (new_state.f, new_state))

            # Same board configuration
            else:
                # Repace if the f value of the current board config is less than the saved one
                if new_state.f < (visited[new_state.id]).f:
                    heapq.heappush(frontier, (new_state.f, new_state))
    return [], -1


def heuristic_basic(board):
    """
    Returns the heuristic value for the given board
    based on the Manhattan Distance Heuristic function.

    Returns the sum of the Manhattan distances between each box
    and its closest storage point.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    storage = sorted(board.storage)
    box = sorted(board.boxes)
    distance = []

    # Iterate through box locations
    for b_pos in box:
        min_distance = 0
        first = True
        min_index = 0
        # Find the closest box
        for i, s_pos in enumerate(storage):
            # Box already on a storage position
            if b_pos == s_pos:
                min_distance = 0
                break

            # Set the first min distance
            if first:
                min_distance = (
                    (s_pos[0] - b_pos[0]) ** 2 + (s_pos[1] - b_pos[1]) ** 2
                ) ** 0.5
                first = False
                continue

            # Calculate the direct distances
            dist = ((s_pos[0] - b_pos[0]) ** 2 + (s_pos[1] - b_pos[1]) ** 2) ** 0.5

            if dist < min_distance:
                min_distance = dist
                min_index = i
        if min_distance != 0:
            dx = abs(b_pos[0] - storage[min_index][0])
            dy = abs(b_pos[1] - storage[min_index][1])
            distance.append(dx + dy)

    return sum(distance)


def heuristic_advanced(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    raise NotImplementedError


def solve_puzzle(board: Board, algorithm: str, hfn):
    """
    Solve the given puzzle using the given type of algorithm.

    :param algorithm: the search algorithm
    :type algorithm: str
    :param hfn: The heuristic function
    :type hfn: Optional[Heuristic]

    :return: the path from the initial state to the goal state
    :rtype: List[State]
    """

    print("Initial board")
    board.display()

    time_start = time.time()

    if algorithm == "a_star":
        print("Executing A* search")
        path, step = a_star(board, hfn)
    elif algorithm == "dfs":
        print("Executing DFS")
        path, step = dfs(board)
    else:
        raise NotImplementedError

    time_end = time.time()
    time_elapsed = time_end - time_start

    if not path:

        print("No solution for this puzzle")
        return []

    else:

        print("Goal state found: ")
        path[-1].board.display()

        print("Solution is: ")

        counter = 0
        while counter < len(path):
            print(counter + 1)
            path[counter].board.display()
            print()
            counter += 1

        print("Solution cost: {}".format(step))
        print("Time taken: {:.2f}s".format(time_elapsed))

        return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The file that contains the puzzle.",
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The file that contains the solution to the puzzle.",
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        choices=["a_star", "dfs"],
        help="The searching algorithm.",
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        required=False,
        default=None,
        choices=["zero", "basic", "advanced"],
        help="The heuristic used for any heuristic search.",
    )
    args = parser.parse_args()

    # set the heuristic function
    heuristic = heuristic_zero
    if args.heuristic == "basic":
        heuristic = heuristic_basic
    elif args.heuristic == "advanced":
        heuristic = heuristic_advanced

    # read the boards from the file
    board = read_from_file(args.inputfile)

    # solve the puzzles
    path = solve_puzzle(board, args.algorithm, heuristic)

    # save solution in output file
    outputfile = open(args.outputfile, "w")
    counter = 1
    for state in path:
        print(counter, file=outputfile)
        print(state.board, file=outputfile)
        counter += 1
    outputfile.close()
