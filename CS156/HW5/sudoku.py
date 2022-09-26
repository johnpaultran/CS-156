# ----------------------------------------------------------------------
# Name:     sudoku
# Purpose:  Homework5
#
# Author(s): Athena Nguyen & John Paul Tran
#
# ----------------------------------------------------------------------
"""
Sudoku puzzle solver implementation

q1:  Basic Backtracking Search
q2:  Backtracking Search with AC-3
q3:  Backtracking Search with MRV Ordering and AC-3
"""
import csp

# Enter your helper functions here
def get_neighbors(row, col):
    """
    Helper function to create_neighbors that gets all of
    the neighbors of a variable at the given index
    :param row: row index of the variable
    :param col: column index of the variable
    :return: set of tuples that represent the indexes
             of all the neighbors of the given variable
    """
    # set to be returned by the function
    n = set()

    # add neighbors of same row into the set
    for col_index in range(9):
        if col_index != col:
            n.add((row, col_index))

    # add neighbors of the same column into the set
    for row_index in range(9):
        if row_index != row:
            n.add((row_index, col))

    # add neighbors of the same 3x3 box into the set
    box_row = int(row / 3)
    box_col = int(col / 3)
    for row_index in range(box_row * 3, (box_row * 3) + 3):
        for col_index in range(box_col * 3, (box_col * 3) + 3):
            if row_index != row and col_index != col and (row_index, col_index) not in n:
                n.add((row_index, col_index))

    # return the set of neighbors of the variable at the given index
    return n

def create_neighbors(puzzle):
    """
    Function that creates a dictionary with keys that are each index in the
    puzzle and their values containing the list of keys' corresponding neighbors
    :param puzzle: The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: dictionary of the neighbors of each index
    """
    # dictionary to be returned by the function
    neighbors_dictionary = {}

    # call to helper function to get the neighbors of each key in the puzzle
    for row in range(9):
        for col in range(9):
            neighbors_dictionary[(row, col)] = get_neighbors(row, col)

    # return the dictionary of keys and their values
    return neighbors_dictionary

def create_domains(puzzle):
    """
    Function that creates a dictionary with the domains of each index in the puzzle
    :param puzzle: The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: dictionary of domain values at each index
    """
    # dictionary to be returned by the function
    domain_dictionary = {}

    # create domain for each index in puzzle
    for row in range(9):
        for col in range(9):
            # if index already has a domain
            if (row, col) in puzzle.keys():
                domain_dictionary[(row, col)] = {puzzle[(row, col)]}
            # else the index has no initial domain
            else:
                # create domain with values 1-9
                domain_dictionary[(row, col)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}

    # return the dictionary domain values at each index
    return domain_dictionary

def check_constraints(var1, val1, var2, val2):
    """
    Function that checks if two given variables satisfy the constraint
    :param var1: first variable
    :param val1: value of the first variable
    :param var2: second variable
    :param val2: value of the second variable
    :return: True if the two given variables have different values, False otherwise
    """
    return val1 != val2

def build_csp(puzzle):
    """
    Create a CSP object representing the puzzle.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: CSP object
    """
    # Enter your code here and remove the pass statement below
    return csp.CSP(create_domains(puzzle), create_neighbors(puzzle), check_constraints)

def q1(puzzle):
    """
    Solve the given puzzle with basic backtracking search
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp = build_csp(puzzle)
    solution = csp.backtracking_search(), csp
    return solution

def q2(puzzle):
    """
    Solve the given puzzle with backtracking search and AC-3 as
    a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp = build_csp(puzzle)
    csp.ac3_algorithm()
    solution = csp.backtracking_search(), csp
    return solution

def q3(puzzle):
    """
    Solve the given puzzle with backtracking search and MRV ordering and
    AC-3 as a preprocessing step.
    :param puzzle (dictionary): The dictionary keys are tuples
    (row, column) representing the filled puzzle squares and the values
    are the corresponding numbers assigned to these squares.
    :return: a tuple consisting of a solution (dictionary) and the
    CSP object.
    """
    # Enter your code here and remove the pass statement below
    csp = build_csp(puzzle)
    csp.ac3_algorithm()
    solution = csp.backtracking_search("MRV"), csp
    return solution
