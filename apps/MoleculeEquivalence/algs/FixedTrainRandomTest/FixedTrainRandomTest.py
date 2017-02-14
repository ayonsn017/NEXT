import time
import numpy.random
import next.utils as utils
from apps.MoleculeEquivalence.algs.Utils import RandomInstanceGenerator, FixedInstanceReader, parameters, ParticipantInfo, instructions, ParticipantQuestion, utility
import ast

class FixedTrainRandomTest:
    pretest_count_key = 'pretest_count'
    training_count_key = 'training_count'
    posttest_count_key = 'posttest_count'
    guard_gap_key = 'guard_gap'
    num_reported_answers_key = 'num_reported_answers'
    pretest_key = 'pretest'
    training_key = 'training'
    posttest_key = 'posttest'
    pretest_file_key = 'pretest_file'
    training_file_key = 'training_file'
    posttest_file_key = 'posttest_file'
    guard_file_key = 'guard_file'
    pretest_generator_key = 'pretest_generator'
    training_generator_key = 'training_generator'
    posttest_generator_key = 'posttest_generator'
    pretest_seed_key = 'pretest_seed'
    posttest_seed_key = 'posttest_seed'
    participant_info_dict_key = 'participant_info_dict'
    alg_label_key = 'alg_label'
    def initExp(self,butler, pretest_count, training_count, posttest_count, guard_gap, alg_list):
        """
        :param butler: Butler, the butler
        :param pretest_count: int, the number of pretest questions to show
        :param training_count: int, the number of training questions to show
        :param posttest_count: int, the number of posttest questions to show
        :param guard_gap: int, gap between guard questions
        :param alg_list: list[dict], a list containing parameters that vary across algorithms
                                 for this algorithm we need pretest, training and posttest files that contain the pretest, training and posttest 
                                 distribution respectively
        :return bool: True to indicate that algorithm initialization was a success
        """
        butler.algorithms.set(key=self.pretest_count_key, value=pretest_count)
        butler.algorithms.set(key=self.training_count_key, value=training_count)
        butler.algorithms.set(key=self.posttest_count_key, value=posttest_count)
        butler.algorithms.set(key=self.guard_gap_key, value=guard_gap)
        butler.algorithms.set(key='num_reported_answers', value=0)  # the number of total questions answered for this algorithm
        # dictionary to store the information for a participant
        butler.algorithms.set(key=self.participant_info_dict_key, value={})

        # converting string to list of dictionaries
        alg_list = ast.literal_eval(alg_list)

        # find out which parameters belong to this algorithm
        for alg_desc in alg_list:
            if alg_desc[self.alg_label_key] == butler.alg_label:
                alg_params = alg_desc

        # save the pretest, training, posttest and guard files
        butler.algorithms.set(key=self.pretest_file_key, value=alg_params[self.pretest_file_key])
        butler.algorithms.set(key=self.training_file_key, value=alg_params[self.training_file_key])
        butler.algorithms.set(key=self.posttest_file_key, value=alg_params[self.posttest_file_key])
        butler.algorithms.set(key=self.guard_file_key, value=alg_params[self.guard_file_key])

        # save the initial seeds
        butler.algorithms.set(key=self.pretest_seed_key, value=parameters.pretest_seed)
        butler.algorithms.set(key=self.posttest_seed_key, value=parameters.posttest_seed)

        return True


    def getQuery(self, butler, participant_uid):
        """
        generate a question to be displayed to the participant
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :return [str, str, int, str]: [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same, ques_type], 
                    same is 1 if the two molecules are the same 0 otherwise
                    ques_type can currently be pretest, posttest or training
                    ques_no is the question number to be displayed to the participant
                    total_ques_count is the total number of questions to be displayed to the participant
        """
        """
        generate a question to be displayed to the participant
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :return [str, str, int, str]: [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same, ques_type], 
                    same is 1 if the two molecules are the same 0 otherwise
                    ques_type can currently be pretest, posttest or training
        """
        # get the question counts
        pretest_count = butler.algorithms.get(key=self.pretest_count_key)
        training_count = butler.algorithms.get(key=self.training_count_key)
        posttest_count = butler.algorithms.get(key=self.posttest_count_key)
        guard_gap = butler.algorithms.get(key=self.guard_gap_key)

        # count total number of questions to show
        guard_count = (pretest_count + training_count + posttest_count) / guard_gap
        total_questions = pretest_count + training_count + posttest_count + guard_count

        # acquire the question generation lock
        ques_gen_lock = butler.memory.lock(parameters.ques_gen_lock_name)
        ques_gen_lock.acquire()

        # check how many question a participant has seen
        # will decide if the next question would be pretest, training or posttest based on this value
        participant_info_dict = butler.algorithms.get(key=self.participant_info_dict_key)

        # new participant
        if participant_uid not in participant_info_dict:
            # get the file names
            pretest_file = butler.algorithms.get(key=self.pretest_file_key)
            training_file = butler.algorithms.get(key=self.training_file_key)
            posttest_file = butler.algorithms.get(key=self.posttest_file_key)
            guard_file = butler.algorithms.get(key=self.guard_file_key)

            # get the seed for this participant and generate the questions
            pretest_seed = butler.algorithms.get(key=self.pretest_seed_key)
            posttest_seed = butler.algorithms.get(key=self.posttest_seed_key)

            # generate the questions for this participant and store them
            participant_info = self.generate_all_questions(pretest_file, training_file, posttest_file, guard_file, pretest_seed, posttest_seed, 
                                                                                          pretest_count, training_count, posttest_count, guard_gap)            

            participant_info_dict[participant_uid] = participant_info
            butler.algorithms.set(key=self.participant_info_dict_key, value=participant_info_dict)

            # increment the seed values
            butler.algorithms.increment(key=self.pretest_seed_key)
            butler.algorithms.increment(key=self.posttest_seed_key)


        else:
            # get the participant information
            participant_info = butler.algorithms.get(key=self.participant_info_dict_key)[participant_uid]
        # release the lock
        ques_gen_lock.release()
        
        participant_question = participant_info.questions[participant_info.num_reported_answers]

        return [participant_question.mol1, participant_question.mol2, participant_question.same, participant_question.ques_type, 
                    participant_question.ques_count, total_questions]

    def processAnswer(self,butler, participant_uid, target_winner):
        """
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :target_winner: int, index of the target the participant selected
        """
        butler.algorithms.increment(key='num_reported_answers')

        # get the question counts
        pretest_count = butler.algorithms.get(key=self.pretest_count_key)
        training_count = butler.algorithms.get(key=self.training_count_key)
        posttest_count = butler.algorithms.get(key=self.posttest_count_key)

        total_questions = pretest_count + training_count + posttest_count

        # increment the number of questions the participant has viewed
        num_reported_answers_increment_lock = butler.memory.lock('num_reported_answers_increment_lock')
        num_reported_answers_increment_lock.acquire()
        participant_info_dict = butler.algorithms.get(key=self.participant_info_dict_key)
        participant_info = participant_info_dict[participant_uid]
        num_reported_answers = participant_info.increment_num_reported_answers()

        # if participant has answered all questions then delete information related to him/her
        if num_reported_answers == total_questions:
            participant_info_dict.pop(participant_uid, 'None')
        else:
            participant_info_dict[participant_uid] = participant_info
        # need this set step, otherwise butler values are not updated
        butler.algorithms.set(key=self.participant_info_dict_key, value=participant_info_dict)   
        num_reported_answers_increment_lock.release()

        return True


    def getModel(self, butler):
        return True

    def generate_all_questions(self, pretest_file, training_file, posttest_file, guard_file, pretest_seed, posttest_seed, pretest_count, 
                                                  training_count, posttest_count, guard_gap):
        """
        generate all questions for a participant
        :param pretest_file: string, the pretest file name
        :param training_file: string, the training file name
        :param posttest_file: string, the posttest file name
        :param guard_file: string, the guard file name
        :param pretest_seed: int, the pretest seed
        :param posttest_seed: int, the posttest seed
        :param pretest_count: int, the number of pretest questions to generate
        :param training_count: int, the number of training questions to generate
        :param posttest_count: int, the number of posttest questions to generate
        :param guard_gap: int, the gap between guard questions
        :return: ParticipantInfo: all questions generated for the participant put in a PariticipantInfo object
        """
        participant_questions = []

        # introduction instruction 1
        participant_question = ParticipantQuestion.ParticipantQuestion(instructions.get_introduction_instruction1(), '', 0, 
                                                                                                                    parameters.instruction_key, 0)
        participant_questions.append(participant_question)

        # introduction instruction 2
        participant_question = ParticipantQuestion.ParticipantQuestion(instructions.get_introduction_instruction2(), '', 0, 
                                                                                                                    parameters.instruction_key, 0)
        participant_questions.append(participant_question)

        # pretest instruction
        participant_question = ParticipantQuestion.ParticipantQuestion(instructions.get_pretest_instruction(), '', 0, 
                                                                                                                    parameters.instruction_key, 0)
        participant_questions.append(participant_question)

        index = 1
        # guard question generator
        guard_question_generator = FixedInstanceReader.FixedInstanceReader(guard_file)

        # pretest questions
        pretest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(pretest_file, seed=pretest_seed)
        participant_questions, index = utility.gen_participant_questions(pretest_question_generator, guard_question_generator, 
                                                                                                                     pretest_count, parameters.pretest_key, index, guard_gap, 
                                                                                                                     participant_questions)

        # training instruction
        participant_question = ParticipantQuestion.ParticipantQuestion(instructions.get_training_instruction(), '', 0, 
                                                                                                                    parameters.instruction_key, 0)
        participant_questions.append(participant_question)

        # training questions
        training_question_generator = FixedInstanceReader.FixedInstanceReader(training_file)
        participant_questions, index = utility.gen_participant_questions(training_question_generator, guard_question_generator, 
                                                                                                                     training_count, parameters.training_key, index, guard_gap, 
                                                                                                                     participant_questions)

        # posttest instruction
        participant_question = ParticipantQuestion.ParticipantQuestion(instructions.get_posttest_instruction(), '', 0, 
                                                                                                                    parameters.instruction_key, 0)
        participant_questions.append(participant_question)

        # posttest questions
        posttest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(posttest_file, seed=posttest_seed)
        participant_questions, index = utility.gen_participant_questions(posttest_question_generator, guard_question_generator, 
                                                                                                                     posttest_count, parameters.posttest_key, index, guard_gap,
                                                                                                                      participant_questions)

        num_reported_answers = 0
        participant_info = ParticipantInfo.ParticipantInfo(questions=participant_questions, num_reported_answers=num_reported_answers)

        return participant_info

