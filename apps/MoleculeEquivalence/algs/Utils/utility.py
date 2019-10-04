from apps.MoleculeEquivalence.algs.Utils import parameters


def gen_participant_questions(question_generator,
                              guard_question_generator, ques_count,
                              ques_type, index, guard_gap,
                              participant_questions,
                              total_questions):
    """
    :param question_generator: QuestionGenerator, generates questions
    :param guard_question_generator: FixedInstanceReader, generates guards
    questions
    :param ques_count: int, number of questions to generate excluding the
    guard questions
    :param ques_type: string, the type of questions to generate (not counting
    the guard questions)
    :param index: int, the starting index of the generated questions to be
    shown to the participant
    :param guard_gap: int, the gap between guard questions
    :param total_questions: int, total number of molecule questions to show
    :param participant_questions: list(list(mol1:string, mol2:string, same:int,
    ques type:string, mol ques no:int, total mol ques noint)),
    the list of questions to which the newly generated questions will be added
    :return
        list[string, string, int, string, int, int], the list of participant
        questions
    """
    m1_index, m2_index, sindex, h1_index, h2_index = 0, 1, 2, 3, 4
    for i in range(ques_count):
        # adding the question type
        question = question_generator.generate_question()
        participant_question = [question[m1_index], question[m2_index],
                                question[sindex], ques_type, index,
                                total_questions, question[h1_index],
                                question[h2_index]]
        index += 1
        participant_questions.append(participant_question)

        # check if we should add guard questions
        if index % (guard_gap + 1) == 0:
            guard_question = guard_question_generator.generate_question()
            participant_question = [guard_question[m1_index],
                                    guard_question[m2_index],
                                    guard_question[sindex],
                                    parameters.guard_key, index,
                                    total_questions, 'Lewis_H2', 'Lewis_O2']
            index += 1
            participant_questions.append(participant_question)

    return participant_questions, index


def gen_num_reported_answers_key(participant_uid):
    """
    generates a key for the number of reported answers for each new participant
    :param participant_uid: the participant uid
    :return string, a key for the number of reported answers for that
    participant
    """
    return participant_uid + 'num_reported_answers'


def gen_participant_questions_key(participant_uid):
    """
    generates a key for the participant infofor each new participant
    :param participant_uid: the participant uid
    :return string, a key for the number of reported answers for that
    participant
    """
    return participant_uid + 'participant_questions'
