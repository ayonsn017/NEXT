import time
import numpy.random
from apps.MoleculesPoolBasedTripletMDS.algs.RandomTrainTest import utilsMDS
import next.utils as utils
from apps.MoleculesPoolBasedTripletMDS.algs.RandomTrainTest import RandomInstanceGenrator

class RandomTrainTest:
    pretest_count_key = 'pretest_count'
    training_count_key = 'training_count'
    posttest_count_key = 'posttest_count'
    num_reported_answers_key = 'num_reported_answers'
    pretest_key = 'pretest'
    training_key = 'training'
    posttest_key = 'posttest'
    participant_answers_count_dict_key = 'participant_answers_count_dict'
    participant_question_generator_dict_key = 'participant_question_generator_dict'
    def initExp(self,butler, pretest_count, training_count, posttest_count,pretest_file, training_file, posttest_file):
        butler.algorithms.set(key='pretest_count', value=pretest_count)
        butler.algorithms.set(key='training_count', value=training_count)
        butler.algorithms.set(key='posttest_count', value=posttest_count)
        butler.algorithms.set(key='num_reported_answers', value=0)  # the number of total questions answered for this algorithm
        butler.algorithms.set(key=self.participant_answers_count_dict_key, value={}) # dictionary to store the number of questions the participant has answered

        log_fname = 'log.txt'
        log_file = open(log_fname, 'a')
        log_file.write('Will this work: ' + butler.alg_id + 'what up?\n')
        log_file.close()

        return True


    def getQuery(self, butler, participant_uid):
        num_reported_answers = butler.algorithms.get(key='num_reported_answers')

        # calculate how many question a participant has seen
        # will decide if the next question would be pretest, training or posttest based on this value
        participant_answers_count_dict = butler.algorithms.get(key=self.participant_answers_count_dict_key)

        # new participant
        if participant_uid not in participant_answers_count_dict:
            participant_answers_count_dict[participant_uid] = 0
            num_reported_answers = 0
        else:
            num_reported_answers = participant_answers_count_dict[participant_uid]

        pretest_count = butler.algorithms.get(key=self.pretest_count_key)
        training_count = butler.algorithms.get(key=self.training_count_key)
        posttest_count = butler.algorithms.get(key=self.posttest_count_key)

        if num_reported_answers < pretest_count:
            mol1, mol2, same = utilsMDS.getRandomQuery()
            ques_type = self.pretest_key
        elif num_reported_answers >= pretest_count and num_reported_answers < pretest_count + training_count:
            mol1, mol2, same =  utilsMDS.get_random_training_query()
            ques_type = self.training_key
        elif num_reported_answers >= pretest_count + training_count:
            mol1, mol2, same = utilsMDS. getRandomQuery()
            ques_type = self.posttest_key

        # increment the number of questions the participant has viewed
        participant_answers_count_dict[participant_uid] = num_reported_answers + 1    
        butler.algorithms.set(key=self.participant_answers_count_dict_key, value=participant_answers_count_dict)  
        return [mol1, mol2, same, ques_type]

    def processAnswer(self,butler,center_id,left_id,right_id,target_winner):
        num_reported_answers = butler.algorithms.increment(key='num_reported_answers')
        return True


    def getModel(self, butler):
        return True
