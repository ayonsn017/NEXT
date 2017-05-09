import numpy as np
from apps.MoleculeEquivalence.algs.Utils import QuestionGenerator


class FixedInstanceReader(QuestionGenerator.QuestionGenerator):
    """Class to get instances from a fixed list"""

    keys = ['Molecule1', 'Representation1', 'Molecule2', 'Representation2', 'Same']

    def __init__(self, dictlist):
        """:param dictlist: list(dict(string, string)), list of dictionaries containing the questions"""
        self.dataset = np.array([[row[key] for key in self.keys] for row in dictlist])
        self.index = 0

    def generate_question(self):
        """
        return a question using the stored index
        :return: [str, str, int], [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same],
                    same is 1 if the two molecules are the same 0 otherwise
        """
        return_value = self.generate_question_from_index(self.index)
        self.index += 1
        return return_value

    def generate_question_from_index(self, index):
        """
        return a question read from file
        :param index: index of the question to return
        :return: [str, str, int], [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same],
                    same is 1 if the two molecules are the same 0 otherwise
        """
        index = index % len(self.dataset)
        mol1, rep1, mol2, rep2, same = self.dataset[index]
        return [rep1 + '_' + mol1, rep2 + '_' + mol2, int(same)]

if __name__ == '__main__':
    input_fname = '../../../../local/data/04_SampleDataset/training_dataset.csv'
    generator = FixedInstanceReader(input_fname)

    print 'Hello World'
