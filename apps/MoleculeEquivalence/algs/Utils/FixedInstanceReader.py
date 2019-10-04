"""
script for fixed training set possibly with highlighting

@author: Ayon
"""
from __future__ import division, print_function
import numpy as np
from apps.MoleculeEquivalence.algs.Utils import QuestionGenerator


class FixedInstanceReader(QuestionGenerator.QuestionGenerator):
    """Class to get instances from a fixed list"""

    non_highlight_keys = ['Molecule1', 'Representation1', 'Molecule2',
                          'Representation2', 'Same']
    highlight_keys = ['Molecule1', 'Representation1', 'Molecule2',
                      'Representation2', 'Same', 'Highlight1', 'Highlight2']

    def __init__(self, dictlist, seed=-1):
        """
        :param dictlist: list(dict(string, string)), list of dictionaries
        containing the questions
        :param seed: int, default value -1,
        the random seed to use to fix the order of representation
        """
        # check if highlighting given or not
        if 'Highlight1' not in dictlist[0].keys():
            self.keys = self.non_highlight_keys
            self.highlight = False
        else:
            self.keys = self.highlight_keys
            self.highlight = True
        self.dataset = np.array([[row[key] for key in self.keys]
                                 for row in dictlist])
        self.index = 0

        if seed != -1:
            np.random.seed(seed)

    def generate_question(self):
        """
        return a question using the stored index
        :return
            str, representation1 || '_' || molecule1
            str, representation2 || '_' || molecule2
            str, 1 if the two molecules are the same 0 otherwise
            str, representation1 || '_' || highlight1, if present None
            otherwise
            str, representation1 || '_' || highlight2, if present None
            otherwise
        """
        return_value = self.generate_question_from_index(self.index)
        self.index += 1
        return return_value

    def generate_question_from_index(self, index):
        """
        return a question read from file
        :param index: index of the question to return
        :return
            str, representation1 || '_' || molecule1
            str, representation2 || '_' || molecule2
            str, 1 if the two molecules are the same 0 otherwise
            str, representation1 || '_' || highlight1, if present None
            otherwise
            str, representation1 || '_' || highlight2, if present None
            otherwise
        """
        index = index % len(self.dataset)
        # flip a just coin to switch the position of the molecules on screen

        if not self.highlight:
            mol1, rep1, mol2, rep2, same = self.dataset[index]
            rep_hlight1, rep_hlight2 = '', ''

        else:
            mol1, rep1, mol2, rep2, same, hlight1, hlight2 = \
                self.dataset[index]
            rep_hlight1 = rep1 + '_' + hlight1
            rep_hlight2 = rep2 + '_' + hlight2

        # toss a coin to determine the order of molecules
        head = np.random.binomial(1, 0.5)
        if head == 1:
            mol1, rep1, mol2, rep2, rep_hlight1, rep_hlight2 = \
                mol2, rep2, mol1, rep1, rep_hlight2, rep_hlight1

        return [rep1 + '_' + mol1, rep2 + '_' + mol2, int(same),
                rep_hlight1, rep_hlight2]


if __name__ == '__main__':
    input_fname = \
        '../../../../local/data/04_SampleDataset/training_dataset.csv'
    generator = FixedInstanceReader(input_fname)

    print('Hello World')
