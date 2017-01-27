import numpy as np

class RandomInstanceGenerator:
    probability_index = 5  # index in distribution list where the probability value is stored
    same_index = 4  # index in distribution list where the same variable is stored
    def __init__(self, input_fname, seed=-1):
        """
        :param input_fname: string, name of the file that contains the distribution
        :param seed: int, default value -1, the random seed to use while generating instances
        """
        self.distributions = np.genfromtxt(input_fname, dtype='str', delimiter=',', skip_header=1)
        self.probabilities = [float(entry[self.probability_index]) for entry in self.distributions ]

        if seed != -1:
            np.random.seed(seed);


    def generate_instance(self):
        """
        return an instance generated using the distribution
        :return: [str, str, str, str, int], [molecule1, representation1, molecule2, representation2, same], 
                    same is 1 if the two molecules are the same 0 otherwise
        """
        multinomial_draw = np.random.multinomial(1, self.probabilities, size=1)[0]

        index = np.where(multinomial_draw==1)[0][0]

        # generate a RV from Bernoulli distribution to decide whether the molecule positions will be flipped or not
        flip = np.random.binomial(1, 0.5)
        if flip == 0:
            return self.distributions[index][:self.probability_index]
        else:
            mol1, rep1, mol2, rep2, same = self.distributions[index][:self.probability_index]
            return [mol2, rep2, mol1, rep1, same]


if __name__ == '__main__':
    input_fname = '03_TrainingPool/training_dist_LewisSF.csv'

    instance_generator1 = RandomInstanceGenerator(input_fname, seed=10)
    

    for i in range(6):
        print i, 'instance generator round 1', instance_generator1.generate_instance()
        
    np.random.seed(10)

    for i in range(6):
        print i, 'instance generator round 2', instance_generator1.generate_instance()

