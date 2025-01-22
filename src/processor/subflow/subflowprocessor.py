from abc import ABC, abstractmethod
from src.structure.sentence import sentence

class SubflowProcessor(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def process(self, subflow: list[sentence]):
        pass