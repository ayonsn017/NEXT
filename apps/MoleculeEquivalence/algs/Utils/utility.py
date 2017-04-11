from apps.MoleculeEquivalence.algs.Utils import parameters, ParticipantQuestion

def gen_participant_questions(question_generator, guard_question_generator, ques_count, ques_type, index, guard_gap,
                                                    participant_questions):
    """
    :param question_generator: QuestionGenerator, generates questions
    :param guard_question_generator: FixedInstanceReader, generates guards questions
    :param ques_count: int, number of questions to generate excluding the guard questions
    :param ques_type: string, the type of questions to generate (not counting the guard questions)
    :param index: int, the starting index of the generated questions to be shown to the participant
    :param guard_gap: int, the gap between guard questions
    :param participant_questions: list(ParticipantQuestion), the list to which the newly generated questions will be added
    :return: participant_questions: list(ParticipantQuestion): the updated list
                  index: int, the index of the next question to be displayed
    """
    for i in range(ques_count):
        # adding the question type
        question = question_generator.generate_question()
        participant_question = ParticipantQuestion.ParticipantQuestion(question[0], question[1], question[2],
                                                                                                                    ques_type, index)
        index += 1
        participant_questions.append(participant_question)

        # check if we should add guard questions
        if index % (guard_gap + 1) == 0:
            guard_question = guard_question_generator.generate_question()
            participant_question = ParticipantQuestion.ParticipantQuestion(guard_question[0], guard_question[1], guard_question[2],
                                                                                                                        parameters.guard_key, index)
            index += 1
            participant_questions.append(participant_question)

    return participant_questions, index


def gen_num_reported_answers_key(participant_uid):
    """
    generates a key for the number of reported answers for each new participant
    :param participant_uid: the participant uid
    :return string, a key for the number of reported answers for that participant
    """
    return participant_uid + 'num_reported_answers'
