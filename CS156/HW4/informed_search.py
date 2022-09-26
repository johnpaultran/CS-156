# ----------------------------------------------------------------------
# Name:     informed_search
# Purpose:  Homework 4 - Implement astar and some heuristics
#
# Author(s): Athena Nguyen & John Paul Tran
# ----------------------------------------------------------------------
"""
A* Algorithm and heuristics implementation

Your task for homework 4 is to implement:
1.  astar
2.  single_heuristic
3.  better_heuristic
4.  gen_heuristic
"""
import data_structures


def astar(problem, heuristic):
    """
    A* graph search algorithm
    returns a solution for the given search problem
    :param
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py
    heuristic (a function) the heuristic function to be used
    :return: list of actions representing the solution to the quest
                or None if there is no solution
    """
    # Enter your code here and remove the pass statement below
    closed = set()  # keep track of our explored states
    fringe = data_structures.PriorityQueue()  # for A*, the fringe is a PriorityQueue
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
                # update new heuristic
                fringe.push(child_node, child_node.cumulative_cost + heuristic(child_state, problem))
    pass


def null_heuristic(state, problem):
    """
    Trivial heuristic to be used with A*.
    Running A* with this null heuristic, gives us uniform cost search
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: 0
    """
    return 0


def single_heuristic(state, problem):
    """
    Single heuristic based on the Manhattan distance. This is admissible
    because the Manhattan distance is calculated without cost, therefore it is smaller.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest

    :return: Manhattan distance, 0 if no medals leftover
    """
    # unpack tuple for sammy and medal
    sammy, medal = state
    # if there is a medal
    if medal:
        # return Manhattan distance
        return abs(medal[0][0] - sammy[0]) + abs(medal[0][1] - sammy[1])
    else:
        return 0

def manhattan_cost(sammy, medal, problem):
    """
    Helper function to calculate the Manhattan distance * the problem cost
    for medals in better_heuristic and gen_heuristic
    :param
    sammy: the current position of Sammy the Spartan
    medal: the position of medal
    problem: (a Problem object) representing the quest
    :return: Manhattan distance * cost of Sammy to the medal
    """
    # Unpack tuples for x & y coordinates of sammy and medal
    sammy_x, sammy_y = sammy
    medal_x, medal_y = medal

    # Check to see if sammy is to the right of the medal
    if sammy_x >= medal_x:
        # Check if sammy is below the medal
        if sammy_y >= medal_y:
            # Calculate heuristic
            return ((sammy_x - medal_x) * problem.cost[problem.WEST]) + ((sammy_y - medal_y) * problem.cost[problem.NORTH])
        # Else sammy is above medal
        else:
            # Calculate heuristic
            return ((sammy_x - medal_x) * problem.cost[problem.WEST]) + ((medal_y - sammy_y) * problem.cost[problem.SOUTH])
    # Else sammy is to the left of the medal
    else:
        # Check if sammy is below the medal
        if sammy_y >= medal_y:
            # Calculate heuristic
            return ((medal_x - sammy_x) * problem.cost[problem.EAST]) + ((sammy_y - medal_y) * problem.cost[problem.NORTH])
        # Else sammy is above medal
        else:
            # Calculate heuristic
            return ((medal_x - sammy_x) * problem.cost[problem.EAST]) + ((medal_y - sammy_y) * problem.cost[problem.SOUTH])


def better_heuristic(state, problem):
    """
    Better heuristic based on the Manhattan distance * the problem cost. This makes
    the heuristic better than single because it incorporates the costs as well. This
    is admissible and consistent since the calculations are still less than actual costs.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: Manhattan distance * cost of each move, 0 if no medal
    """
    # unpack tuple for sammy and medal
    sammy, medal = state
    # if there is a medal
    if medal:
        return manhattan_cost(sammy, medal[0], problem)
    else:
        return 0


def gen_heuristic(state, problem):
    """
    General heuristic calculates the better heuristic of each medal and takes the max
    as the heuristic for A*. The max value is the nearest to the actual cost. This heuristic
    is admissible since it is still less than or equal to actual cost and expands less nodes.
    :param
    state: A state is represented by a tuple containing:
                the current position of Sammy the Spartan
                a tuple containing the positions of the remaining medals
    problem: (a Problem object) representing the quest
    :return: the highest better heuristic out of the medals, 0 if no medals leftover
    """
    # unpack tuple for sammy and medal
    sammy, medals = state
    # if there are any medals
    if medals:
        # return the max heuristic out of the medals
        return max(manhattan_cost(sammy, medal, problem) for medal in medals)
    else:
        return 0