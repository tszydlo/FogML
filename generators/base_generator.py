from abc import abstractmethod, ABC


class BaseGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass
