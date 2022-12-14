# ----------------------------------------------------------------------
# Name:     uninformed_search
# Purpose:  Homework3 - Implement bfs and ucs graph search algorithms
#
# Author(s): Athena Nguyen & John Paul Tran
#
# ----------------------------------------------------------------------
"""
Uninformed Search Algorithm implementation

dfs has been implemented for you.
Your task for homework 3 is to implement bfs and ucs.
"""
import data_structures

def dfs(problem):
    """
    Depth first graph search algorithm - implemented for you
    :param problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.Stack() # for dfs, the fringe is a stack
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)
    return None  # Failure -  no solution was found

def bfs(problem):
    """
    Breadth first graph search algorithm
    :param problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
            or None if there is no solution
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.Queue()  # for bfs, the fringe is a Queue
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root)
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                child_node = data_structures.Node(child_state, node, action)
                fringe.push(child_node)
    return None  # Failure -  no solution was found

def ucs(problem):
    """
    Uniform cost first graph search algorithm
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    :return: list of actions representing the solution to the quest
    """
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # for ucs, the fringe is a PriorityQueue
    state = problem.start_state()
    root = data_structures.Node(state, None, None)
    fringe.push(root, root.cumulative_cost)  # cumulative cost is the priority from root
    while not fringe.is_empty():
        node = fringe.pop()
        if problem.is_goal(node.state):
            return node.solution()  # we found a solution
        if node.state not in closed:  # we are implementing graph search
            closed.add(node.state)
            for child_state, action, action_cost in problem.expand(node.state):
                # update cumulative cost
                child_node = data_structures.Node(child_state, node, action, node.cumulative_cost + action_cost)
                fringe.push(child_node, child_node.cumulative_cost)
    return None  # Failure -  no solution was found

