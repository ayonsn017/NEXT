import next.utils as utils
from apps.MoleculeEquivalence.algs.Utils import RandomInstanceGenerator, FixedInstanceReader, parameters, instructions, utility
import ast


class MyAlg:
    """class to present questions generated at random from both the training and test distribution"""

    increment_dictionary = {parameters.pretest_seed_key: 1, parameters.training_seed_key: 1,
                            parameters.posttest_seed_key: 1}

    def initExp(self, butler, pretest_count, training_count, posttest_count, guard_gap, alg_list):
        """
        :param butler: Butler, the butler
        :param pretest_count: int, the number of pretest questions to show
        :param training_count: int, the number of training questions to show
        :param posttest_count: int, the number of posttest questions to show
        :param guard_gap: int, the gap between guard questions
        :param alg_list: list[dict], a list containing parameters that vary across algorithms
        for this algorithm we need pretest distribution, training distribution, posttest distribution and guard data
        :return bool: True to indicate that algorithm initialization was a success
        """
        butler.algorithms.set(key=parameters.pretest_count_key, value=pretest_count)
        butler.algorithms.set(key=parameters.training_count_key, value=training_count)
        butler.algorithms.set(key=parameters.posttest_count_key, value=posttest_count)
        butler.algorithms.set(key=parameters.guard_gap_key, value=guard_gap)

        # count total number of questions to show
        guard_count = (pretest_count + training_count + posttest_count) / guard_gap
        total_questions = pretest_count + training_count + posttest_count + guard_count
        butler.algorithms.set(key=parameters.total_questions_key, value=total_questions)

        # converting string to list of dictionaries
        alg_list = ast.literal_eval(alg_list)

        # find out which parameters belong to this algorithm
        for alg_desc in alg_list:
            if alg_desc[parameters.alg_label_key] == butler.alg_label:
                alg_params = alg_desc

        # save the pretest, training, posttest, guard data, time required to finish the survey and monetary gain
        butler.algorithms.set(key=parameters.pretest_dist_key, value=alg_params[parameters.pretest_dist_key])
        butler.algorithms.set(key=parameters.training_data_key, value=alg_params[parameters.training_data_key])
        butler.algorithms.set(key=parameters.posttest_dist_key, value=alg_params[parameters.posttest_dist_key])
        butler.algorithms.set(key=parameters.guard_data_key, value=alg_params[parameters.guard_data_key])
        butler.algorithms.set(key=parameters.time_required_key, value=alg_params[parameters.time_required_key])
        butler.algorithms.set(key=parameters.monetary_gain_key, value=alg_params[parameters.monetary_gain_key])

        # save the initial seeds
        butler.algorithms.set(key=parameters.pretest_seed_key, value=parameters.pretest_seed)
        butler.algorithms.set(key=parameters.training_seed_key, value=parameters.training_seed)
        butler.algorithms.set(key=parameters.posttest_seed_key, value=parameters.posttest_seed)

        return True

    def getQuery(self, butler, participant_uid):
        """
        generate a question to be displayed to the participant
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :return [str, str, int, str]: [representation1 || '_' || molecule1,  representation2 || '_' ||molecule2, same,
        ques_type, ques_no, total_ques_count], same is 1 if the two molecules are the same 0 otherwise ques_type can
        currently be pretest, posttest or training ques_no is the question number to be displayed to the participant
        total_ques_count is the total number of questions to be displayed to the participant
        """
        # check how many question a participant has seen
        # will decide if the next question would be pretest, training or posttest based on this value
        participant_questions_key = utility.gen_participant_questions_key(participant_uid)
        num_reported_answers_key = utility.gen_num_reported_answers_key(participant_uid)

        # new participant
        if not butler.algorithms.exists(key=participant_questions_key):
            # get the question counts
            pretest_count = butler.algorithms.get(key=parameters.pretest_count_key)
            training_count = butler.algorithms.get(key=parameters.training_count_key)
            posttest_count = butler.algorithms.get(key=parameters.posttest_count_key)
            guard_gap = butler.algorithms.get(key=parameters.guard_gap_key)

            # get the data, time required to finish the survey and monetary gain
            pretest_dist = butler.algorithms.get(key=parameters.pretest_dist_key)
            training_dist = butler.algorithms.get(key=parameters.training_data_key)
            posttest_dist = butler.algorithms.get(key=parameters.posttest_dist_key)
            guard_data = butler.algorithms.get(key=parameters.guard_data_key)
            time_required = butler.algorithms.get(key=parameters.time_required_key)
            monetary_gain = butler.algorithms.get(key=parameters.monetary_gain_key)

            # increment and get the seeds for this participant
            seed_dict = butler.algorithms.increment_many(key_value_dict=self.increment_dictionary)
            pretest_seed = seed_dict[parameters.pretest_seed_key]
            training_seed = seed_dict[parameters.training_seed_key]
            posttest_seed = seed_dict[parameters.posttest_seed_key]

            # get the total number of questions to show
            total_questions = butler.algorithms.get(key=parameters.total_questions_key)

            # generate the questions for this participant and store them
            participant_questions = self.generate_all_questions(pretest_dist, training_dist, posttest_dist, guard_data,
                                                                pretest_seed, training_seed, posttest_seed,
                                                                pretest_count, training_count, posttest_count,
                                                                guard_gap, time_required, monetary_gain,
                                                                total_questions)

            butler.algorithms.set(key=participant_questions_key, value=participant_questions)

            # have a separate num reported answers entry in butler
            num_reported_answers = 0
            butler.algorithms.set(key=num_reported_answers_key, value=num_reported_answers)
        else:
            # get the participant information
            participant_questions = butler.algorithms.get(key=participant_questions_key)
            num_reported_answers = butler.algorithms.get(key=num_reported_answers_key)

        participant_question = participant_questions[num_reported_answers]

        return participant_question

    def processAnswer(self, butler, participant_uid, target_winner):
        """
        :param butler: Butler, the butler
        :participant_uid: str, a unique identifier for the participant
        :target_winner: int, index of the target the participant selected
        """
        # increment the number of questions the participant has viewed by one
        num_reported_answers_key = utility.gen_num_reported_answers_key(participant_uid)
        num_reported_answers = butler.algorithms.increment(key=num_reported_answers_key)

        # delete the entry if all questions answered
        participant_questions_key = utility.gen_participant_questions_key(participant_uid)
        participant_questions = butler.algorithms.get(key=participant_questions_key)
        if num_reported_answers == len(participant_questions):
            butler.algorithms.get_and_delete(key=participant_questions_key)
            butler.algorithms.get_and_delete(key=num_reported_answers_key)

        return True

    def getModel(self, butler):
        return True

    def generate_all_questions(self, pretest_dist, training_dist, posttest_dist, guard_data, pretest_seed,
                               training_seed, posttest_seed, pretest_count, training_count, posttest_count,
                               guard_gap, time_required, monetary_gain, total_questions):
        """
        generate all questions for a participant
        :param pretest_dist: string, the pretest distribution in string format
        :param training_dist: string, the training distribution in string format
        :param posttest_dist: string, the posttest distribution in string format
        :param guard_data: string, the guard questions in string format
        :param pretest_seed: int, the pretest seed
        :param training_seed: int, the training seed
        :param posttest_seed: int, the posttest seed
        :param pretest_count: int, the number of pretest questions to generate
        :param training_count: int, the number of training questions to generate
        :param posttest_count: int, the number of posttest questions to generate
        :param guard_gap: int, the gap between guard questions
        :param time_required: str, the time required to complete the survey, showed in introduction
        :param monetary_gain: str, the monetary gain to the participants
        :param total_questions: int, total number of molecule questions to show to the participant
        :return: ParticipantInfo: all questions generated for the participant put in a PariticipantInfo object
        """
        participant_questions = []

        '''
        # not showing first instruction question since we don not need consent for MTurkers
        # introduction instruction 1
        # same structure as molecule question. m1 contains the instruction. m2 is empty. same is set to 0. ques_count
        # also set to zero
        participant_question = \
            [instructions.get_introduction_instruction1(monetary_gain), '', 0, parameters.instruction_key, 0, total_questions]
        participant_questions.append(participant_question)
        '''

        # introduction instruction 2
        participant_question = \
            [instructions.get_introduction_instruction2(pretest_count, training_count, posttest_count, guard_gap,
                                                        time_required), '', 0, parameters.terms_key, 0,
             total_questions]
        participant_questions.append(participant_question)

        # pretest instruction
        participant_question = [instructions.get_pretest_instruction(), '', 0, parameters.instruction_key, 0,
                                total_questions]
        participant_questions.append(participant_question)

        index = 1
        # guard question generator
        guard_question_generator = FixedInstanceReader.FixedInstanceReader(guard_data)

        # pretest questions
        pretest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(pretest_dist, seed=pretest_seed)
        participant_questions, index = utility.gen_participant_questions(pretest_question_generator,
                                                                         guard_question_generator,
                                                                         pretest_count, parameters.pretest_key, index,
                                                                         guard_gap, participant_questions,
                                                                         total_questions)

        # training instruction
        participant_question = [instructions.get_training_instruction(), '', 0, parameters.instruction_key, 0,
                                total_questions]
        participant_questions.append(participant_question)

        # training questions
        training_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(training_dist, seed=training_seed)
        participant_questions, index = utility.gen_participant_questions(training_question_generator,
                                                                         guard_question_generator,
                                                                         training_count, parameters.training_key, index,
                                                                         guard_gap, participant_questions,
                                                                         total_questions)

        # posttest instruction
        participant_question = [instructions.get_posttest_instruction(), '', 0, parameters.instruction_key, 0,
                                total_questions]
        participant_questions.append(participant_question)

        # posttest questions
        posttest_question_generator = RandomInstanceGenerator.RandomInstanceGenerator(posttest_dist, seed=posttest_seed)
        participant_questions, index = utility.gen_participant_questions(posttest_question_generator,
                                                                         guard_question_generator, posttest_count,
                                                                         parameters.posttest_key, index, guard_gap,
                                                                         participant_questions, total_questions)

        return participant_questions
