class ParticipantQuestion:
    def __init__(self, mol1, mol2, same, ques_type, ques_count):
        """
        :param mol1: string, the first molecule. for instruction questions this will contain the instruction
        :param mol2: string, the second molecule. for instruction questions this will be an empty string
        :param same: int, 1 if mol1 and mol2 are the same, 0 otherwise. for instruction questions this value will be 0
        :param ques_type: string, the type of question
        :param ques_count: int, the number of the question to be shown, for instruction questions this value will be 0
        """
        self.mol1 = mol1
        self.mol2 = mol2
        self.same = same
        self.ques_type = ques_type
        self.ques_count = ques_count
        