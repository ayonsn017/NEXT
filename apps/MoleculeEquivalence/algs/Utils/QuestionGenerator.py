from abc import ABCMeta, abstractmethod

class QuestionGenerator:
    """
    abstract base class to generate questions
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_question(self):
        return
