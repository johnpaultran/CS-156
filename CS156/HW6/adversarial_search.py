# ----------------------------------------------------------------------
# Name:     adversarial_search
# Purpose:  Homework 6 - Implement adversarial search algorithms
#
# Author: Athena Nguyen & John Paul Tran
#
# ----------------------------------------------------------------------
"""
Adversarial search algorithms implementation

Your task for homework 6 is to implement:
1.  minimax
2.  alphabeta
3.  abdl (alpha beta depth limited)
"""
import random
import math  # You can use math.inf to initialize to infinity

def rand(game_state):
    """
    Generate a random move.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the random move
    """
    done = False
    while not done:
        row = random.randint(0, game_state.size - 1)
        col = random.randint(0, game_state.size - 1)
        if game_state.available(row,col):
            done = True
    return row, col


def minimax(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm.
    (searching the entire tree from the current game state)
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    # calculate best move out of possible moves using minimax
    minimax = max(game_state.possible_moves(), key=lambda x: value(game_state.successor(x, "AI"), "user"))
    # return solution
    return minimax

def value(game_state, agent):
    """
    Calculate the minimax value for any state under the given agent's
    control.
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # AI win
    if game_state.is_win('AI'):
        return 1
    # User win
    if game_state.is_win('user'):
        return -1
    # Game is tied
    if game_state.is_tie():
        return 0
    # if the agent is AI return MAX
    if agent == 'AI':
        return max_value(game_state)
    # if the agent is user return MIN
    else:
        return min_value(game_state)

def max_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # list to hold the possible moves
    moves = []
    # for each possible move's index in the gameboard
    for row, col in game_state.possible_moves():
        # get the successor state's index and add to the list of moves
        moves.append(value(game_state.successor((row, col), 'AI'), 'user'))
    # return the max of the possible moves
    return max(moves)

def min_value(game_state):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user)
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # list to hold the possible moves
    moves = []
    # for each possible move's index in the gameboard
    for row, col in game_state.possible_moves():
        # get the successor state's index and add to the list of moves
        moves.append(value(game_state.successor((row, col), 'user'), 'AI'))
    # return the min of the possible moves
    return min(moves)


def alphabeta(game_state):
    """
    Find the best move for our AI agent using the minimax algorithm
    with alpha beta pruning.
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    alpha = -math.inf
    beta = math.inf
    # calculate best move out of possible moves using minimax w/ alpha beta pruning
    alphabeta = max(game_state.possible_moves(), key=lambda x: ab_value(game_state.successor(x, "AI"), "user", alpha, beta))
    # return solution
    return alphabeta

def ab_value(game_state, agent, alpha, beta):
    """
    Calculate the minimax value for any state under the given agent's
    control using alpha beta pruning
    :param game_state: GameState object - state may be terminal or
    non-terminal.
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) value of that state -1, 0 or 1
    """
    # AI win
    if game_state.is_win('AI'):
        return 1
    # User win
    if game_state.is_win('user'):
        return -1
    # Game is tied
    if game_state.is_tie():
        return 0
    # if the agent is AI return MAX
    if agent == 'AI':
        return abmax_value(game_state, alpha, beta)
    # if the agent is user return MIN
    else:
        return abmin_value(game_state, alpha, beta)

def abmax_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Max's
    control (AI agent) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # initialize v to negative infinity
    v = -math.inf
    # for each possible move in the gameboard
    for move in game_state.possible_moves():
        v = max(v, ab_value(game_state.successor(move, 'AI'), 'user', alpha, beta))
        # return v if it is greater than or equal to beta
        if v >= beta:
            return v
        # set new alpha value
        alpha = max(alpha, v)
    return v

def abmin_value(game_state, alpha, beta):
    """
    Calculate the minimax value for a non-terminal state under Min's
    control (user) using alpha beta pruning
    :param game_state: non-terminal GameState object
    :return: (integer) value of that state -1, 0 or 1
    """
    # initialize v to positive infinity
    v = math.inf
    # for each possible move in the gameboard
    for move in game_state.possible_moves():
        v = min(v, ab_value(game_state.successor(move, 'user'), 'AI', alpha, beta))
        # return v if it is less than or equal to alpha
        if v <= alpha:
            return v
        # set new beta value
        beta = min(beta, v)
    return v


def abdl(game_state, depth):
    """
    Find the best move for our AI agent by limiting the alpha beta
    search the given depth and using the evaluation function
    game_state.eval()
    :param game_state: GameState object
    :return:  a tuple representing the row column of the best move
    """
    alpha = -math.inf
    beta = math.inf
    # calculate best move out of possible moves using abdl
    abdl = max(game_state.possible_moves(), key=lambda x: abdl_value(game_state.successor(x, "AI"), "user", alpha, beta, depth))
    # return solution
    return abdl

def abdl_value(game_state, agent, alpha, beta, depth):
    """
    Calculate the utility for any state under the given agent's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: GameState object - state may be terminal or
    non-terminal
    :param agent: (string) 'user' or 'AI' - AI is max
    :return: (integer) utility of that state
    """
    # new value more consistent with eval (# of states max can win + # of states max can win when 1 is already taken)
    new_value = game_state.size + game_state.size - 1
    # AI win
    if game_state.is_win('AI'):
        return new_value
    # User win
    if game_state.is_win('user'):
        return -new_value
    # Game is tied
    if game_state.is_tie():
        return 0
    # Maximum depth is reached
    if depth == 0:
        return game_state.eval()
    # if the agent is AI return MAX
    if agent == 'AI':
        return abdlmax_value(game_state, alpha, beta, depth)
    # if the agent is user return MIN
    else:
        return abdlmin_value(game_state, alpha, beta, depth)

def abdlmax_value(game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Max's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # initialize v to negative infinity
    v = -math.inf
    # for each possible move in the gameboard
    for move in game_state.possible_moves():
        v = max(v, abdl_value(game_state.successor(move, 'AI'), 'user', alpha, beta, depth - 1))
        # return v if it is greater than or equal to beta
        if v >= beta:
            return v
        # set new alpha value
        alpha = max(alpha, v)
    return v

def abdlmin_value( game_state, alpha, beta, depth):
    """
    Calculate the utility for a non-terminal state under Min's control
    using depth limited alpha beta pruning and the evaluation
    function game_state.eval()
    :param game_state: non-terminal GameState object
    :return: (integer) utility (evaluation function) of that state
    """
    # initialize v to positive infinity
    v = math.inf
    # for each possible move in the gameboard
    for move in game_state.possible_moves():
        v = min(v, abdl_value(game_state.successor(move, 'user'), 'AI', alpha, beta, depth - 1))
        # return v if it is less than or equal to alpha
        if v <= alpha:
            return v
        # set new beta value
        beta = min(beta, v)
    return v