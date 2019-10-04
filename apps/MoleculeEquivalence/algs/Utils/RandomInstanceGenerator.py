"""
script to sample a question from a distribution

@author: Ayon
"""
from __future__ import division, print_function
import numpy as np
from apps.MoleculeEquivalence.algs.Utils import QuestionGenerator


class RandomInstanceGenerator(QuestionGenerator.QuestionGenerator):
    """Class to generate random questions from a distribution"""

    probability_index = 5  # index in distribution list where the probability value is stored
    same_index = 4  # index in distribution list where the same variable is stored
    keys = ['Molecule1', 'Representation1', 'Molecule2', 'Representation2', 'Same', 'Probability']

    def __init__(self, dictlist, seed=-1):
        """
        :param dictlist: list(dict(string, string)), list of dictionaries containing the distribution
        :param seed: int, default value -1, the random seed to use while generating instances
        """
        self.distributions = np.array([[row[key] for key in self.keys] for row in dictlist])
        self.probabilities = [float(entry[self.probability_index]) for entry in self.distributions]

        if seed != -1:
            np.random.seed(seed)

    def generate_question(self):
        """
        return a question generated using the distribution
        :return
            str, representation1 || '_' || molecule1
            str, representation2 || '_' || molecule2
            str, 1 if the two molecules are the same 0 otherwise
            str, dummy highlight for molecule 1
            str, dummy highlight for molecule 2
        """
        multinomial_draw = \
            np.random.multinomial(1, self.probabilities, size=1)[0]

        index = np.where(multinomial_draw == 1)[0][0]

        # generate a RV from Bernoulli distribution to decide whether the
        # molecule positions will be flipped or not
        flip = np.random.binomial(1, 0.5)
        if flip == 0:
            mol1, rep1, mol2, rep2, same = \
                self.distributions[index][:self.probability_index]
        else:
            mol2, rep2, mol1, rep1, same = \
                self.distributions[index][:self.probability_index]

        # if this question is found again then generate a new question by
        # recursion
        temp_mol1, temp_mol2 = rep1 + '_' + mol1, rep2 + '_' + mol2
        if temp_mol1 == 'SF_(C2H5)2O' or temp_mol2 == 'SF_(C2H5)2O':
            return self.generate_question()

        return [rep1 + '_' + mol1, rep2 + '_' + mol2, same, '', '']


if __name__ == '__main__':
    input_fname = \
        '../../../../local/data/03_TrainingPool/training_dist_LewisSF.csv'

    instance_generator1 = RandomInstanceGenerator(input_fname, seed=10)

    for i in range(6):
        print(i, 'instance generator round 1',
              instance_generator1.generate_question())

    np.random.seed(10)

    for i in range(6):
        print(i, 'instance generator round 2',
              instance_generator1.generate_question())
