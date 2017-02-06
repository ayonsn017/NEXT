import time
import numpy.random
import next.utils as utils
from apps.MoleculeEquivalence.algs.Utils import RandomInstanceGenerator, FixedInstanceReader, parameters
import ast

class FixedTrainRandomTest:
    pretest_count_key = 'pretest_count'
    training_count_key = 'training_count'
    posttest_count_key = 'posttest_count'
    num_reported_answers_key = 'num_reported_answers'
    pretest_key = 'pretest'
    training_key = 'training'
    posttest_key = 'posttest'
    pretest_file_key = 'pretest_file'
    training_file_key = 'training_file'
    posttest_file_key = 'posttest_file'
    pretest_generator_key = 'pretest_generator'
    training_generator_key = 'training_generator'
    posttest_generator_key = 'posttest_generator'
    pretest_seed_key = 'pretest_seed'
    posttest_seed_key = 'posttest_seed_key'
    participant_answers_count_dict_key = 'participant_answers_count_dict'
    alg_label_key = 'alg_label'
    def initExp(self,butler, pretest_count, training_count, posttest_count, alg_list):
        """
        :param butler: Butler, the butler
        :param pretest_count: int, the number of pretest questions to show
        :param training_count: int, the number of training questions to show
        :param posttest_count: int, the number of posttest questions to show
        :param alg_list: list[dict], a list containing parameters that vary across algorithms
                                 for this algorithm we need pretest, training and posttest files that contain the pretest, training and posttest 
                                 distribution respectively
        :return bool: True to indicate that algorithm initialization was a success
        """
        butler.algorithms.set(key='pretest_count', value=pretest_count)
        butler.algorithms.set(key='training_count', value=training_count)
        butler.algorithms.set(key='posttest_count', value=posttest_count)
        butler.algorithms.set(key='num_reported_answers', value=0)  # the number of total questions answered for this algorithm
        # dictionary to store the number of questions the participant has answered
        butler.algorithms.set(key=self.participant_answers_count_dict_key, value={}) 

        # converting string to list of dictionaries
        alg_list = ast.literal_eval(alg_list)

        # find out which parameters belong to this algorithm
        for alg_desc in alg_list:
            if alg_desc[self.alg_label_key] == butler.alg_label:
                alg_params = alg_desc

        # extract the pretest, training and posttest file names and instantiate the generators
        pretest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(alg_params[self.pretest_file_key])
        butler.algorithms.set(key=self.pretest_generator_key, value=pretest_question_generator)
        training_question_generator = FixedInstanceReader.FixedInstanceReader(alg_params[self.training_file_key])
        butler.algorithms.set(key=self.training_generator_key, value=training_question_generator)
        posttest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(alg_params[self.posttest_file_key])
        butler.algorithms.set(key=self.posttest_generator_key, value=posttest_question_generator)

        return True


    def getQuery(self, butler, participant_uid):
        """
        generate a question to be displayed to the participant
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :return [str, str, int, str]: [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same, ques_type], 
                    same is 1 if the two molecules are the same 0 otherwise
                    ques_type can currently be pretest, posttest or training
        """
        # calculate how many question a participant has seen
        # will decide if the next question would be pretest, training or posttest based on this value
        participant_answers_count_dict = butler.algorithms.get(key=self.participant_answers_count_dict_key)

        # new participant
        if participant_uid not in participant_answers_count_dict:
            participant_answers_count_dict[participant_uid] = 0
            # need this set step, otherwise butler values are not updated
            butler.algorithms.set(key=self.participant_answers_count_dict_key, value=participant_answers_count_dict)   
            num_reported_answers = 0
        else:
            num_reported_answers = participant_answers_count_dict[participant_uid]

        # decide which type of question to show and generate that type of question
        pretest_count = butler.algorithms.get(key=self.pretest_count_key)
        training_count = butler.algorithms.get(key=self.training_count_key)
        posttest_count = butler.algorithms.get(key=self.posttest_count_key)

        if num_reported_answers < pretest_count:
            question_generator = butler.algorithms.get(key=self.pretest_generator_key)
            ques_type = self.pretest_key
            mol1, mol2, same = question_generator.generate_question() 
        elif num_reported_answers >= pretest_count and num_reported_answers < pretest_count + training_count:
            training_index = num_reported_answers - pretest_count # the index of the training question to get
            question_generator = butler.algorithms.get(key=self.training_generator_key)
            ques_type = self.training_key
            mol1, mol2, same = question_generator.generate_question(training_index) 
        elif num_reported_answers >= pretest_count + training_count:
            question_generator = butler.algorithms.get(key=self.posttest_generator_key)
            ques_type = self.posttest_key
            mol1, mol2, same = question_generator.generate_question() 

        

        return [mol1, mol2, same, ques_type]

    def processAnswer(self,butler, participant_uid, target_winner):
        """
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :target_winner: int, index of the target the participant selected
        """
        butler.algorithms.increment(key='num_reported_answers')

        # increment the number of questions the participant has viewed
        participant_answers_count_dict = butler.algorithms.get(key=self.participant_answers_count_dict_key)
        num_reported_answers = participant_answers_count_dict[participant_uid] + 1
        if num_reported_answers == 12:
            participant_answers_count_dict.pop(participant_uid, 'None')
        else:
            participant_answers_count_dict[participant_uid] = num_reported_answers
        # need this set step, otherwise butler values are not updated
        butler.algorithms.set(key=self.participant_answers_count_dict_key, value=participant_answers_count_dict)   

        return True


    def getModel(self, butler):
        return True
