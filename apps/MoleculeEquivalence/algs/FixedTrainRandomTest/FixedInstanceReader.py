import numpy as np

class FixedInstanceReader:
    def __init__(self, input_fname):
        """
        :param input_fname: the input file name which contains the questions
        """
        self.input_fname = input_fname
        self.dataset = np.genfromtxt(input_fname, dtype='str', delimiter=',', skip_header=1)

    def generate_question(self, index):
        """
        return an instance generated using the distribution
        :param index: index of the question to return
        :return: [str, str, int], [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same], 
                    same is 1 if the two molecules are the same 0 otherwise
        """
        index = index % len(self.dataset)
        mol1, rep1, mol2, rep2, same = self.dataset[index]
        return [rep1 + '_' + mol1, rep2 + '_' +mol2, int(same)]

if __name__ == '__main__':
    input_fname = '../../../../local/data/04_SampleDataset/training_dataset.csv'
    generator = FixedInstanceReader(input_fname)

    print 'Hello World'