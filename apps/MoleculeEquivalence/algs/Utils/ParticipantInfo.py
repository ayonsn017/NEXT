class ParticipantInfo:
    """
    class to store information regarding a participant
    """

    def __init__(self, questions=None, num_reported_answers=0):
        """
        :param questions: list(list(string, string, int)) the list of questions to be shown to the participant
        :param num_reported_answers: the number of questions the participant has answered
        """

        self.questions = questions
        self.num_reported_answers = num_reported_answers

    def increment_num_reported_answers(self):
        """
        increments the number of questions the participant has answered
        :return: num_reported_answers
        """
        self.num_reported_answers += 1