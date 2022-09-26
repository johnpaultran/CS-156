# ----------------------------------------------------------------------
# Name:     beliefs
# Purpose:  Homework 8
#
# Author(s): Athena Nguyen & John Paul
#
# ----------------------------------------------------------------------
"""
Module to track the belief distribution over all possible grid positions

Your task for homework 8 is to implement:
1.  update
2.  recommend_sensing
"""
import utils

class Belief(object):

    """
    Belief class used to track the belief distribution based on the
    sensing evidence we have so far.
    Arguments:
    size (int): the number of rows/columns in the grid

    Attributes:
    open (set of tuples): set containing all the positions that have not
        been observed so far.
    current_distribution (dictionary): probability distribution based on
        the evidence observed so far.
        The keys of the dictionary are the possible grid positions
        The values represent the (conditional) probability that the
        treasure is found at that position given the evidence
        (sensor data) observed so far.
    """

    def __init__(self, size):
        # Initially all positions are open - have not been observed
        self.open = {(x, y) for x in range(size)
                     for y in range(size)}
        # Initialize to a uniform distribution
        self.current_distribution = {pos: 1 / (size ** 2) for pos in self.open}


    def update(self, color, sensor_position, model):
        """
        Update the belief distribution based on new evidence:  our agent
        detected the given color at sensor location: sensor_position.
        :param color: (string) color detected
        :param sensor_position: (tuple) position of the sensor
        :param model (Model object) models the relationship between the
             treasure location and the sensor data
        :return: None
        """
        # Iterate over ALL positions in the grid and update the
        # probability of finding the treasure at that position - given
        # the new evidence.
        # The probability of the evidence given the Manhattan distance
        # to the treasure is given by calling model.pcolorgivendist.
        # Don't forget to normalize.
        # Don't forget to update self.open since sensor_position has
        # now been observed.

        # sum to be used for normalization
        normal_sum = float(0)

        for position in self.current_distribution:
            # calculate Manhattan distance
            distance = utils.manhattan_distance(position, sensor_position)
            # calculate probability
            prob = model.pcolorgivendist(color, distance)
            self.current_distribution[position] *= prob
            normal_sum += self.current_distribution[position]

        # normalize
        for position in self.current_distribution:
            self.current_distribution[position] /= normal_sum

        # update self.open
        self.open.discard(sensor_position)


    def recommend_sensing(self):
        """
        Recommend where we should take the next measurement in the grid.
        The position should be the most promising unobserved location.
        If all remaining unobserved locations have a probability of 0,
        return the unobserved location that is closest to the (observed)
        location with he highest probability.
        If there are no remaining unobserved locations return the
        (observed) location with the highest probability.

        :return: tuple representing the position where we should take
            the next measurement
        """
        # the observed position that has the highest probability closest to the treasure
        closest_treasure = max(self.current_distribution, key=self.current_distribution.get)
        # the unobserved position that has the highest probability closest to the treasure
        closest_unobserved = max(self.open, key=self.current_distribution.get)

        # if there are still unobserved positions remaining
        if len(self.open) > 0:
            # check for probability greater than 0
            if self.current_distribution.get(closest_unobserved) > 0:
                return closest_unobserved
            # unobserved locations have a probability of 0
            else:
                # return the unobserved location closest to the observed location w/ highest probability
                return utils.closest_point(closest_treasure, self.open)
        # there are no remaining unobserved positions
        else:
            # return the observed location w/ highest probability
            return closest_treasure
