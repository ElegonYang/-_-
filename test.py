import abc


class BaseStudent(abc.ABC):

    def __init__(self, name='kevin'):
        self._name = name

    @classmethod
    def find_student(cls, name):
        n = name.lower()
        for student in cls.__subclasses__():
            if student.__name__ == n:
                return student
            raise ValueError('查無此學生')

    @abc.abstractmethod
    def answer(self):
        """回答問題"""


class Jake(BaseStudent):
    ...
