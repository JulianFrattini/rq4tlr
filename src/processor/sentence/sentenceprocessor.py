from abc import ABC, abstractmethod
from structure.sentence import sentence

class SentenceProcessor(ABC):

    @property
    @abstractmethod
    def name(self):
        pass
    
    @abstractmethod
    def process(self, sentence: sentence):
        pass