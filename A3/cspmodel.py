############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 3 Starter Code
## v1.0
############################################################

from board import *
from cspbase import *


def kropki_model(board):
    """
    Create a CSP for a Kropki Sudoku Puzzle given a board of dimension.

    If a variable has an initial value, its domain should only contain the initial value.
    Otherwise, the variable's domain should contain all possible values (1 to dimension).

    We will encode all the constraints as binary constraints.
    Each constraint is represented by a list of tuples, representing the values that
    satisfy this constraint. (This is the table representation taught in lecture.)

    Remember that a Kropki sudoku has the following constraints.
    - Row constraint: every two cells in a row must have different values.
    - Column constraint: every two cells in a column must have different values.
    - Cage constraint: every two cells in a 2x3 cage (for 6x6 puzzle)
            or 3x3 cage (for 9x9 puzzle) must have different values.
    - Black dot constraints: one value is twice the other value.
    - White dot constraints: the two values are consecutive (differ by 1).

    Make sure that you return a 2D list of variables separately.
    Once the CSP is solved, we will use this list of variables to populate the solved board.
    Take a look at csprun.py for the expected format of this 2D list.

    :returns: A CSP object and a list of variables.
    :rtype: CSP, List[List[Variable]]

    """
    var_list = create_variables(board.dimension, board)
    # [var.dom for var in var_list]
    obj = CSP("name", var_list)

    bin_diff_cons = satisfying_tuples_difference_constraints(board.dimension)
    white_dot_cons = satisfying_tuples_white_dots(board.dimension)
    black_dot_cons = satisfying_tuples_black_dots(board.dimension)
    no_dot_cons = satisfying_tuples_no_dots(board.dimension)
    r_c_const = create_row_and_col_constraints(board.dimension, bin_diff_cons, var_list)
    for c in r_c_const:
        obj.add_constraint(c)

    return obj
    raise NotImplementedError


def create_variables(dim, board):
    """
    Return a list of variables for the board, and initialize their domain appropriately.

    We recommend that your name each variable Var(row, col).

    :param dim: Size of the board
    :type dim: int

    :returns: A list of variables with an initial domain, one for each cell on the board
    :rtype: List[Variables]
    """
    var_list = []

    for r in range(len(board.cells)):
        for c in range(len(board.cells[r])):
            name = f"Var({str(r)},{str(c)})"
            var_list.append(Variable(name, list(range(1, dim + 1))))

    return var_list

    raise NotImplementedError


def satisfying_tuples_difference_constraints(dim):
    """
    Return a list of satifying tuples for binary difference constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    return [(r, c) for r in range(1, dim + 1) for c in range(1, dim + 1) if r != c]

    raise NotImplementedError


def satisfying_tuples_white_dots(dim):
    """
    Return a list of satifying tuples for white dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    return [
        (r, c) for r in range(1, dim + 1) for c in range(1, dim + 1) if abs(r - c) == 1
    ]

    raise NotImplementedError


def satisfying_tuples_black_dots(dim):
    """
    Return a list of satifying tuples for black dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    return [
        (r, c)
        for r in range(1, dim + 1)
        for c in range(1, dim + 1)
        if r == c * 2 or c == r * 2
    ]

    raise NotImplementedError


def create_row_and_col_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different row/column constraints.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]

    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    c_list = []
    # Find row constraints
    for r in range(dim):
        # Scan through each column and the remainig variables within the column
        for c in range(dim):
            for c_remain in range(c + 1, dim):
                curr_var = variables[r * dim + c]
                constrain_var = variables[r * dim + c_remain]
                # Add a new constraint variable for the pair of variables
                name = f"row_{curr_var.name}_{constrain_var.name}"
                const = Constraint(name, [curr_var, constrain_var])
                # Add tuples satisifying tuples to the constaint
                const.add_satisfying_tuples(sat_tuples)
                c_list.append(const)

    # Find column constraints
    for c in range(dim):
        for r in range(dim):
            for r_remain in range(r + 1, dim):
                curr_var = variables[r * dim + c]
                constrain_var = variables[r_remain * dim + c]
                name = f"row_{curr_var.name}_{constrain_var.name}"
                const = Constraint(name, [curr_var, constrain_var])
                const.add_satisfying_tuples(sat_tuples)
                c_list.append(const)

    return c_list

    raise NotImplementedError


def create_cage_constraints(dim, sat_tuples, variables):
    """
    Create and return a list of binary all-different constraints for all cages.

    :param dim: Size of the board
    :type dim: int

    :param sat_tuples: A list of domain value pairs (value1, value2) such that
        the two values in each tuple are different.
    :type sat_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]

    :returns: A list of binary all-different constraints
    :rtype: List[Constraint]
    """
    constraint = []

    return constraint

    raise NotImplementedError


def create_dot_constraints(dim, dots, white_tuples, black_tuples, variables):
    """
    Create and return a list of binary constraints, one for each dot.

    :param dim: Size of the board
    :type dim: int

    :param dots: A list of dots, each dot is a Dot object.
    :type dots: List[Dot]

    :param white_tuples: A list of domain value pairs (value1, value2) such that
        the two values in each tuple satisfy the white dot constraint.
    :type white_tuples: List[(int, int)]

    :param black_tuples: A list of domain value pairs (value1, value2) such that
        the two values in each tuple satisfy the black dot constraint.
    :type black_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]

    :returns: A list of binary dot constraints
    :rtype: List[Constraint]
    """
    constraint = []

    return constraint

    raise NotImplementedError


def satisfying_tuples_no_dots(dim):
    """
    Return a list of satifying tuples for no dot constraints.

    :param dim: Size of the board
    :type dim: int

    :returns: A list of satifying tuples
    :rtype: List[(int,int)]
    """
    return [
        (r, c)
        for r in range(1, dim + 1)
        for c in range(1, dim + 1)
        if (r != c * 2 and c != r * 2) and (abs(r - c) != 1) and (r != c)
    ]

    raise NotImplementedError


def create_no_dot_constraints(dim, dots, no_dot_tuples, variables):
    """
    Create and return a list of binary constraints, one for each dot.

    :param dim: Size of the board
    :type dim: int

    :param dots: A list of dots, each dot is a Dot object.
    :type dots: List[Dot]

    :param no_dot_tuples: A list of domain value pairs (value1, value2) such that
        the two values in each tuple satisfy the no dot constraint.
    :type no_dot_tuples: List[(int, int)]

    :param variables: A list of all the variables in the CSP
    :type variables: List[Variable]

    :returns: A list of binary no dot constraints
    :rtype: List[Constraint]
    """
    constraint = []
    for d in dots:
        satifsy_constraint = satisfying_tuples_no_dots(dim)
        constraint.append(satifsy_constraint)

    return constraint

    raise NotImplementedError
